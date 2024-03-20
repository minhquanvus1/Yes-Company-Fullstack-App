import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from typing import List

AUTH0_DOMAIN = 'dev-tioi4bnfisc6bcli.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'https://yesCompany/api'

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header() -> str:
    print('from auth.py')
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
    auth_header: str = request.headers['Authorization']
    print(f'auth_header: {auth_header}')
    header_parts: List = auth_header.split(' ')
    if len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    token = header_parts[1]
    return token

def check_permissions(permission, payload) -> bool:
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'forbidden',
            'description': 'Permission not found.'
        }, 403)
    return True

def verify_decode_jwt(token) -> dict:
    print('inside verify_decode_jwt')
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
        print(f'unverified_header: {unverified_header}')
    except jwt.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Error decoding header.'
        }, 400)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    rsa_key = {}
    for each_jwk in jwks['keys']:
        if each_jwk['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': each_jwk['kty'],
                'kid': each_jwk['kid'],
                'use': each_jwk['use'],
                'n': each_jwk['n'],
                'e': each_jwk['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token is expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                print('inside requires_auth_decorator')
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as e:
                print(f'Error: {e.error}')
                print(f'Status Code: {e.status_code}')
                raise e
            except Exception as e:
                print(f'Error: {e}')
                abort(500)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator