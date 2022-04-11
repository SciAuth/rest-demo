#!/bin/sh
export FLASK_APP=./cashman/index.py
export AUTH0_DOMAIN=dev-7jgsf20u.us.auth0.com
source $(python3 -m pipenv --venv)/bin/activate
flask run
