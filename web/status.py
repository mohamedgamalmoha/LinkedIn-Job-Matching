from http import HTTPStatus as PyHTTP


class HTTPStatus:
    OK: int = PyHTTP.OK.value  # 200
    CREATED: int = PyHTTP.CREATED.value  # 201
    BAD_REQUEST: int = PyHTTP.BAD_REQUEST.value  # 400
    UNAUTHORIZED: int = PyHTTP.UNAUTHORIZED.value  # 401
    FORBIDDEN: int = PyHTTP.FORBIDDEN.value  # 403
    NOT_FOUND: int = PyHTTP.NOT_FOUND.value  # 404
    CONFLICT: int = PyHTTP.CONFLICT.value  # 409
