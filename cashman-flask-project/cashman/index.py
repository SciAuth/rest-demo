"""Python Flask RESTful APIs with Auth0 & SciAuth integration
"""
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from utils.auth0_decorator import requires_auth, requires_scope
from utils.AuthError import AuthError
from utils.scitokens_protect import protect

app = Flask(__name__)

# Create sample data
incomes = {"yolanda": [{"description": "salary", "amount": 5000}]}
expenses = {"yolanda": [{"description": "pizza", "amount": 50}]}

""" 
Expense could be accessed without authorization --> no token verification needed
"""


@app.route("/expenses/<string:Name>", methods=["GET"])
def get_expenses(Name):
    return jsonify(expenses[Name])


@app.route("/expenses/<string:Name>", methods=["POST"])
def add_expense(Name):
    new_expense = request.get_json()
    if Name in expenses:
        expenses[Name].append(new_expense)
    else:
        expenses[Name] = [new_expense]
    return "", 204


# input should be in the format '[{}, {}]'
@app.route("/expenses/<string:Name>", methods=["PUT"])
def replace_expense(Name):
    input_content = request.get_json()
    print(input_content)
    old_expense = input_content[0]
    new_expense = input_content[1]
    if Name in expenses:
        if old_expense in expenses[Name]:
            replace_index = expenses[Name].index(old_expense)
            expenses[replace_index] = new_expense
        else:
            expenses[Name].append(new_expense)
    return "", 204


@app.route("/expenses/<string:Name>", methods=["DELETE"])
def remove_expense(Name):
    delete_content = request.get_json()
    if Name in expenses:
        if delete_content in expenses[Name]:
            expenses[Name].remove(delete_content)
    return "", 204


"""
Income should be accessed with authorization --> auth0 decorator added for each method
"""


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route("/incomes/<string:Name>", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_incomes(Name):
    scope = "get:" + "/incomes/" + Name
    if requires_scope(scope):
        return jsonify(incomes[Name])
    return ""


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
