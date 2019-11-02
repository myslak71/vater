"""API request decorator module."""
import functools
import inspect
from typing import Callable, List, Optional, Tuple, Type, Union

from vater.models import Subject
from vater.request_types import RequestType


def api_request(
    url_pattern: str,
    handler_class: Type[RequestType],
    *,
    validators: Optional[dict] = None,
    **kwargs
) -> Callable:
    """Initialize request handler."""
    handler = handler_class(url_pattern=url_pattern, validators=validators, **kwargs)

    def decorator_api_request(func: Callable) -> Callable:
        """Allow passing arguments."""

        @functools.wraps(func)
        def wrapper_api_request(
            *args: tuple, **kwargs: dict
        ) -> Union[Tuple[bool, str], Tuple[Union[Subject, List[Subject]], str]]:
            """Return handler result."""
            arg_spec = inspect.getfullargspec(func)

            params: dict = {
                "client": args[0],
                **kwargs,
                **{
                    key: value
                    for key, value in zip(arg_spec.args, args)
                    if key != "self"
                },
            }

            # add not present keywords with their default value
            for param in arg_spec.kwonlyargs:
                if param not in kwargs and param != "self":
                    params[param] = arg_spec.kwonlydefaults[param]

            handler.register_params(**params)

            return handler.result()

        return wrapper_api_request

    return decorator_api_request
