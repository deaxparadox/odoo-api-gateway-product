from typing import Any, Callable
from rest_framework.response import Response
from abc import abstractmethod, ABC

def api_error_response(message: list | str | Callable, status, /):
    if callable(message):
        return Response({"Error": message()}, status=status)
    return Response({"Error": message}, status=status)


def api_message_response(message: list | str | Callable, status, /):
    if callable(message):
        return Response({"Message": message()}, status=status)
    return Response({"Message": message}, status=status)


# class Validator(ABC):
#     def __set_name__(self, owner, name):
#         self.private_name = "_" + name
#     def __get__(self, obj, objtype=None):
#         return getattr(obj, self.private_name)
#     def __set__(self, obj, value):
#         self.validate(value)
#         setattr(obj, self.private_name, value)
    
#     @abstractmethod
#     def validate(self, value):
#         pass

# class Message(Validator):
#     def validate(self, value):
#         if isinstance(value, (tuple, int, float, bool)):
#             raise TypeError(f"Expected value to be of type list, str, or dict")
            

# class ResponseTemplate:
#     message = Message()