import datetime

import iso8601
from django.contrib.auth import logout
from django.contrib.auth.middleware import AuthenticationMiddleware
from pytz import utc


class Auth0Middleware(AuthenticationMiddleware):
    '''Django API Key authentication Middleware'''

    def process_request(self, request):
        expires = request.session.get('expires', None)
        if expires is None:
            return

        expires_date = iso8601.parse_date(expires)
        if expires_date < utc.localize(datetime.datetime.now()):
            del request.session['auth']
            logout(request)
