# RESTful Demo App for Web Token Authorizations

A demo app with simple REST APIs that uses [Auth0](https://auth0.com/) and [SciTokens](https://scitokens.org/) to authorize access to the API endpoints

## Installation

### Cloning this repo

You can clone this repository by using:

```bash
$ git clone git@github.com:SciAuth/rest-demo.git
```

### Installing Flask

First and foremost, make sure that your local machine is installed with Python 3, Pip, and Flask. If you are not sure, check to see if everything is set up as expected:

```bash
$ python3 --version
# Python 3.9.10
```

```bash
$ pip3 --version
# pip 22.0.3
```

```bash
$ flask --version
# Python 3.9.10
# Flask 2.0.3
# Werkzeug
```

If you have never developed a Flask application before, high chance you haven't had it yet. The installation is quite simple

```bash
# you might need to use pip3 instead of pip
$ pip install Flask
```

### Installing Pre-requisites

To manage our project's dependencies (with specific versions) without messing up with the system's global packages, we are going to use [`pipenv`](https://github.com/pypa/pipenv) instead of `pip`.

> Pipenv is a dependency manager that isolates projects on private environments, allowing packages to be installed per project

```bash
$ pip install pipenv
```

The prerequisites for this app are located on `Pipfile` and `Pipfile.lock`.

> The `Pipfile` specifies packages requirements for a Python application or library to development and execution.

> The `Pipfile.lock` specifies the version of the packages present in Pipfile to be used. It eliminates the risk of automatically upgrading packages that depend upon each other and break of the project dependency tree.

You can manually install each of them or run:

```bash
$ pipenv install --dev
```

## Running locally

To run this app on your local server, direct to the `cashman-flask-project` folder to facilitate the start up of our application:

```bash
$ cd cashman-flask-project
$ chmod +x bootstrap.sh
$ ./bootstrap.sh
```

This will first defines the main script (`index.py`) to be executed by Flask, then activate a virtual environment by `pipenv` that locates exact versions of our dependencies, then run our Flask app.

If the script is working properly, you should expect to see a result similar to this:

```bash
# * Serving Flask app './cashman/index.py' (lazy loading)
# * Environment: production
#   WARNING: This is a development server. Do not use it in a production deployment.
#   Use a production WSGI server instead.
# * Debug mode: off
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Description

The app provides 3 different REST APIs that allow [standard HTTP method requests](https://restfulapi.net/http-methods/) `GET`, `POST`, `PUT`, `DELETE`. Each API is built with different authorization scopes:

- `/expenses` is a public endpoint that requires no authorization.
- `/incomes` is a private endpoint authorized with [Auth0](https://auth0.com/) tokens with static scopes.
- `/properties` is a private endpoint authorized with [SciTokens](https://scitokens.org/) tokens with dynamic scopes.

**_We have defined our own API to configure Auth0 authorization following [this tutorial](https://auth0.com/docs/quickstart/backend/python) on Auth0 website._**

## Getting tokens

## Usage

There are two ways to test our app, you can use [Postman](https://www.postman.com/) – a platform for building and testing APIs and testing or [`curl`](https://curl.se/) command-line tool. Here we will show how we test our

### Test `/expenses` API

This is a public endpoint, thus to test all 4 HTTP methods are working properly, we simple invoke `curl` calls.

**GET**

```bash
$ curl --request GET \
  --url http://127.0.0.1:5000/expenses/linh
```

Response

```
[{"amount":20,"description":"salad"}]
```

**POST**

```bash

```

Response

```

```

**PUT**

```bash

```

Response

```

```

**DELETE**

```bash

```

Response

```

```

### Test `/incomes` API

To test this endpoint, we first need to ask Auth0 for authorized tokens by issuing the following API call:

```bash
$ curl --request POST \
  --url https://dev-7jgsf20u.us.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"MXzwZEYbHMFlJZWpfNjSFWttW0xq16JT","client_secret":"DjItEcgIhsFK6ma0rr3dgc-cMcuH1nMfRVSl181VNU3eiMh5_SlV9XcPwIJqb7c5","audience":"https://cashman/api","grant_type":"client_credentials"}'
```

We previously allowed these following scopes from our Auth0 dashboard:

![Auth0 scopes](Auth0_scopes.png)

Thus, if the above request is successful, you should expect to get something similar to this response:

```
{
    "access_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im85Z2FhelRrM0tHVzJvU1g5VlpaaiJ9.eyJpc3MiOiJodHRwczovL2Rldi03amdzZjIwdS51cy5hdXRoMC5jb20vIiwic3ViIjoiTVh6d1pFWWJITUZsSlpXcGZOalNGV3R0VzB4cTE2SlRAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vY2FzaG1hbi9hcGkiLCJpYXQiOjE2NDgxMTI1MTgsImV4cCI6MTY0ODE5ODkxOCwiYXpwIjoiTVh6d1pFWWJITUZsSlpXcGZOalNGV3R0VzB4cTE2SlQiLCJzY29wZSI6InJlYWQ6aW5jb21lcyB3cml0ZTppbmNvbWVzIGRlbGV0ZTppbmNvbWVzIHVwZGF0ZTppbmNvbWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.oxnL0kRhhczd8utKvYjjRw79mxdGKjKE_qviyR44Au8AFzVB-J4tu5CFXWzRoWajsKc1fPha32pt2s3v39bu5OUmmSLS_Zd4V4SvxmBvzHYdhJk2QY37GpHpgaPGwZst6M6YjMh0XxChFHxab_GxbAe__H5ZK8UBUCD09LuJWS-IjF4Wa5pl1vJP-dAkOf5aTCA9kqxZTTbcnDbJXOi2QAW5RTGY-dLQQAQDHU04EtFyBB4tIHqJBAX2mtdSpFnAxiIJOgopk3yaDItPHl_--5c_4uZq1lZ81e76I5tyFt0jJllJij8QSQribeHWp5CAzjhJe0v-MrZXO6WbUnJZ6g",
    "scope":"read:incomes write:incomes delete:incomes update:incomes"
    "expires_in":86400,
    "token_type":"Bearer"}
```

To inspect this token, you can decode it at [jwt.io](https://jwt.io/):

![JWT debug](jwt_debug.png)

You can now extract the `access_token `property from the response to make to create a `bearer token` with an `Authorization Header` in your request to obtain authorized access to your API.

**GET**

```bash
$ curl --request GET \
  --url http://127.0.0.1:5000/incomes/linh \
  --header 'authorization: Bearer <access_token>'
```

**Response**

```
[{"amount":1000,"description":"stock interest"}]
```

### Test `/properties` API

To test this endpoint, we first need to ask SciTokens for authorized tokens for our request. Go to https://demo.scitokens.org/ to generate your sample SciTokens. You can edit the payload of the SciToken on the left to serve your tests, such as adding new scope. You can also add multiple scopes for the tokens, separated by a single space.

For example the below token is used to authorize permission for all methods on `/properties/linh` endpoint. However, this token shouldn't work if we use it to request `/properties/yolanda`.

![](scitoken_generator.png)

You now can copy the encoded token on the right for your API call.

**GET**

```bash
$ curl --request GET \
  --url http://127.0.0.1:5000/properties/linh \
  --header 'authorization: Bearer <your_sample_token>'
```

**Response**

```
[{"amount":5000,"description":"truck"},{"amount":70000,"description":"condo"}]
```

**POST**

```bash

```

Response

```

```

**PUT**

```bash

```

Response

```

```

**DELETE**

```bash

```

Response

```

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author & Contacts

[Linh Tang](mailto:tanglinh@grinnell.edu) - SciAuth Fellow Spring 2022

[Yolanda Jiang](mailto:jianghui@grinnell.edu) - SciAuth Fellow Spring 2022
