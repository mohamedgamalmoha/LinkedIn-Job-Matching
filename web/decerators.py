import inspect
from functools import wraps, partial
from typing import Any, Sequence, Union, Callable

from flask import current_app
from flask_jwt_extended import verify_jwt_in_request


LocationType = Union[str, Sequence, None]


# Modified version of the original jwt_required function to allow authentication for async endpoints
# It follows the same logic as original
def jwt_required_v2(func: Callable = None, optional: bool = False, fresh: bool = False, refresh: bool = False,
                    locations: LocationType = None, verify_type: bool = True) -> Any:
    """
     A decorator to protect a Flask endpoint with JSON Web Tokens.

     Any route decorated with this will require a valid JWT to be present in the
     request (unless optional=True, in which case no JWT is also valid) before the
     endpoint can be called.

     :param func:
        Endpoint function that needs to be verified. Defaults to None

     :param optional:
         If ``True``, allow the decorated endpoint to be accessed if no JWT is present in
         the request. Defaults to ``False``.

     :param fresh:
         If ``True``, require a JWT marked with ``fresh`` to be able to access this
         endpoint. Defaults to ``False``.

     :param refresh:
         If ``True``, requires a refresh JWT to access this endpoint. If ``False``,
         requires an access JWT to access this endpoint. Defaults to ``False``.

     :param locations:
         A location or list of locations to look for the JWT in this request, for
         example ``'headers'`` or ``['headers', 'cookies']``. Defaults to ``None``
         which indicates that JWTs will be looked for in the locations defined by the
         ``JWT_TOKEN_LOCATION`` configuration option.

     :param verify_type:
         If ``True``, the token type (access or refresh) will be checked according
         to the ``refresh`` argument. If ``False``, type will not be checked and both
         access and refresh tokens will be accepted.
     """

    if func is None:
        return partial(jwt_required_v2, optional=optional, fresh=fresh, refresh=refresh, locations=locations,
                       verify_type=verify_type)

    @wraps(func)
    async def wrap_func(*args, **kwargs):
        verify_jwt_in_request(optional, fresh, refresh, locations, verify_type)
        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return current_app.ensure_sync(func)(*args, **kwargs)
    return wrap_func
