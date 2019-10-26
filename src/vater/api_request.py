"""API request decorator module."""
import functools
import inspect
from typing import Callable, List, Tuple, Type, Union

from vater.models import Subject
from vater.request_types import RequestType


def api_request(
    url_pattern: str, handler_class: Type[RequestType], **kwargs
) -> Callable:
    """Decorate for api requests."""
    handler = handler_class(url_pattern=url_pattern, **kwargs)

    def decorator_api_request(func: Callable) -> Callable:
        """Allow passing arguments."""

        @functools.wraps(func)
        def wrapper_api_request(
            *args: tuple, **kwargs: dict
        ) -> Union[Tuple[bool, str], Tuple[Union[Subject, List[Subject]], str]]:
            """Fetch subject/subjects and request identifier from API."""
            signature = inspect.signature(func)

            # add not present keywords with their default value
            for parameter in signature.parameters:
                if parameter not in kwargs and parameter != "self":
                    kwargs[parameter] = signature.parameters[parameter].default

            handler.register_args(*args, **kwargs)

            return handler.result()

        return wrapper_api_request

    return decorator_api_request
