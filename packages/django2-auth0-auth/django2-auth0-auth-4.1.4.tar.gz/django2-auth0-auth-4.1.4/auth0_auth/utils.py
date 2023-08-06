from base64 import urlsafe_b64decode, urlsafe_b64encode

import requests
from django.conf import settings
from jose import jwt
import logging

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


logger = logging.getLogger("auth0_auth")


DOMAIN = getattr(settings, "AUTH0_DOMAIN")
SCOPE = getattr(settings, "AUTH0_SCOPE", "openid email")
VERIFY_AT_HASH = getattr(settings, "AUTH0_VERIFY_AT_HASH", True)
RESPONSE_TYPE = getattr(settings, "AUTH0_RESPONSE_TYPE", "code")
CLIENT_ID = getattr(settings, "AUTH0_CLIENT_ID")
CLIENT_SECRET = getattr(settings, "AUTH0_CLIENT_SECRET")
SECRET_BASE64_ENCODED = getattr(settings, "AUTH0_SECRET_BASE64_ENCODED", False)
if SECRET_BASE64_ENCODED:
    try:
        CLIENT_SECRET = urlsafe_b64decode(CLIENT_SECRET)
    except TypeError as e:
        logger.debug(
            "Could not base64 decode client secret {}. Received error, {}.".format(
                CLIENT_SECRET, e.message
            )
        )


def get_jwt(code, redirect_uri):
    url = 'https://{domain}/oauth/token'.format(domain=DOMAIN)

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": urlsafe_b64encode(CLIENT_SECRET),
        "code": code,
        "redirect_uri": redirect_uri
    }

    return requests.post(url, json=data).json()


def decode_jwt(id_token):
    try:
        issuer = 'https://{domain}/'.format(domain=DOMAIN)
        url = 'https://{domain}/.well-known/jwks.json'.format(domain=DOMAIN)
        jwks = requests.get(url).json()

        return jwt.decode(id_token,
                          jwks,
                          algorithms=['RS256'],
                          audience=CLIENT_ID,
                          issuer=issuer,
                          options={'verify_at_hash': VERIFY_AT_HASH})
    except (jwt.JWTError, jwt.ExpiredSignatureError, jwt.JWTClaimsError,) as e:
        logger.debug(
            "Could not retrieve sub. Token validation error, {}".format(str(e))
        )


def get_login_url(
    domain=DOMAIN,
    scope=SCOPE,
    client_id=CLIENT_ID,
    redirect_uri=None,
    response_type=RESPONSE_TYPE,
    response_mode="form_post",
    state=None,
):
    param_dict = {
        "response_type": response_type,
        "response_mode": response_mode,
        "scope": scope,
        "client_id": client_id,
    }
    if redirect_uri is not None:
        param_dict["redirect_uri"] = redirect_uri
    if state is not None:
        param_dict["state"] = state
    params = urlencode(param_dict)
    return "https://{domain}/authorize?{params}".format(domain=domain, params=params)


def get_logout_url(redirect_uri, client_id=CLIENT_ID, domain=DOMAIN):
    params = urlencode({"returnTo": redirect_uri, "client_id": client_id})
    return "https://{domain}/v2/logout?{params}".format(domain=domain, params=params)


def get_email_from_token(payload):
    if "email" in payload:
        return payload["email"]
    elif "sub" in payload:
        return payload["sub"].split("|").pop()
    else:
        logger.debug(
            'Could not retrieve email. Token payload does not contain keys: "email" or "sub".'
        )
        return None


def is_email_verified_from_token(payload):
    return payload.get("email_verified", True)


def get_sub_from_token(payload):
    if "sub" in payload:
        return payload["sub"].replace("|",'.')
    else:
        logger.debug(
            'Could not retrieve sub. Token payload does not contain keys: "sub".'
        )
        return None
