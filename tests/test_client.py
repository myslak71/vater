"""Test client module."""
import datetime
import json
from http import HTTPStatus

import pytest
from freezegun import freeze_time

from tests.conftest import SAMPLE_ACCOUNT, SAMPLE_DATE, SAMPLE_NIP, SAMPLE_REGON
from vater.errors import (
    ERROR_CODE_MAPPING,
    InvalidAccountError,
    InvalidDateError,
    InvalidNipError,
    InvalidRegonError,
    InvalidRequestData,
    UnknownExternalApiError,
)
from vater.models import (
    EntityCheck,
    EntityItem,
    EntityList,
    EntityPerson,
    Entry,
    EntryList,
    Subject,
)


@pytest.fixture
def subject() -> Subject:
    """Return sample Subject."""
    return Subject(
        name="Eminem",
        nip=SAMPLE_NIP,
        status_vat="Active",
        regon=SAMPLE_REGON,
        pesel="77777777777",
        krs="6969696969",
        residence_address="8 mile",
        working_address="8 mile",
        representatives=[
            EntityPerson(
                company_name="Moby Dick Inc",
                first_name="sir Richard",
                last_name="Lion Heart",
                nip=SAMPLE_NIP,
                pesel="77777777777",
            )
        ],
        authorized_clerks=[
            EntityPerson(
                company_name="Moby Dick Inc",
                first_name="sir Richard",
                last_name="Lion Heart",
                nip=SAMPLE_NIP,
                pesel="77777777777",
            )
        ],
        partners=[
            EntityPerson(
                company_name="Moby Dick Inc",
                first_name="sir Richard",
                last_name="Lion Heart",
                nip=SAMPLE_NIP,
                pesel="77777777777",
            )
        ],
        registration_legal_date=datetime.date(2001, 1, 1),
        registration_denial_basis="Denial Basis",
        registration_denial_date=datetime.date(2002, 2, 2),
        restoration_basis="Restoration Basis",
        restoration_date=datetime.date(2003, 3, 3),
        removal_basis="Removal Basis",
        removal_date=datetime.date(2004, 4, 4),
        account_numbers=[SAMPLE_ACCOUNT],
        has_virtual_accounts=False,
    )


def test_no_result(client, httpx_mock):
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

    assert client.search_nip(
        nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1)
    ) == EntityItem(
        subject=None,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


def test_search_nip(client, httpx_mock, subject):
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

    assert client.search_nip(
        nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1)
    ) == EntityItem(
        subject=subject,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


def test_search_nips(client, httpx_mock, subject):
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

    assert client.search_nips(
        nips=[SAMPLE_NIP], date=datetime.date(2001, 1, 1)
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


def test_search_regon(client, httpx_mock, subject):
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

    assert client.search_regon(
        regon=SAMPLE_REGON, date=datetime.date(2001, 1, 1)
    ) == EntityItem(
        subject=subject,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


def test_search_regons(client, httpx_mock, subject):
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

    assert client.search_regons(
        regons=[SAMPLE_REGON], date=datetime.date(2001, 1, 1)
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


def test_search_account(client, httpx_mock, subject):
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

    assert client.search_bank_account(
        bank_account=SAMPLE_ACCOUNT, date=datetime.date(2001, 1, 1)
    ) == EntityList(
        subjects=[subject],
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


def test_search_accounts(client, httpx_mock, subject):
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

    assert client.search_bank_accounts(
        bank_accounts=[SAMPLE_ACCOUNT], date=datetime.date(2001, 1, 1)
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


def test_check_nip(client, httpx_mock):
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

    assert client.check_nip(
        nip=SAMPLE_NIP, bank_account=SAMPLE_ACCOUNT, date=datetime.date(2001, 1, 1)
    ) == EntityCheck(
        account_assigned=True,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


def test_check_regon(client, httpx_mock):
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

    assert client.check_regon(
        regon=SAMPLE_REGON, bank_account=SAMPLE_ACCOUNT, date=datetime.date(2001, 1, 1)
    ) == EntityCheck(
        account_assigned=True,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@freeze_time("2001-01-01")
def test_default_time(client, httpx_mock, subject):
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

    assert client.search_nip(
        nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1)
    ) == EntityItem(
        subject=subject,
        request_id="aa111-aa111aaa",
        request_date_time="01-01-2022 17:17:17",
    )


@pytest.mark.parametrize(
    "error_code", [error_code for error_code in ERROR_CODE_MAPPING]
)
def test_api_returns_400(error_code, client, httpx_mock):
    """Test that `InvalidRequestData` is raised when the API returns 400."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nip/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.BAD_REQUEST,
        json={"code": error_code, "message": "Message from the server"},
        headers={"Content-Type": "application/json"},
    )

    with pytest.raises(InvalidRequestData, match=ERROR_CODE_MAPPING[error_code]):
        client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1))


def test_api_returns_500(client, httpx_mock):
    """Test that `UnknownExternalApiError` is raised when the API returns 500."""
    httpx_mock.add_response(
        url=f"https://wl-test.mf.gov.pl/api/search/nip/{SAMPLE_NIP}?date={SAMPLE_DATE}",
        method="GET",
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        json={"message": "Unknown error"},
        headers={"Content-Type": "application/json"},
    )

    with pytest.raises(UnknownExternalApiError) as exception_info:
        client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1))

    assert "{'message': 'Unknown error'}" in str(exception_info.value)


@pytest.mark.parametrize(
    "nip",
    (
        "123",
        "",
        "12345678901",
        "1234567890",
    ),
)
def test_invalid_nip(nip, client):
    """Test that error is raised when given NIP is invalid."""
    with pytest.raises(InvalidNipError):
        client.search_nip(nip=nip)


@pytest.mark.parametrize(
    "regon",
    (
        "123456",
        "",
        "12345678901",
        "123456789",
    ),
)
def test_invalid_regon(regon, client):
    """Test that error is raised when given REGON is invalid."""
    with pytest.raises(InvalidRegonError):
        client.search_regon(regon=regon)


@pytest.mark.parametrize(
    "account",
    (
        "123456",
        "",
        "0" * 27,
    ),
)
def test_invalid_account(account, client):
    """Test that error is raised when given account is invalid."""
    with pytest.raises(InvalidAccountError):
        client.search_bank_account(bank_account=account)


@pytest.mark.parametrize(
    "date",
    (
        "01-01-2019",
        "not a date",
    ),
)
def test_invalid_date(date, client):
    """Test that error is raised when given date is invalid."""
    with pytest.raises(InvalidDateError):
        client.search_nip(nip=SAMPLE_NIP, date=date)
