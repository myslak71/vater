"""Vat register client module."""
import datetime
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Self

from httpx import AsyncClient as AsyncHTTPClient
from httpx import Client as HTTPClient
from httpx import Response

from vater.errors import (
    ERROR_CODE_MAPPING,
    InvalidAccountError,
    InvalidDateError,
    InvalidNipError,
    InvalidRegonError,
    InvalidRequestData,
    UnknownExternalApiError,
)
from vater.models import EntityCheck, EntityItem, EntityList, EntryList


class BaseClient(ABC):
    """Abstract class for all clients."""

    # Used for NIP validation
    _NIP_WEIGHTS = (6, 5, 7, 2, 3, 4, 5, 6, 7)

    # Used for REGON validation
    _REGON_WEIGHTS = {
        9: (8, 9, 2, 3, 4, 5, 6, 7),
        14: (2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8),
    }
    _VALID_REGON_LENGTHS = (9, 14)

    _DATE_FORMAT = "%Y-%m-%d"

    def __init__(self: Self, *, base_url: str) -> None:
        """
        Set root API URL.

        :param base_url: root URL of the VAT register API
        """
        self.base_url = base_url

    def _validate_date(
        self: Self,
        value: str | datetime.date | None,
    ) -> datetime.date:
        """Validate given date."""
        if value is None:
            return datetime.date.today()

        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value, self._DATE_FORMAT).date()
            except ValueError:
                raise InvalidDateError(
                    (
                        f"Given date is not datetime.date, datetime.datetime "
                        f"or str with `{self._DATE_FORMAT}`"
                    )
                )
        elif not isinstance(value, datetime.date):
            raise InvalidDateError(
                (
                    f"Given date is not datetime.date, datetime.datetime "
                    f"or str with `{self._DATE_FORMAT}`"
                )
            )

        return value

    def _validate_nip(self: Self, value: str) -> None:
        """Validate NIP value."""
        value_len = len(value)
        if value_len != 10:
            raise InvalidNipError(f"`{value}` invalid length: {value_len}, required 10")

        sum_value = sum(s[0] * int(s[1]) for s in zip(self._NIP_WEIGHTS, value))
        if sum_value % 11 != int(value[-1]):
            raise InvalidNipError(f"`{value}` - invalid checksum")

    def _validate_regon(self: Self, value: str) -> None:
        """Validate REGON value."""
        value_len = len(value)
        if value_len not in self._VALID_REGON_LENGTHS:
            raise InvalidRegonError(
                (
                    f"`{value}` invalid length: {value_len}, "
                    f"required {self._VALID_REGON_LENGTHS}"
                )
            )

        sum_value = sum(
            s[0] * int(s[1]) for s in zip(self._REGON_WEIGHTS[value_len], value)
        )
        if sum_value % 11 != int(value[-1]):
            raise InvalidRegonError(f"`{value}` - invalid checksum")

    @staticmethod
    def _validate_account(value: str) -> str:
        """Check if a given value is valid account number."""
        value_len = len(value)
        if value_len != 26:
            raise InvalidAccountError(
                f"`{value}` invalid length: {value_len}, required 26"
            )
        return value

    @abstractmethod
    async def _send_request(self, url: str, params: dict[str, str]) -> dict:
        """Make request to VAT register API."""
        pass

    @staticmethod
    def _handle_response_status_code(response: Response) -> dict[str, Any]:
        """Handle response status code."""
        if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise UnknownExternalApiError(response.json())
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise InvalidRequestData(ERROR_CODE_MAPPING[response.json()["code"]])
        if response.status_code == HTTPStatus.OK:
            return response.json()


class AsyncClient(BaseClient):
    """
    Vat register client class.

    Currently the API limits maximum number of requested subjects
    to 30, therefore if that number is exceeded MaximumParameterNumberExceeded
    is raised.
    """

    async def _send_request(self, url: str, params: dict[str, str]) -> dict:
        """Send GET request with given URL parameters to given URL."""
        async with AsyncHTTPClient(base_url=self.base_url) as client:
            response = await client.get(url=url, params=params)

        return self._handle_response_status_code(response=response)

    async def search_nip(
        self: Self, *, nip: str, date: datetime.date | None = None
    ) -> EntityItem:
        """
        Get detailed VAT payer information for given NIP.

        :param nip: NIP number of the subject to fetch
        :param date: date data is acquired from
        :return: EntityItem object
        """
        self._validate_nip(nip)
        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/search/nip/{nip}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityItem.parse_obj(response_payload["result"])

    async def search_nips(
        self: Self, *, nips: list[str], date: datetime.date | None = None
    ) -> EntryList:
        """
        Get detailed VAT payer information for given NIPs.

        :param nips: NIP numbers of the subjects to fetch
        :param date: date data is acquired from
        :return: EntryList object
        """
        for nip in nips:
            self._validate_nip(nip)

        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/search/nips/{','.join(nips)}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntryList.parse_obj(response_payload["result"])

    async def search_regon(
        self: Self, *, regon: str, date: datetime.date | None = None
    ) -> EntityItem:
        """
        Get detailed VAT payer information for given REGON.

        :param regon: REGON number of the subject to fetch
        :param date: date data is acquired from
        :return: EntityItem object
        """
        self._validate_regon(regon)
        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/search/regon/{regon}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityItem.parse_obj(response_payload["result"])

    async def search_regons(
        self: Self, *, regons: list[str], date: datetime.date | None = None
    ) -> EntryList:
        """
        Get detailed VAT payer information for given REGONs.

        :param regons: REGON numbers of the subjects to fetch
        :param date: date data is acquired from
        :return: EntryList object
        """
        for regon in regons:
            self._validate_regon(regon)

        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/search/regons/{','.join(regons)}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntryList.parse_obj(response_payload["result"])

    async def search_bank_account(
        self: Self, *, bank_account: str, date: datetime.date | None = None
    ) -> EntityList:
        """
        Get detailed VAT payer information for given account.

        :param bank_account: account number of the subject to fetch
        :param date: date data is acquired from
        :return: EntityList object
        """
        self._validate_account(bank_account)
        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/search/bank-account/{bank_account}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityList.parse_obj(response_payload["result"])

    async def search_bank_accounts(
        self: Self, *, bank_accounts: list[str], date: datetime.date | None = None
    ) -> EntryList:
        """
        Get detailed VAT payer information for given accounts.

        :param bank_accounts: account numbers of the subject to fetch
        :param date: date data is acquired from
        :return: EntryList object
        """
        for account in bank_accounts:
            self._validate_account(account)

        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/search/bank-accounts/{','.join(bank_accounts)}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntryList.parse_obj(response_payload["result"])

    async def check_regon(
        self,
        *,
        regon: str,
        bank_account: str,
        date: datetime.date | None = None,
    ) -> EntityCheck:
        """
        Check if given account is assigned to the subject with given REGON.

        :param regon: REGON number of the subject to check
        :param bank_account: account number of the subject to check
        :param date: EntityCheck object
        """
        self._validate_regon(regon)
        self._validate_account(bank_account)
        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/check/regon/{regon}/bank-account/{bank_account}?date={date}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityCheck.parse_obj(response_payload["result"])

    async def check_nip(
        self,
        *,
        nip: str,
        bank_account: str,
        date: datetime.date | None = None,
    ) -> EntityCheck:
        """
        Check if given account is assigned to the subject with given NIP.

        :param nip: NIP number of the subject to check
        :param bank_account: account number of the subject to check
        :param date: EntityCheck object
        """
        self._validate_nip(nip)
        self._validate_account(bank_account)
        date = self._validate_date(date)

        response_payload = await self._send_request(
            url=f"/api/check/nip/{nip}/bank-account/{bank_account}?date={date}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityCheck.parse_obj(response_payload["result"])


class Client(BaseClient):
    """
    Vat register client class.

    Currently the API limits maximum number of requested subjects
    to 30, therefore if that number is exceeded MaximumParameterNumberExceeded
    is raised.
    """

    def _send_request(self, url: str, params: dict[str, str]) -> dict:
        """Send GET request with given URL parameters to given URL."""
        with HTTPClient(base_url=self.base_url) as client:
            response = client.get(url=url, params=params)

        return self._handle_response_status_code(response=response)

    def search_nip(
        self: Self, *, nip: str, date: datetime.date | None = None
    ) -> EntityItem:
        """
        Get detailed VAT payer information for given NIP.

        :param nip: NIP number of the subject to fetch
        :param date: date data is acquired from
        :return: EntityItem object
        """
        self._validate_nip(nip)
        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/search/nip/{nip}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityItem.parse_obj(response_payload["result"])

    def search_nips(
        self: Self, *, nips: list[str], date: datetime.date | None = None
    ) -> EntryList:
        """
        Get detailed VAT payer information for given NIPs.

        :param nips: NIP numbers of the subjects to fetch
        :param date: date data is acquired from
        :return: EntryList object
        """
        for nip in nips:
            self._validate_nip(nip)

        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/search/nips/{','.join(nips)}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntryList.parse_obj(response_payload["result"])

    def search_regon(
        self: Self, *, regon: str, date: datetime.date | None = None
    ) -> EntityItem:
        """
        Get detailed VAT payer information for given regon.

        :param regon: REGON number of the subject to fetch
        :param date: date data is acquired from
        :return: EntityItem object
        """
        self._validate_regon(regon)
        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/search/regon/{regon}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityItem.parse_obj(response_payload["result"])

    def search_regons(
        self: Self, *, regons: list[str], date: datetime.date | None = None
    ) -> EntryList:
        """
        Get detailed VAT payer information for given REGONs.

        :param regons: REGON numbers of the subjects to fetch
        :param date: date data is acquired from
        :return: EntryList object
        """
        for regon in regons:
            self._validate_regon(regon)

        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/search/regons/{','.join(regons)}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntryList.parse_obj(response_payload["result"])

    def search_bank_account(
        self: Self, *, bank_account: str, date: datetime.date | None = None
    ) -> EntityList:
        """
        Get detailed VAT payer information for given account.

        :param bank_account: bank account number of the subjects to fetch
        :param date: date data is acquired from
        :return: EntityList object
        """
        self._validate_account(bank_account)
        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/search/bank-account/{bank_account}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityList.parse_obj(response_payload["result"])

    def search_bank_accounts(
        self: Self, *, bank_accounts: list[str], date: datetime.date | None = None
    ) -> EntryList:
        """
        Get detailed VAT payer information for given accounts.

        :param bank_accounts: account numbers of the subject to fetch
        :param date: date data is acquired from
        :return: EntryList object
        """
        for account in bank_accounts:
            self._validate_account(account)

        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/search/bank-accounts/{','.join(bank_accounts)}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntryList.parse_obj(response_payload["result"])

    def check_regon(
        self,
        *,
        regon: str,
        bank_account: str,
        date: datetime.date | None = None,
    ) -> EntityCheck:
        """
        Check if given account is assigned to the subject with given REGON.

        :param regon: REGON number of the subject to check
        :param bank_account: account number of the subject to check
        :param date: EntityCheck object
        """
        self._validate_regon(regon)
        self._validate_account(bank_account)
        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/check/regon/{regon}/bank-account/{bank_account}?date={date}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityCheck.parse_obj(response_payload["result"])

    def check_nip(
        self,
        *,
        nip: str,
        bank_account: str,
        date: datetime.date | None = None,
    ) -> EntityCheck:
        """
        Check if given account is assigned to the subject with given NIP.

        :param nip: NIP number of the subject to check
        :param bank_account: account number of the subject to check
        :param date: EntityCheck object
        """
        self._validate_nip(nip)
        self._validate_account(bank_account)
        date = self._validate_date(date)

        response_payload = self._send_request(
            url=f"/api/check/nip/{nip}/bank-account/{bank_account}?date={date}",
            params={"date": date.strftime(self._DATE_FORMAT)},
        )

        return EntityCheck.parse_obj(response_payload["result"])
