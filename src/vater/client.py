"""Vat register client module."""
import datetime
import functools
import inspect
from enum import Enum
from typing import Callable, Iterable, List, Optional, Tuple, Union

import requests

from vater.errors import ERROR_CODE_MAPPING, InvalidRequestData, UnknownExternalApiError
from vater.models import Subject, SubjectSchema


class RequestType(Enum):
    """Represents request type - there is a different API response for each."""

    CHECK = "check"
    SEARCH = "search"


def handle_response(  # type: ignore
    response, request_type: RequestType, many: bool = False
) -> Union[Tuple[bool, str], Tuple[Union[Subject, List[Subject]], str]]:
    """Handle response from API."""
    if response.status_code == 400:
        raise InvalidRequestData(ERROR_CODE_MAPPING[response.json()["code"]])
    elif response.status_code != 200:
        raise UnknownExternalApiError(response.status_code, response.text)

    result = response.json()["result"]

    if request_type == RequestType.CHECK:
        return result["accountAssigned"] == "TAK", result["requestId"]
    else:
        subjects = SubjectSchema().load(
            result["subjects" if many else "subject"], many=many
        )
        return subjects, result["requestId"]


def api_request(url: str, request_type: RequestType, many: bool = False) -> Callable:
    """Decorate for api requests."""

    def outer_wrapper(func: Callable) -> Callable:
        """Allow passing arguments."""

        @functools.wraps(func)
        def inner_wrapper(
            self, parameter: str, date: datetime.date, account: str = None
        ) -> Union[Tuple[bool, str], Tuple[Union[Subject, List[Subject]], str]]:
            """Fetch subject/subjects and request identifier from API."""
            nonlocal url

            url = prepare_url(account, date, parameter)

            response = requests.get(
                f"{self.base_url}{url}",
                # without User-Agent header production API returns 403
                headers={"User-Agent": ""},
            )

            return handle_response(response, request_type, many)

        def prepare_url(
            account: Optional[str], date: datetime.date, parameter: str
        ) -> str:
            """Evaluate path parameters."""
            nonlocal url
            if request_type == RequestType.CHECK:
                url = url.replace(
                    f"{{{inspect.getfullargspec(func).args[3]}}}",
                    account,  # type: ignore
                )
            else:
                if many and not isinstance(parameter, str):
                    parameter = ",".join(parameter)

            url = url.replace(f"{{{inspect.getfullargspec(func).args[1]}}}", parameter)
            return url.replace("{date}", str(date))

        return inner_wrapper

    return outer_wrapper


class Client:
    """Vat register client class."""

    def __init__(self, base_url: str) -> None:
        """Set API url."""
        self.base_url = base_url

    @api_request("/api/search/nip/{nip}?date={date}", request_type=RequestType.SEARCH)
    def search_nip(self, nip: str, date: datetime.date) -> Tuple[Subject, str]:
        """Get detailed vat payer information for given nip."""

    @api_request(
        "/api/search/nips/{nips}?date={date}",
        request_type=RequestType.SEARCH,
        many=True,
    )
    def search_nips(
        self, nips: Iterable[str], date: datetime.date
    ) -> Tuple[List[Subject], str]:
        """Get a list of detailed vat payers information."""

    @api_request(
        "/api/search/regon/{regon}?date={date}", request_type=RequestType.SEARCH
    )
    def search_regon(self, regon: str, date: datetime.date) -> Tuple[Subject, str]:
        """Get detailed vat payer information for given regon."""

    @api_request(
        "/api/search/regons/{regons}?date={date}",
        request_type=RequestType.SEARCH,
        many=True,
    )
    def search_regons(
        self, regons: Iterable[str], date: datetime.date
    ) -> Tuple[List[Subject], str]:
        """Get a list of detailed vat payers information."""

    @api_request(
        "/api/search/bank-account/{account}?date={date}",
        request_type=RequestType.SEARCH,
        many=True,
    )
    def search_account(self, account: str, date: datetime.date) -> Tuple[Subject, str]:
        """Get detailed vat payer information for given bank account."""

    @api_request(
        "/api/search/bank-accounts/{accounts}?date={date}",
        request_type=RequestType.SEARCH,
        many=True,
    )
    def search_accounts(
        self, accounts: Iterable[str], date: datetime.date
    ) -> Tuple[List[Subject], str]:
        """Get a list of detailed vat payers information."""

    @api_request(
        "/api/check/nip/{nip}/bank-account/{account}?date={date}",
        request_type=RequestType.CHECK,
    )
    def check_nip(
        self, nip: str, date: datetime.date, account: str
    ) -> Tuple[bool, str]:
        """Check if given account is assigned to subject with given nip."""

    @api_request(
        "/api/check/regon/{regon}/bank-account/{account}?date={date}",
        request_type=RequestType.CHECK,
    )
    def check_regon(
        self, regon: str, date: datetime.date, account: str
    ) -> Tuple[bool, str]:
        """Check if given account is assigned to subject with given regon."""


# if __name__ == "__main__":
#     client = Client(base_url="https://wl-api.mf.gov.pl")
#
#     subject = client.search_nip("9542682325", "2019-09-30")
#     print(subject)
#     subjects = client.search_nips(["9542682325"], "2019-09-30")
#     print(subjects)
#     subject = client.search_regon("241234369", "2019-09-30")
#     print(subject)
#     subjects = client.search_regons(["241234369"], "2019-09-30")
#     print(subjects)
#     subject = client.search_account("23249000050000460042096848", "2019-09-30")
#     print(subject)
#     subject = client.search_accounts(["23249000050000460042096848"], "2019-09-30")
#     print(subject)
#
#     res = client.check_nip("9542682325", "2019-09-30", "23249000050000460042096848")
#     print(res)
#     res = client.check_regon("241234369", "2019-09-30", "23249000050000460042096848")
#     print(res)
