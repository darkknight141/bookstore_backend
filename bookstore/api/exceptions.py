from starlette import status


class BaseServiceException(Exception):
    def __init__(self,
                 detail: str = "Произошла ошибка на сервере",
                 status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
                 ):
        self.detail = detail
        self.status_code = status_code


class ForbiddenException(BaseServiceException):
    def __init__(self, detail: str = "Отказано в доступе"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class NotAuthorizedException(BaseServiceException):
    def __init__(self, detail: str = "Не авторизован"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class ClientException(BaseServiceException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class NotFoundException(BaseServiceException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)
