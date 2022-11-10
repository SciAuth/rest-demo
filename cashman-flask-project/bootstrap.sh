#!/bin/sh
export FLASK_APP=./cashman/index.py
export AUTH0_DOMAIN=dev-7jgsf20u.us.auth0.com
export API_IDENTIFIER="https://cashman/api"
# source $(python3 -m pipenv --venv) /bin/activate

# Build steps: (note: venv should come with python module).  
# python3 -m venv cashman
# . cashman/bin/activate
flask run
