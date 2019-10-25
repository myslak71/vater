"""Vat register client module."""
import datetime
import functools
from typing import Callable, Iterable, List, Tuple, Type, Union

from vater.models import Subject
from vater.request_types import CheckRequest, RequestType, SearchRequest


def api_request(
    url_pattern: str, handler_class: Type[RequestType], **kwargs
) -> Callable:
    """Decorate for api requests."""

    def decorator_api_request(func: Callable) -> Callable:
        """Allow passing arguments."""
        handler = handler_class(url_pattern=url_pattern, **kwargs)

        @functools.wraps(func)
        def wrapper_api_request(
            *args: tuple, **kwargs: dict
        ) -> Union[Tuple[bool, str], Tuple[Union[Subject, List[Subject]], str]]:
            """Fetch subject/subjects and request identifier from API."""
            if handler.args is None or handler.kwargs is None:
                handler.register_args(*args, **kwargs)
            return handler.result()

        return wrapper_api_request

    return decorator_api_request


class Client:
    """Vat register client class."""

    def __init__(self, base_url: str) -> None:
        """Set API url."""
        self.base_url = base_url

    @api_request("/api/search/nip/{nip}?date={date}", SearchRequest)
    def search_nip(
        self, *, nip: str, date: datetime.date, raw=False
    ) -> Tuple[Subject, str]:
        """Get detailed vat payer information for given nip."""

    @api_request("/api/search/nips/{nips}?date={date}", SearchRequest, many=True)
    def search_nips(
        self, nips: Iterable[str], date: datetime.date, raw=False
    ) -> Tuple[List[Subject], str]:
        """Get a list of detailed vat payers information."""

    @api_request("/api/search/regon/{regon}?date={date}", SearchRequest)
    def search_regon(
        self, regon: str, date: datetime.date, raw=False
    ) -> Tuple[Subject, str]:
        """Get detailed vat payer information for given regon."""

    @api_request("/api/search/regons/{regons}?date={date}", SearchRequest, many=True)
    def search_regons(
        self, regons: Iterable[str], date: datetime.date, raw=False
    ) -> Tuple[List[Subject], str]:
        """Get a list of detailed vat payers information."""

    @api_request(
        "/api/search/bank-account/{account}?date={date}",
        SearchRequest,
        many=True,  # API returns `subjects` key for single account search
    )
    def search_account(
        self, account: str, date: datetime.date, raw=False
    ) -> Tuple[Subject, str]:
        """Get detailed vat payer information for given bank account."""

    @api_request(
        "/api/search/bank-accounts/{accounts}?date={date}", SearchRequest, many=True
    )
    def search_accounts(
        self, accounts: Iterable[str], date: datetime.date, raw=False
    ) -> Tuple[List[Subject], str]:
        """Get a list of detailed vat payers information."""

    @api_request(
        "/api/check/nip/{nip}/bank-account/{account}?date={date}", CheckRequest
    )
    def check_nip(
        self, nip: str, account: str, date: datetime.date, raw=False
    ) -> Tuple[bool, str]:
        """Check if given account is assigned to the subject with given nip."""

    @api_request(
        "/api/check/regon/{regon}/bank-account/{account}?date={date}", CheckRequest
    )
    def check_regon(
        self, regon: str, account: str, date: datetime.date, raw=False
    ) -> Tuple[bool, str]:
        """Check if given account is assigned to the subject with given regon."""
