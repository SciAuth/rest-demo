from flask import Flask, jsonify, request

app = Flask(__name__)

# /server.py
#from flask import redirect
#from flask import render_template
#from flask import session
#from flask import url_for
from authlib.integrations.flask_client import OAuth
#from six.moves.urllib.parse import urlencode

#import constants

import json
from functools import wraps

from flask import _request_ctx_stack
from flask_cors import CORS, cross_origin
#from flask_cors import cross_origin
from jose import jwt
from six.moves.urllib.request import urlopen

AUTH0_DOMAIN = 'dev-7jgsf20u.us.auth0.com'
API_IDENTIFIER = 'https://cashman/api'
ALGORITHMS = ["RS256"]

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]
expenses = [
  { 'description': 'pizza', 'amount': 50 }
]


@app.route('/incomes/private')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_incomes():
  return jsonify(incomes)


@app.route('/incomes/private', methods=['POST'])
#@requires_auth
def add_income():
  incomes.append(request.get_json())
  return '', 204

@app.route('/incomes/private', methods=['PUT'])
#@requires_auth
def replace_income():
  incomes.clear()
  incomes.append(request.get_json())
  return '', 204

@app.route('/incomes/private-scoped', methods=['DELETE'])
@requires_auth
def remove_income():
    if requires_scope("read:messages"):
        incomes.pop()
        return '', 204
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)

@app.route('/expenses/public')
def get_expenses():
  return jsonify(expenses)


@app.route('/expenses/public', methods=['POST'])
def add_expense():
  expenses.append(request.get_json())
  return '', 204

@app.route('/expenses/public', methods=['PUT'])
def replace_expense():
  expenses.clear()
  expenses.append(request.get_json())
  return '', 204

@app.route('/expenses/public', methods=['DELETE'])
def remove_expense():
  expenses.pop()
  return '', 204

# This doesn't need authentication
# @APP.route("/api/public")
# @cross_origin(headers=["Content-Type", "Authorization"])
# def public():
#     response = "Hello from a public endpoint! You don't need to be authenticated to see this."
#     return jsonify(message=response)

# # This needs authentication
# @APP.route("/api/private")
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
# def private():
#     response = "Hello from a private endpoint! You need to be authenticated to see this."
#     return jsonify(message=response)

# # This needs authorization
# @APP.route("/api/private-scoped")
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
# def private_scoped():
#     if requires_scope("read:messages"):
#         response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
#         return jsonify(message=response)
#     raise AuthError({
#         "code": "Unauthorized",
#         "description": "You don't have access to this resource"
#     }, 403)