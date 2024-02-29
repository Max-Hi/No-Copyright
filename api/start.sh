#!/bin/bash -x
HOST=10.8.0.1
PORT=5500
export FLASK_ENV=development
export FLASK_APP=api.py
read -p 'Username: ' username
export USERNAME=$username
read -sp 'Password: ' password
export PASSWORD=$password
flask run --host=$HOST --port=$PORT
