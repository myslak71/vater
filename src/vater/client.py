"""Vat register client module."""
import datetime
import functools
import inspect
from typing import Callable, Iterable, List, Optional, Tuple, Type, Union

from vater.models import Subject
from vater.request_types import CheckRequest, RequestType, SearchRequest


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


class Client:
    """Vat register client class."""

    def __init__(self, base_url: str) -> None:
        """
        Set root API url.

        :param base_url: root url of the API
        """
        self.base_url = base_url

    @api_request("/api/search/nip/{nip}?date={date}", SearchRequest)
    def search_nip(
        self, *, nip: str, date: Optional[datetime.date] = None, raw: bool = False
    ) -> Tuple[Subject, str]:
        """
        Get detailed vat payer information for given nip.

        :param nip: nip number of the subject to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        :return: subject and request id
        """

    @api_request("/api/search/nips/{nips}?date={date}", SearchRequest, many=True)
    def search_nips(
        self,
        nips: Iterable[str],
        date: Optional[datetime.date] = None,
        raw: bool = False,
    ) -> Tuple[List[Subject], str]:
        """
        Get a list of detailed vat payers information.

        :param nips: nip numbers of the subjects to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request("/api/search/regon/{regon}?date={date}", SearchRequest)
    def search_regon(
        self, regon: str, date: Optional[datetime.date] = None, raw: bool = False
    ) -> Tuple[Subject, str]:
        """
        Get detailed vat payer information for given regon.

        :param regon: regon number of the subject to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request("/api/search/regons/{regons}?date={date}", SearchRequest, many=True)
    def search_regons(
        self,
        regons: Iterable[str],
        date: Optional[datetime.date] = None,
        raw: bool = False,
    ) -> Tuple[List[Subject], str]:
        """
        Get a list of detailed vat payers information.

        :param regons: regon numbers of the subjects to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request(
        "/api/search/bank-account/{account}?date={date}",
        SearchRequest,
        many=True,  # API returns `subjects` key for single account search
    )
    def search_account(
        self, account: str, date: Optional[datetime.date] = None, raw: bool = False
    ) -> Tuple[Subject, str]:
        """
        Get detailed vat payer information for given bank account.

        :param account: account number of the subject to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request(
        "/api/search/bank-accounts/{accounts}?date={date}", SearchRequest, many=True
    )
    def search_accounts(
        self,
        accounts: Iterable[str],
        date: Optional[datetime.date] = None,
        raw: bool = False,
    ) -> Tuple[List[Subject], str]:
        """
        Get a list of detailed vat payers information.

        :param accounts: account numbers of the subjects to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request(
        "/api/check/nip/{nip}/bank-account/{account}?date={date}", CheckRequest
    )
    def check_nip(
        self,
        nip: str,
        account: str,
        date: Optional[datetime.date] = None,
        raw: bool = False,
    ) -> Tuple[bool, str]:
        """
        Check if given account is assigned to the subject with given nip.

        :param nip: nip number of the subject to check
        :param account: accountat number of the subject to check
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request(
        "/api/check/regon/{regon}/bank-account/{account}?date={date}", CheckRequest
    )
    def check_regon(
        self,
        regon: str,
        account: str,
        date: Optional[datetime.date] = None,
        raw: bool = False,
    ) -> Tuple[bool, str]:
        """
        Check if given account is assigned to the subject with given regon.

        :param regon: regon number of the subject to check
        :param account: account number of the subject to check
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """
