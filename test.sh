#!/bin/bash
python3 app.py &
APP_PID=$!

# Run Postman collections with Newman
newman run forum_multiple_posts.postman_collection.json -e env.json
newman run forum_post_read_delete.postman_collection.json -e env.json

kill APP_PID=$!

echo "Tests completed."

# Exit
exit 0
