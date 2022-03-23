import scitokens
from functools import wraps
from flask import request
import traceback
import inspect

audience = "https://demo.scitokens.org"
issuers = ["https://demo.scitokens.org"]


def protect(**outer_kwargs):
    def real_decorator(some_function):
        @wraps(some_function)
        def wrapper(*args, **kwargs):
            if "Authorization" not in request.headers:
                headers = {"WWW-Authenticate": "Bearer"}
                return ("No Authentication Header", 401, headers)

            bearer = request.headers.get("Authorization")
            if len(bearer.split()) != 2:
                headers = {"WWW-Authenticate": "Bearer"}
                return ("Authentication header incorrect format", 401, headers)

            serialized_token = bearer.split()[1]
            try:
                token = scitokens.SciToken.deserialize(serialized_token, audience)
            except Exception as e:
                print(str(e))
                traceback.print_exc()
                headers = {"WWW-Authenticate": "Bearer"}
                return ("Unable to deserialize: %{}".format(str(e)), 401, headers)

            # if not isinstance(issuers, list):
            #     issuers = [issuers]
            success = False
            permission = outer_kwargs["permission"]
            path = request.path
            for issuer in issuers:
                enforcer = scitokens.Enforcer(issuer, audience)
                if enforcer.test(token, permission, path):
                    success = True
                    break

            if not success:
                headers = {"WWW-Authenticate": "Bearer"}
                return (
                    "Validation incorrect: {}".format(enforcer.last_failure),
                    403,
                    headers,
                )

            # If the function takes "token" as an argument, send the token
            if "token" in inspect.getfullargspec(some_function).args:
                kwargs["token"] = token

            return some_function(*args, **kwargs)

        return wrapper

    return real_decorator
