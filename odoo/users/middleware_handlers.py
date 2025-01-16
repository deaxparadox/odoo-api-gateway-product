from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import AccessToken

def custom_exception_handler(exc, context):
    print(exc, context)
    response = exception_handler(exc, context)

    if isinstance(exc, (TokenError, InvalidToken)):
        return Response({"error": "Access token has expired"}, status=401)

    return response


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware