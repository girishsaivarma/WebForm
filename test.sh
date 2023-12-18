#!/bin/bash

# Source NVM in the current shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Use the correct Node.js version with NVM
nvm use 16

python3 app.py &
APP_PID=$!
python3 test.py

# Run Postman collections with Newman
newman run forum_multiple_posts.postman_collection.json -e env.json
newman run forum_post_read_delete.postman_collection.json -e env.json

kill $APP_PID

echo "Tests completed."

# Exit
exit 0
