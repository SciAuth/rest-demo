from flask import Flask, jsonify, request

app = Flask(__name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]
expenses = [
  { 'description': 'pizza', 'amount': 50 }
]


@app.route('/incomes')
def get_incomes():
  return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
  incomes.append(request.get_json())
  return '', 204

@app.route('/expenses')
def get_expenses():
  return jsonify(expenses)


@app.route('/expenses', methods=['POST'])
def add_expense():
  expenses.append(request.get_json())
  return '', 204