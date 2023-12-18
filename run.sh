#!/bin/sh

export FLASK_APP=app.py  # replace with your Flask app file name
export FLASK_ENV=development
exec flask run
