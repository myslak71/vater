"""Test async client module."""
import datetime
import json
from http import HTTPStatus

import pytest
import pytest_asyncio
from freezegun import freeze_time

from tests.conftest import SAMPLE_ACCOUNT, SAMPLE_DATE, SAMPLE_NIP, SAMPLE_REGON
from vater import AsyncClient
from vater.errors import (
    ERROR_CODE_MAPPING,
    InvalidAccountError,
    InvalidDateError,
    InvalidNipError,
    InvalidRegonError,
    InvalidRequestData,
    UnknownExternalApiError,
)
from vater.models import EntityCheck, EntityItem, EntityList, Entry, EntryList


@pytest_asyncio.fixture
def async_client() -> AsyncClient:
    """Yield vat register API client. Client connects to test API client."""
    return AsyncClient(base_url="https://wl-test.mf.gov.pl")


@pytest.mark.asyncio
async def test_no_result(async_client, httpx_mock):
    """Test that None is returned as a subject for non-existing nip."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nip/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "subject": None,
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1))
    ) == EntityItem(
        subject=None,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.asyncio
async def test_search_nip(async_client, httpx_mock, subject):
    """Test proper object is returned for valid NIP."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nip/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "subject": json.loads(subject.json(by_alias=True)),
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1))
    ) == EntityItem(
        subject=subject,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.asyncio
async def test_search_nips(async_client, httpx_mock, subject):
    """Test proper object is returned for valid NIPS."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nips/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "entries": [
                    {
                        "identifier": "IDENTIFIER",
                        "subjects": [json.loads(subject.json(by_alias=True))],
                    }
                ],
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_nips(
            nips=[SAMPLE_NIP], date=datetime.date(2001, 1, 1)
        )
    ) == EntryList(
        entries=[
            Entry(
                identifier="IDENTIFIER",
                subjects=[subject],
            )
        ],
        request_id="aa111-aa111aaa",
        request_date_time=datetime.datetime(2022, 1, 1, 17, 17, 17),
    )


@pytest.mark.asyncio
async def test_search_regon(async_client, httpx_mock, subject):
    """Test proper object is returned for valid REGON."""
    httpx_mock.add_response(
        url=(
            "https://wl-test.mf.gov.pl/api/search/regon/"
            f"{SAMPLE_REGON}?date={SAMPLE_DATE}"
        ),
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "subject": json.loads(subject.json(by_alias=True)),
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_regon(
            regon=SAMPLE_REGON, date=datetime.date(2001, 1, 1)
        )
    ) == EntityItem(
        subject=subject,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.asyncio
async def test_search_regons(async_client, httpx_mock, subject):
    """Test proper object is returned for valid regons."""
    httpx_mock.add_response(
        url=(
            f"https://wl-test.mf.gov.pl/api/search/regons"
            f"/{SAMPLE_REGON}?date={SAMPLE_DATE}"
        ),
        method="GET",
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "entries": [
                    {
                        "identifier": "IDENTIFIER",
                        "subjects": [json.loads(subject.json(by_alias=True))],
                    }
                ],
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_regons(
            regons=[SAMPLE_REGON], date=datetime.date(2001, 1, 1)
        )
    ) == EntryList(
        entries=[
            Entry(
                identifier="IDENTIFIER",
                subjects=[subject],
            )
        ],
        request_id="aa111-aa111aaa",
        request_date_time=datetime.datetime(2022, 1, 1, 17, 17, 17),
    )


@pytest.mark.asyncio
async def test_search_account(async_client, httpx_mock, subject):
    """Test proper object is returned returned for valid account."""
    httpx_mock.add_response(
        url=(
            "https://wl-test.mf.gov.pl/api/search/bank-account/"
            f"{SAMPLE_ACCOUNT}?date={SAMPLE_DATE}"
        ),
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "subjects": [json.loads(subject.json(by_alias=True))],
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_bank_account(
            bank_account=SAMPLE_ACCOUNT, date=datetime.date(2001, 1, 1)
        )
    ) == EntityList(
        subjects=[subject],
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.asyncio
async def test_search_accounts(async_client, httpx_mock, subject):
    """Test proper object is returned returned for valid accounts."""
    httpx_mock.add_response(
        url=(
            "https://wl-test.mf.gov.pl/api/search/bank-accounts/"
            f"{SAMPLE_ACCOUNT}?date={SAMPLE_DATE}"
        ),
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "entries": [
                    {
                        "identifier": "IDENTIFIER",
                        "subjects": [json.loads(subject.json(by_alias=True))],
                    }
                ],
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_bank_accounts(
            bank_accounts=[SAMPLE_ACCOUNT], date=datetime.date(2001, 1, 1)
        )
    ) == EntryList(
        entries=[
            Entry(
                identifier="IDENTIFIER",
                subjects=[subject],
            )
        ],
        request_id="aa111-aa111aaa",
        request_date_time=datetime.datetime(2022, 1, 1, 17, 17, 17),
    )


@pytest.mark.asyncio
async def test_check_nip(async_client, httpx_mock):
    """Test proper object is returned for valid NIP and account."""
    httpx_mock.add_response(
        url=(
            f"https://wl-test.mf.gov.pl/api/check/nip/{SAMPLE_NIP}/bank-account/"
            f"{SAMPLE_ACCOUNT}?date={SAMPLE_DATE}"
        ),
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "accountAssigned": "TAK",
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.check_nip(
            nip=SAMPLE_NIP, bank_account=SAMPLE_ACCOUNT, date=datetime.date(2001, 1, 1)
        )
    ) == EntityCheck(
        account_assigned=True,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.asyncio
async def test_check_regon(async_client, httpx_mock):
    """Test proper object is returned for valid NIP and account."""
    httpx_mock.add_response(
        url=(
            f"https://wl-test.mf.gov.pl/api/check/regon/{SAMPLE_REGON}/bank-account/"
            f"{SAMPLE_ACCOUNT}?date={SAMPLE_DATE}"
        ),
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "accountAssigned": "TAK",
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.check_regon(
            regon=SAMPLE_REGON,
            bank_account=SAMPLE_ACCOUNT,
            date=datetime.date(2001, 1, 1),
        )
    ) == EntityCheck(
        account_assigned=True,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.asyncio
@freeze_time("2001-01-01")
async def test_default_time(async_client, httpx_mock, subject):
    """Test that today date is used when no date is passed."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nip/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.OK,
        json={
            "result": {
                "subject": json.loads(subject.json(by_alias=True)),
                "requestId": "aa111-aa111aaa",
                "requestDateTime": "01-01-2022 17:17:17",
            }
        },
        headers={"Content-Type": "application/json"},
    )

    assert (
        await async_client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1))
    ) == EntityItem(
        subject=subject,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error_code", [error_code for error_code in ERROR_CODE_MAPPING]
)
async def test_api_returns_400(error_code, async_client, httpx_mock):
    """Test that `InvalidRequestData` is raised when the API returns 400."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nip/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.BAD_REQUEST,
        json={"code": error_code, "message": "Message from the server"},
        headers={"Content-Type": "application/json"},
    )

    with pytest.raises(InvalidRequestData, match=ERROR_CODE_MAPPING[error_code]):
        await async_client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1))


@pytest.mark.asyncio
async def test_api_returns_500(async_client, httpx_mock):
    """Test that `UnknownExternalApiError` is raised when the API returns 500."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nip/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        json={"message": "Unknown error"},
        headers={"Content-Type": "application/json"},
    )

    with pytest.raises(UnknownExternalApiError) as exception_info:
        await async_client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1))

    assert "{'message': 'Unknown error'}" in str(exception_info.value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "nip",
    (
        "123",
        "",
        "12345678901",
        "1234567890",
    ),
)
async def test_invalid_nip(nip, async_client):
    """Test that error is raised when given NIP is invalid."""
    with pytest.raises(InvalidNipError):
        await async_client.search_nip(nip=nip)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "regon",
    (
        "123456",
        "",
        "12345678901",
        "123456789",
    ),
)
async def test_invalid_regon(regon, async_client):
    """Test that error is raised when given REGON is invalid."""
    with pytest.raises(InvalidRegonError):
        await async_client.search_regon(regon=regon)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "account",
    (
        "123456",
        "",
        "0" * 27,
    ),
)
async def test_invalid_account(account, async_client):
    """Test that error is raised when given account is invalid."""
    with pytest.raises(InvalidAccountError):
        await async_client.search_bank_account(bank_account=account)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date",
    (
        "01-01-2019",
        "not a date",
    ),
)
async def test_invalid_date(date, async_client):
    """Test that error is raised when given date is invalid."""
    with pytest.raises(InvalidDateError):
        await async_client.search_nip(nip=SAMPLE_NIP, date=date)
