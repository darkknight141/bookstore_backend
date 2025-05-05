from api.exceptions import BaseServiceException


class AlreadyExistsException(BaseServiceException):
    detail = 'User already exists.'


class UserDoesNotExistException(BaseServiceException):
    detail = 'User does not exist.'


class InvalidPasswordException(BaseServiceException):
    detail = 'Invalid password.'
