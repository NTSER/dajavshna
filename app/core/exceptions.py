from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse


class DajavshnaException(Exception):
    """Base exception for all exceptions in Dajavsha APP"""

    status = status.HTTP_404_NOT_FOUND


class EntityNotFound(DajavshnaException):
    """Entity not found in database"""

    status = status.HTTP_400_BAD_REQUEST


class ClientNotAuthorized(DajavshnaException):
    """Client is not authorized to perform the action"""

    status = status.HTTP_401_UNAUTHORIZED


class BadCredentials(DajavshnaException):
    """Bad credentials"""

    status = status.HTTP_401_UNAUTHORIZED


class InvalidToken(DajavshnaException):
    """Access token is invalid or expired"""

    status = status.HTTP_401_UNAUTHORIZED


class EmailAlreadyRegistered(DajavshnaException):
    """Email is already registered"""

    status = status.HTTP_406_NOT_ACCEPTABLE


class AccountNotVerified(DajavshnaException):
    """Account is not verified"""

    status = status.HTTP_401_UNAUTHORIZED


def _get_handler(status_code: int, detail: str | None):
    def handler(request: Request, exception: Exception):
        raise HTTPException(status_code=status_code, detail=detail)

    return handler


def add_exception_handlers(app: FastAPI):
    for subclass in DajavshnaException.__subclasses__():
        app.add_exception_handler(
            subclass, _get_handler(status_code=subclass.status, detail=subclass.__doc__)
        )

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    def internal_server_error(request, exception):
        return JSONResponse(
            content={"detail": "Something went wrong"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={"X-Error": f"{exception}"},
        )
