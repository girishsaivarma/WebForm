from flask import Flask, jsonify, request
from datetime import datetime
import threading
import secrets
import re

app = Flask(__name__)

# Global variables for storing data
user_counter = 0
post_counter = 0
user_storage = {}
post_storage = {}
data_access_lock = threading.Lock()

# Helper function to generate a unique user key
def generate_unique_key():
    return secrets.token_urlsafe(16)

# Endpoint to create a new user
@app.route('/register', methods=['POST'])
def register_user():
    with data_access_lock:
        # Validate request format
        if not request.is_json:
            return jsonify(error='Invalid JSON format.'), 400

        user_details = request.get_json()
        name = user_details.get('name')
        if not isinstance(name, str):
            return jsonify(error='Name is required and must be a string.'), 400

        user_name = user_details.get('username')
        if not isinstance(user_name, str):
            return jsonify(error='Username is required and must be a string.'), 400

        # Check for existing username
        if any(user['username'] == user_name for user in user_storage.values()):
            return jsonify(error='Username already in use.'), 400

        # Create new user
        global user_counter
        user_counter += 1
        new_user_key = generate_unique_key()
        user_storage[user_counter] = {'id': user_counter, 'name': name, 'username': user_name, 'key': new_user_key}

        return jsonify(id=user_counter, key=new_user_key), 200

# Endpoint to get user information by ID or username
@app.route('/user/<user_identifier>', methods=['GET'])
def get_user(user_identifier):
    with data_access_lock:
        user = None
        if user_identifier.isdigit():
            user = user_storage.get(int(user_identifier))
        else:
            user = next((u for u in user_storage.values() if u['username'] == user_identifier), None)

        if user is None:
            return jsonify(error='User not found.'), 404

        user_info = {'id': user['id'], 'name': user['name'], 'username': user['username']}
        return jsonify(user_info), 200

# Endpoint to update user information
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    with data_access_lock:
        if user_id not in user_storage:
            return jsonify(error='User not found.'), 404

        update_data = request.get_json()
        if 'key' not in update_data or user_storage[user_id]['key'] != update_data['key']:
            return jsonify(error='Unauthorized access.'), 401

        # Update user details
        user_storage[user_id].update({k: v for k, v in update_data.items() if k in ['name', 'username']})
        return jsonify(message='User information updated successfully.'), 200

# Endpoint to create a new post
@app.route('/post', methods=['POST'])
def create_post():
    with data_access_lock:
        post_data = request.get_json()

        # Validate post data
        if 'msg' not in post_data or not isinstance(post_data['msg'], str):
            return jsonify(error='Invalid post message.'), 400

        global post_counter
        post_counter += 1
        new_post_key = generate_unique_key()

        post_details = {'id': post_counter, 'msg': post_data['msg'], 'key': new_post_key, 'timestamp': datetime.utcnow().isoformat()}
        if 'user_id' in post_data and 'user_key' in post_data:
            user_id = post_data['user_id']
            if user_storage.get(user_id, {}).get('key') == post_data['user_key']:
                post_details.update({'user_id': user_id, 'username': user_storage[user_id]['username']})
            else:
                return jsonify(error='Invalid user credentials.'), 401

        post_storage[post_counter] = post_details
        return jsonify(post_details), 200

# Endpoint to get a specific post by ID
@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    with data_access_lock:
        if post_id not in post_storage:
            return jsonify(error='Post not found.'), 404

        post = post_storage[post_id]
        post_info = {k: v for k, v in post.items() if k != 'key'}
        return jsonify(post_info), 200

# Endpoint to delete a post
@app.route('/post/<int:post_id>/delete/<post_key>', methods=['DELETE'])
def delete_post(post_id, post_key):
    with data_access_lock:
        if post_id not in post_storage or post_storage[post_id]['key'] != post_key:
            return jsonify(error='Invalid post ID or key.'), 403

        deleted_post = post_storage.pop(post_id)
    return jsonify({k: v for k, v in deleted_post.items() if k != 'key'}), 200

# Endpoint to get posts within a certain date range
@app.route('/posts', methods=['GET'])
def get_posts_within_range():
    # Your implementation here

# Endpoint to get posts by a specific user
@app.route('/posts/user/<username>', methods=['GET'])
def get_posts_by_username(username):
    # Your implementation here

# Endpoint for fulltext search in posts
@app.route('/posts/search', methods=['GET'])
def search_in_posts():
    # Your implementation here

# Additional code and endpoints as needed

if __name__ == '__main__':
    app.run(debug=True)
