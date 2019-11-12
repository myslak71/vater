"""Vat register client module."""
import datetime
from typing import Iterable, List, Optional, Tuple

from vater.api_request import api_request
from vater.models import Subject
from vater.request_types import CheckRequest, SearchRequest
from vater.validators import (
    account_validator,
    accounts_validator,
    date_validator,
    nip_validator,
    nips_validator,
    regon_validator,
    regons_validator,
)


class Client:
    """
    Vat register client class.

    Currently the API limits maximum number of requested subjects
    to 30, therefore if that number is exceeded MaximumParameterNumberExceeded
    is raised.
    """

    def __init__(self, base_url: str) -> None:
        """
        Set root API url.

        :param base_url: root url of the API
        """
        self.base_url = base_url

    @api_request(
        "/api/search/nip/{nip}?date={date}",
        SearchRequest,
        validators={"date": [date_validator], "nip": [nip_validator]},
    )
    def search_nip(
        self, nip: str, *, date: Optional[datetime.date] = None, raw: bool = False
    ) -> Tuple[Subject, str]:
        """
        Get detailed vat payer information for given nip.

        :param nip: nip number of the subject to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        :return: subject and request id
        """

    @api_request(
        "/api/search/nips/{nips}?date={date}",
        SearchRequest,
        many=True,
        validators={"date": [date_validator], "nips": [nips_validator]},
    )
    def search_nips(
        self,
        nips: Iterable[str],
        *,
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

    @api_request(
        "/api/search/regon/{regon}?date={date}",
        SearchRequest,
        validators={"date": [date_validator], "regon": [regon_validator]},
    )
    def search_regon(
        self, regon: str, *, date: Optional[datetime.date] = None, raw: bool = False
    ) -> Tuple[Subject, str]:
        """
        Get detailed vat payer information for given regon.

        :param regon: regon number of the subject to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request(
        "/api/search/regons/{regons}?date={date}",
        SearchRequest,
        many=True,
        validators={"date": [date_validator], "regons": [regons_validator]},
    )
    def search_regons(
        self,
        regons: Iterable[str],
        *,
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
        validators={"date": [date_validator], "account": [account_validator]},
    )
    def search_account(
        self, account: str, *, date: Optional[datetime.date] = None, raw: bool = False
    ) -> Tuple[Subject, str]:
        """
        Get detailed vat payer information for given bank account.

        :param account: account number of the subject to fetch
        :param date: date data is acquired from
        :param raw: flag indicating if raw json from the server is returned
                    or python object representation
        """

    @api_request(
        "/api/search/bank-accounts/{accounts}?date={date}",
        SearchRequest,
        many=True,
        validators={"date": [date_validator], "accounts": [accounts_validator]},
    )
    def search_accounts(
        self,
        accounts: Iterable[str],
        *,
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
        "/api/check/nip/{nip}/bank-account/{account}?date={date}",
        CheckRequest,
        validators={
            "date": [date_validator],
            "nip": [nip_validator],
            "account": [account_validator],
        },
    )
    def check_nip(
        self,
        nip: str,
        *,
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
        "/api/check/regon/{regon}/bank-account/{account}?date={date}",
        CheckRequest,
        validators={
            "date": [date_validator],
            "account": [account_validator],
            "regon": [regon_validator],
        },
    )
    def check_regon(
        self,
        regon: str,
        *,
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
