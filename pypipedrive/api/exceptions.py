from typing import Any, Dict, Optional
from requests.status_codes import codes


V1 = "v1"
V2 = "api/v2"


class ApiException(Exception):

    code:            int = None  # HTTP status code.
    version:         str = None  # API version where the exception occurred.
    success:         Optional[bool] = None  # V1/V2
    error:           Optional[str] = None   # V1/V2
    error_info:      Optional[str] = None  # V1
    data:            Optional[Any] = None   # V1
    additional_data: Optional[Any] = None  # V1

    def __init__(
        self,
        code: int = None,
        version: str = None,
        error_response: Optional[Dict] = None):
        if code is not None:
            self.code = code
        else:
            if self.code is None:
                raise RuntimeError("HTTP status code must be provided to ApiException.")
        if version not in [V1, V2]:
            raise RuntimeError(f"Invalid API version: {version} (expected '{V1}'/'{V2}')")
        self.version = version
        error_response = error_response or {}
        self.success = error_response.get("success")
        self.error = error_response.get("error")
        if self.version == V1:
            self.error_info = error_response.get("error_info")
            self.data = error_response.get("data")
            self.additional_data = error_response.get("additional_data")
        super().__init__(self.message())

    def message(self) -> str:
        parts = [str(self.code)]
        if self.error:
            parts.append(self.error)
        if self.version == V1 and self.error_info:
            parts.append(f"(info: {self.error_info})")
        return " ".join(parts)


class BadRequestException(ApiException):
    """400 - like bad request / malformed payload."""
    code: int = 400


class UnauthorizedException(ApiException):
    """401 -  unauthorized error."""
    code: int = 401


class ForbiddenException(ApiException):
    """403 - forbidden error."""
    code: int = 403


class NotFoundException(ApiException):
    """404 - not found error."""
    code: int = 404


class MethodNotAllowedException(ApiException):
    """405 - method not allowed error."""
    code: int = 405


class ConflictException(ApiException):
    """409 - like conflict (duplicate, state conflict...)."""
    code: int = 409


class GoneException(ApiException):
    """410 - gone error."""
    code: int = 410


class ServerErrorException(ApiException):
    """500 - server error."""
    code: int = 500


def raise_from_error_response(
    code: int = None,
    version: str = None,
    error_response: Dict = None) -> None:
    """
    Inspect the API error payload and raise a specific exception when possible.
    Fallback: ApiException.

    Args:
        code: The HTTP status code from the API response.
        version: The API version where the error occurred.
        error_response: The error response payload from the API.
    Raises:
        ApiException: Specific exception based on the error response.
    """
    if not error_response:
        raise RuntimeError("No error response payload provided.")
    if code is None or not isinstance(code, int):
        raise RuntimeError("Invalid or missing HTTP status code.")
    if version not in [V1, V2]:
        raise RuntimeError(f"Invalid API version: {version} (expected '{V1}'/'{V2}')")

    if code == codes.bad_request:
        raise BadRequestException(version=version, error_response=error_response)
    elif code == codes.unauthorized:
        raise UnauthorizedException(version=version, error_response=error_response)
    elif code == codes.forbidden:
        raise ForbiddenException(version=version, error_response=error_response)
    elif code == codes.not_found:
        raise NotFoundException(version=version, error_response=error_response)
    elif code == codes.method_not_allowed:
        raise MethodNotAllowedException(version=version, error_response=error_response)
    elif code == codes.gone:
        raise GoneException(version=version, error_response=error_response)
    elif code == codes.conflict:
        raise ConflictException(version=version, error_response=error_response)
    elif code >= codes.server_error:
        raise ServerErrorException(version=version, error_response=error_response)
    # Fallback to general ApiException when no special case matched.
    raise ApiException(code=code, version=version, error_response=error_response)