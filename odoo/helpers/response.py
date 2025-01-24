from rest_framework.response import Response

def api_error_response(message: list[str], status, /):
    return Response({"Error": message()}, status=status)


def api_message_response(message: list[str], status, /):
    if callable(message):
        return Response({"Message": message()}, status=status)
    return Response({"Message": message}, status=status)