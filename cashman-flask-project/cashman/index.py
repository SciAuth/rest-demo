"""Python Flask RESTful APIs with Auth0 & SciAuth integration
"""
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from utils.auth0_decorator import requires_auth, requires_scope
from utils.AuthError import AuthError
from utils.scitokens_protect import protect

app = Flask(__name__)

# Create sample data
incomes = {
    "yolanda": [{"description": "salary", "amount": 5000}],
    "linh": [{"description": "stock interest", "amount": 1000}],
}
expenses = {
    "yolanda": [{"description": "pizza", "amount": 50}],
    "linh": [{"description": "salad", "amount": 20}],
}

""" 
Expense could be accessed without authorization --> no token verification needed
"""


@app.route("/expenses/<string:Name>", methods=["GET"])
def get_expenses(Name):
    if Name in expenses:
        return jsonify(expenses[Name])
    return "", 204


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
def update_expense(Name):
    request_body = request.get_json()
    old_expense = request_body[0]
    new_expense = request_body[1]
    if Name in expenses:
        if old_expense in expenses[Name]:
            update_index = expenses[Name].index(old_expense)
            expenses[Name][update_index] = new_expense
        else:
            expenses[Name].append(new_expense)
    return "", 204


@app.route("/expenses/<string:Name>", methods=["DELETE"])
def remove_expense(Name):
    expense_to_delete = request.get_json()
    if Name in expenses and expense_to_delete in expenses[Name]:
            expenses[Name].remove(expense_to_delete)
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
    if requires_scope("read:incomes"):
        if Name in incomes:
            return jsonify(incomes[Name])
        return "", 204
    raise AuthError(
        {
            "code": "Unauthorized",
            "description": "You don't have permission to perform this action",
        },
        403,
    )


@app.route("/incomes/<string:Name>", methods=["POST"])
@requires_auth
def add_income(Name):
    if requires_scope("write:incomes"):
        new_income = request.get_json()
        if Name in incomes:
            incomes[Name].append(new_income)
        else:
            incomes[Name] = [new_income]
        return "", 204
    raise AuthError(
        {
            "code": "Unauthorized",
            "description": "You don't have permission to perform this action",
        },
        403,
    )


@app.route("/incomes/<string:Name>", methods=["PUT"])
@requires_auth
def update_income(Name):
    if requires_scope("update:incomes"):
        request_body = request.get_json()
        old_income = request_body[0]
        new_income = request_body[1]
        if Name in incomes:
            if old_income in incomes[Name]:
                update_index = incomes[Name].index(old_income)
                incomes[Name][update_index] = new_income
            else:
                incomes[Name].append(new_income)
        return "", 204
    raise AuthError(
        {
            "code": "Unauthorized",
            "description": "You don't have permission to perform this action",
        },
        403,
    )


@app.route("/incomes/<string:Name>", methods=["DELETE"])
@requires_auth
def remove_income(Name):
    if requires_scope("delete:incomes"):
        income_to_delete = request.get_json()
        if Name in incomes and income_to_delete in incomes[Name]:
            incomes[Name].remove(income_to_delete)
        return "", 204
    raise AuthError(
        {
            "code": "Unauthorized",
            "description": "You don't have permission to perform this action",
        },
        403,
    )


"""
Properties should be accessed with authorization from SciToken
"""
properties = {
    "yolanda": [
        {"description": "car", "amount": 2000},
        {"description": "house", "amount": 100000},
    ],
    "linh": [
        {"description": "truck", "amount": 5000},
        {"description": "condo", "amount": 70000},
    ],
}


@app.route("/properties/<string:Name>", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@protect(
    audience="https://demo.scitokens.org",
    permission="read",
    issuer=["https://demo.scitokens.org"],
)
def get_property(Name):
    if Name in properties:
        return jsonify(properties[Name])
    return "", 204


@app.route("/properties/<string:Name>", methods=["POST"])
@protect(
    audience="https://demo.scitokens.org",
    permission="write",
    issuer=["https://demo.scitokens.org"],
)
def add_property(Name):
    new_property = request.get_json()
    if Name in properties:
        properties[Name].append(new_property)
    else:
        properties[Name] = [new_property]
    return "", 204


@app.route("/properties/<string:Name>", methods=["PUT"])
@protect(
    audience="https://demo.scitokens.org",
    permission="update",
    issuer=["https://demo.scitokens.org"],
)
def update_property(Name):
    request_body = request.get_json()
    old_property = request_body[0]
    new_property = request_body[1]
    if Name in properties:
        if old_property in properties[Name]:
            update_index = properties[Name].index(old_property)
            properties[Name][update_index] = new_property
        else:
            properties[Name].append(new_property)
    return "", 204


@app.route("/properties/<string:Name>", methods=["DELETE"])
@protect(
    audience="https://demo.scitokens.org",
    permission="delete",
    issuer=["https://demo.scitokens.org"],
)
def remove_property(Name):
    property_to_delete = request.get_json()
    if Name in properties and property_to_delete in properties[Name]:
        properties[Name].remove(property_to_delete)
    return "", 204
