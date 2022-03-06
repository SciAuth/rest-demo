"""Python Flask RESTful API Auth0 integration example
"""
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from cashman.auth0_decorator import AuthError, requires_auth, requires_scope

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


@app.route("/incomes/private", methods=["PUT"])
@requires_auth
def replace_income():
    incomes.clear()
    incomes.append(request.get_json())
    return "", 204


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
