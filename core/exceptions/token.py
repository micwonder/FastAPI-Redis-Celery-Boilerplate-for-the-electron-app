from core.exceptions import CustomException

class DecodeTokenException(CustomException):
    code = 401
    success = False
    message = "Error: token decode error."


class ExpiredTokenException(CustomException):
    code = 401
    success = False
    message = "Error: token expired."
