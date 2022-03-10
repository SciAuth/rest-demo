"""Python Flask RESTful APIs with Auth0 & SciAuth integration
"""
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from utils.auth0_decorator import requires_auth, requires_scope
from utils.AuthError import AuthError
from utils.scitokens_protect import protect

app = Flask(__name__)

# Create sample data
incomes = [{"description": "salary", "amount": 5000}]
expenses = [{"description": "pizza", "amount": 50}]

""" 
Expense could be accessed without authorization --> no token verification needed
"""


@app.route("/expenses/public", methods=["GET"])
def get_expenses():
    return jsonify(expenses)


@app.route("/expenses/public", methods=["POST"])
def add_expense():
    expenses.append(request.get_json())
    return "", 204


@app.route("/expenses/public", methods=["PUT"])
def replace_expense():
    expenses.clear()
    expenses.append(request.get_json())
    return "", 204


@app.route("/expenses/public", methods=["DELETE"])
def remove_expense():
    expenses.pop()
    return "", 204


"""
Income should be accessed with authorization --> auth0 decorator added for each method
"""


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route("/incomes/private", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_incomes():
    return jsonify(incomes)


@app.route("/incomes/private", methods=["POST"])
@requires_auth
def add_income():
    incomes.append(request.get_json())
    return "", 204


# TODO: #4 let user change specific item rather than delete the whole list
@app.route("/incomes/private", methods=["PUT"])
@requires_auth
def replace_income():
    incomes.clear()
    incomes.append(request.get_json())
    return "", 204


# TODO: #5 add scope for other actions
@app.route("/incomes/private", methods=["DELETE"])
@requires_auth
def remove_income():
    # Delete operation requires different scope's permission
    if requires_scope("delete:income"):
        incomes.pop()
        return "", 204
    raise AuthError(
        {
            "code": "Unauthorized",
            "description": "You don't have access to this resource",
        },
        403,
    )


"""
Properties should be accessed with authorization from SciToken
"""
properties = [{"car": 2000, "house": 100000}]


@app.route("/properties", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@protect(
    audience="https://demo.scitokens.org",
    issuer=["https://demo.scitokens.org"],
)
def get_properties():
    return jsonify(properties)


# TODO:let #6 user delete a specific item rather than the earliest item being added
@app.route("/properties", methods=["DELETE"])
@protect(
    audience="https://demo.scitokens.org",
    scope="delete:/properties",
    issuer=["https://demo.scitokens.org"],
)
def remove_properties():
    properties.pop()
