
import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
"""
Get Token from header
Reads Authorization from the request header, checks if a Bearer Token is attached, splits the Ttken itself from the "Bearer" title and returns this
"""
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if auth is None:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)
    
    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with 'Bearer'."
        }, 401)
    
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found."
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"
        }, 401)

    return parts[1]

"""
Verify and Decode JWTs
Checks if the key is in the well-known jwk json and then decodes the JWT in order to return this
"""
def verify_decode_jwt(token):
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in json.loads(urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json").read())['keys']:
        """
        Verify JWT
        """
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
            """
            Decode JWT
            """
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                "code": "token_expired",
                "description": "Token expired"
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                "code": "invalid_claims",
                "description": "Incorrect claims, check the audience and issuer"
            }, 401)
            
        except Exception:
            raise AuthError({
                "code": "invalid_header",
                "description": "Unable to parse authentication token."
            }, 401)

    raise AuthError({
        "code": "invalid_header",
        "description": "Unable to find appropriate key"
    }, 401)

"""
Check permissions
Raises AuthError if "permissions" isn't in payload and the if the required permission is in the permissions payload
"""
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            "code": "permissions_missing_in_payload",
            "description": "Permissions expected in payload"
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            "code": "not_authorized",
            "description": "Permission not found"
        }, 401)
    return True

"""
Requires Auth
- Get the token form request header
- Verify and Decode JWT
- Check given permission
"""
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
