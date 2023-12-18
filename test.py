

import unittest
import json
from server import forum_app  # Import the Flask app from server.py
from web_users import MemberManager, ForumMember  # Import the MemberManager and ForumMember from web_users.py

class TestMemberManager(unittest.TestCase):
    
    member_manager = MemberManager()
    # Placeholder for creating a new member and capturing valid_member_id and correct_user_key
    # This should be replaced with actual logic to create a member and capture their ID and key
    new_member = member_manager.register_member("new_user", "New User")
    valid_member_id = new_member.member_id
    correct_user_key = new_member.access_key
    def setUp(self):
            self.app = forum_app.test_client()  # Create a test client for the Flask app
            self.member_manager = MemberManager()

    def test_user_creation(self):
        # Test user creation
        response = self.app.post('/member', json={'member_name': 'testuser', 'full_name': 'Test User'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['member_name'].startswith('testuser'))

    def test_moderator_creation(self):
        # Test moderator creation
        response = self.app.post('/add_moderator',
                                headers={'Master-Key': 'admin_key'},
                                json={'member_name': 'newmod', 'full_name': 'New Mod'})
        self.assertEqual(response.status_code, 201)

    def test_user_auth(self):
        # Test user authentication
        valid_user = self.member_manager.register_member("authuser", "Auth User")
        response = self.app.get(f'/member/{valid_user.member_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['member_name'], 'testuser')

        # Add more test cases for user authentication here

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        forum_app.testing = True  # Use the forum_app from server.py
        self.app = forum_app.test_client()
        self.member_manager = MemberManager()

    def test_create_user_endpoint(self):
        # Test the create user endpoint
        response = self.app.post('/member', json={'member_name': 'testuser', 'full_name': 'Test User'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['member_name'], 'testuser')

    def test_create_moderator_endpoint(self):
        # Test the create moderator endpoint
        response = self.app.post('/add_moderator',
                                headers={'Master-Key': 'admin_key'},
                                json={'member_name': 'newmod', 'full_name': 'New Mod'})
        self.assertEqual(response.status_code, 201)

    def test_post_creation_endpoint(self):
        # Test post creation
        post_data = {'message': 'This is a test post'}
        response = self.app.post('/discussion', json=post_data)
        self.assertEqual(response.status_code, 200)

    def test_post_read_endpoint(self):
        # Test reading a post
        # Create a post then test reading that post
        post_data = {'message': 'Test Post for Reading'}
        create_response = self.app.post('/discussion', json=post_data)
        post_id = create_response.json['id']
        response = self.app.get(f'/discussion/{post_id}')
        self.assertEqual(response.status_code, 200)

    def test_post_delete_endpoint(self):
        # Create a post and get its ID and key
        post_data = {'message': 'Test Post for Deletion'}
        create_response = self.app.post('/discussion', json=post_data)
        post_id = create_response.json['id']
        key = create_response.json['key']

        # Delete the post
        delete_url = f'/discussion/{post_id}/remove/{key}'
        response = self.app.delete(delete_url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_endpoint(self):
        # Create a post and get its ID and key
        post_data = {'message': 'Test Post for Editing'}
        create_response = self.app.post('/discussion', json=post_data)
        post_id = create_response.json['id']
        key = create_response.json['key']

        # Edit the post
        edit_data = {'post_id': post_id, 'member_key': key, 'new_message': 'Edited Test Post'}
        edit_url = f'/discussion/{post_id}/edit'
        response = self.app.put(edit_url, json=edit_data)
        self.assertEqual(response.status_code, 200)

    def test_filter_posts_by_date_endpoint(self):
        # Test filtering posts by date
        post_data = {'message': 'Test Post for Filtering by Date'}
        create_response = self.app.post('/discussion', json=post_data)
        post_id = create_response.json['id']
        response = self.app.get(f'/discussions?year=2023')
        self.assertEqual(response.status_code, 200)

    def test_filter_posts_by_member_endpoint(self):
        # Test filtering posts by member
        post_data = {'message': 'Test Post for Filtering by Member'}
        create_response = self.app.post('/discussion', json=post_data)
        post_id = create_response.json['id']
        response = self.app.get(f'/discussions/member/{1}')  # Assuming a member with ID 1 exists
        self.assertEqual(response.status_code, 200)

    def test_update_user_profile_endpoint(self):
        # Test updating user profile
        update_data = {'user_key': 'user_key', 'new_real_name': 'Updated User'}
        response = self.app.put(f'/user/{1}/update', json=update_data)  # Assuming a user with ID 1 exists
        self.assertEqual(response.status_code, 200)

    def test_search_posts_endpoint(self):
        # Test searching for posts
        response = self.app.get('/posts/search?keyword=test')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
