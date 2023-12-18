#!/bin/bash

# Install or update NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# Source NVM in the current shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  

# Install Node.js 16.x
nvm install 16

# Use Node.js 16.x
nvm use 16

# Install Newman
npm install -g newman

# Install datetime
pip3 install datetime

# Install secrets
pip3 install secrets


# Update pip and setup tools
pip3 install --upgrade pip setuptools
