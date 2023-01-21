import scitokens
from functools import wraps
from flask import request
import traceback
import inspect

audiences = ["https://demo.scitokens.org", "https://token-issuer.localdomain"]
issuers = ["https://demo.scitokens.org", "https://token-issuer.localdomain"]

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
            myAudience = None
            parsedToken = None
            exception = None
            exeTrace = ""
            for audience in audiences:
                try:
                    # method 1: insecure -> True
                    # method 2: public_key -> Get public key and test in deserialize
                    # + normally would be fetched from token issuer, but just code in
                    # In configuration for demo, check public_key as well
                    parsedToken = scitokens.SciToken.deserialize(serialized_token, audience)
                    myAudience = audience
                    break
                except Exception as e:
                    exception = e
                    exeTrace = traceback.format_exc()
                    continue
            
            # Check if found valid audience
            if not myAudience:
                print(str(exception))
                traceback.print_exc() # TODO: Not too sure how to handle this. Maybe format_exc?
                headers = {"WWW-Authenticate": "Bearer"}
                return ("Unable to deserialize: %{}".format(str(exception)), 401, headers)

            # if not isinstance(issuers, list):
            #     issuers = [issuers]
            success = False
            permission = outer_kwargs["permission"]
            path = request.path
            for issuer in issuers:
                enforcer = scitokens.Enforcer(issuer, myAudience)
                if enforcer.test(parsedToken, permission, path):
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
                kwargs["token"] = parsedToken

            return some_function(*args, **kwargs)

        return wrapper

    return real_decorator
