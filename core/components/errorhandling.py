"""
    This component implements our standardized error object
"""

from rest_framework import status
from rest_framework.response import Response
from enum import Enum, unique


class ErrorHandling:
    @staticmethod
    def get_response(
        component, http_status, error_code, message, extra_info: dict = None
    ):
        """
        OUR SUPPORTED ERROR CODES:

        400 Bad Request - ValidationError(APIException)
        This response means that server could not understand the request
        due to invalid syntax.

        401 Unauthorized - raise NotAuthenticated(APIException)
        Although the HTTP standard specifies "unauthorized",
        semantically this response means "unauthenticated". That is,
        the client must authenticate itself to get the requested response.

        403 Forbidden - raise PermissionDenied(APIException)
        The client does not have access rights to the content,
        i.e. they are unauthorized, so server is rejecting to give proper
        response. Unlike 401, the client's identity is known to the server.

        404 Not Found - raise MethodNotAllowed(APIException)
        The server can not find requested resource.
        In the browser, this means the URL is not recognized.
        In an API, this can also mean that the endpoint is valid but
        the resource itself does not exist. Servers may also send this
        response instead of 403 to hide the existence of a resource from
        an unauthorized client. This response code is probably the most
        famous one due to its frequent occurrence on the web.

        500 Internal Server Error - status.HTTP_500_INTERNAL_SERVER_ERROR
        The server has encountered a situation it doesn't know how to handle.
        """

        http_status = str(http_status)
        error_code = str(error_code)
        response_value = None
        if http_status == "403" or http_status == "401":
            response_value = Response(
                {
                    "http_status_code": "403",
                    "message": message,
                    "component_on_error": component,
                    "error_code": error_code,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        elif http_status == "404":
            response_value = Response(
                {
                    "http_status_code": "404",
                    "message": message,
                    "component_on_error": component,
                    "error_code": error_code,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        elif http_status == "413":
            response_value = Response(
                {
                    "http_status_code": "413",
                    "message": message,
                    "component_on_error": component,
                    "error_code": error_code,
                },
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )
        elif http_status == "400" or http_status[0] == "4":
            response_value = Response(
                {
                    "http_status_code": "400",
                    "message": message,
                    "component_on_error": component,
                    "error_code": error_code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            response_value = Response(
                {
                    "http_status_code": http_status,
                    "message": message,
                    "component_on_error": component,
                    "error_code": error_code,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if extra_info is not None:
            response_value.data["extra_info"] = extra_info
        return response_value


@unique
class ErrorCode(Enum):
    """
    OUR SUPPORTED BUSINESS LOGIC/INTERNAL ERROR CODES
    """

    # HTTP errors
    ERROR_HTTP_400_BAD_REQUEST = "400"
    ERROR_HTTP_401_UNAUTHORIZED = "401"
    ERROR_HTTP_403_FORBIDDEN = "403"
    ERROR_HTTP_404_NOT_FOUND = "404"
    ERROR_HTTP_409_CONFLICT = "409"
    ERROR_HTTP_413_REQUEST_ENTITY_TOO_LARGE = "413"
    ERROR_HTTP_500_INTERNAL_SERVER_ERROR = "500"

    # Common logical errors
    ERROR_INVALID_OR_MISSING_ARGS_8001 = "8001"

    def __str__(self):
        return self.value
