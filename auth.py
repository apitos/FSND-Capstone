import json
from flask import request, _request_ctx_stack, session, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

import http.client


AUTH0_DOMAIN = 'capstone-app.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Capstone'

conn = http.client.HTTPSConnection("AUTH0_DOMAIN")

payload = "{\"client_id\":\"J55VPnytALfjPqjrWdhWRGv7vVhRZH0R\",\"client_secret\":\"owGAefX8ykpoFyOtUTex1IFESQ2Y-_UXBnJp3tN2WXR-pEf3D1zguePy1buLK-ic\",\"audience\":\"Capstone\",\"grant_type\":\"client_credentials\"}"
# print (payload)
headers = {"content-type":"application/json"}
conn.request("POST", "/oauth/token", payload, headers)
res = conn.getresponse()
data = res.read()
data1 = data.decode("utf-8")
result = json.loads(data1)
access_token = result['access_token']

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    """

    auth ='Bearer {}'.format(access_token)

    #auth = request.headers.get('Authorization', None)

    if not auth:
        print('FAIL')
        print('auth_header is:', auth)
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    print (token)
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                    'Incorrect claims. Please, check the audience and issuer.'
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
            token = None
            if 'token' in session:
                token = session['token']
            else:
                token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator    