"""Test client module."""
import datetime

import pytest
import responses
from freezegun import freeze_time

from vater.errors import (
    ERROR_CODE_MAPPING,
    InvalidRequestData,
    MaximumParameterNumberExceeded,
    UnknownExternalApiError,
    ValidationError,
)
from vater.models import Company, Subject
from vater.request_types import SearchRequest

SAMPLE_NIP = "0" * 10
SAMPLE_REGON = "0" * 9
SAMPLE_ACCOUNT = "0" * 26


class TestSubjectSearch:
    """Test class for search methods."""

    def set_up(self):
        """Set up test environment."""
        self.example_subject_dict = {
            "name": "Eminem",
            "nip": SAMPLE_NIP,
            "statusVat": "Active",
            "regon": SAMPLE_REGON,
            "pesel": 11 * "7",
            "krs": 5 * "69",
            "residenceAddress": "8 mile",
            "workingAddress": "8 mile",
            "representatives": [
                {
                    "companyName": "Moby Dick Inc",
                    "firstName": "sir Richard",
                    "lastName": "Lion Heart",
                    "nip": SAMPLE_NIP,
                    "pesel": 11 * "7",
                }
            ],
            "authorizedClerks": [
                {
                    "companyName": "Moby Dick Inc",
                    "firstName": "sir Richard",
                    "lastName": "Lion Heart",
                    "nip": SAMPLE_NIP,
                    "pesel": 11 * "7",
                }
            ],
            "partners": [
                {
                    "companyName": "Moby Dick Inc",
                    "firstName": "sir Richard",
                    "lastName": "Lion Heart",
                    "nip": SAMPLE_NIP,
                    "pesel": 11 * "7",
                }
            ],
            "registrationLegalDate": "2001-01-01",
            "registrationDenialBasis": "Denial Basis",
            "registrationDenialDate": "2002-02-02",
            "restorationBasis": "Restoration Basis",
            "restorationDate": "2003-03-03",
            "removalBasis": "Removal Basis",
            "removalDate": "2004-04-04",
            "accountNumbers": [SAMPLE_ACCOUNT],
            "hasVirtualAccounts": False,
        }
        self.example_subject = Subject(
            name="Eminem",
            nip=SAMPLE_NIP,
            status_vat="Active",
            regon=SAMPLE_REGON,
            pesel="77777777777",
            krs="6969696969",
            residence_address="8 mile",
            working_address="8 mile",
            representatives=[
                Company(
                    company_name="Moby Dick Inc",
                    first_name="sir Richard",
                    last_name="Lion Heart",
                    nip=SAMPLE_NIP,
                    pesel="77777777777",
                )
            ],
            authorized_clerks=[
                Company(
                    company_name="Moby Dick Inc",
                    first_name="sir Richard",
                    last_name="Lion Heart",
                    nip=SAMPLE_NIP,
                    pesel="77777777777",
                )
            ],
            partners=[
                Company(
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

    @responses.activate
    def test_search_nip(self, client):
        """Test proper subject and request identifier are returned for valid nip."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/nip/{SAMPLE_NIP}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subject": self.example_subject_dict,
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_nip(SAMPLE_NIP, date=datetime.date(2001, 1, 1)) == (
            self.example_subject,
            "aa111-aa111aaa",
        )

    @responses.activate
    def test_search_nips(self, client):
        """Test proper subjects and request identifier are returned for valid nips."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/nips/{SAMPLE_NIP}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subjects": [self.example_subject_dict],
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_nips(
            nips=[SAMPLE_NIP], date=datetime.date(2001, 1, 1)
        ) == ([self.example_subject], "aa111-aa111aaa")

    @responses.activate
    def test_search_regon(self, client):
        """Test proper subject and request identifier are returned for valid regon."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/regon/{SAMPLE_REGON}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subject": self.example_subject_dict,
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_regon(
            regon=SAMPLE_REGON, date=datetime.date(2001, 1, 1)
        ) == (self.example_subject, "aa111-aa111aaa")

    @responses.activate
    def test_search_regons(self, client):
        """Test proper subjects and request identifier are returned for valid regons."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/regons/{SAMPLE_REGON}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subjects": [self.example_subject_dict],
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_regons(
            regons=[SAMPLE_REGON], date=datetime.date(2001, 1, 1)
        ) == ([self.example_subject], "aa111-aa111aaa")

    @responses.activate
    def test_search_account(self, client):
        """Test proper subject and request identifier are returned for valid account."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/bank-account/{13 * '69'}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subjects": [self.example_subject_dict],
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_account(
            account=f"{13 * '69'}", date=datetime.date(2001, 1, 1)
        ) == ([self.example_subject], "aa111-aa111aaa")

    @responses.activate
    def test_search_accounts(self, client):
        """Test proper subject and request identifier are returned for valid accounts."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/bank-accounts/{SAMPLE_ACCOUNT}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subjects": [self.example_subject_dict],
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_accounts(
            accounts=[SAMPLE_ACCOUNT], date=datetime.date(2001, 1, 1)
        ) == ([self.example_subject], "aa111-aa111aaa")

    @responses.activate
    def test_check_nip(self, client):
        """Test proper tuple is returned for valid nip and account."""
        self.set_up()
        responses.add(
            responses.GET,
            (
                f"https://test-api.no/api/check/nip/{SAMPLE_NIP}/bank-account/"
                f"{SAMPLE_ACCOUNT}?date=2001-01-01"
            ),
            status=200,
            json={"result": {"accountAssigned": "TAK", "requestId": "aa111-aa111aaa"}},
            content_type="application/json",
        )

        assert client.check_nip(
            nip=SAMPLE_NIP, account=SAMPLE_ACCOUNT, date=datetime.date(2001, 1, 1)
        ) == (True, "aa111-aa111aaa")

    @responses.activate
    def test_check_regon(self, client):
        """Test proper tuple is returned for valid regon and account."""
        self.set_up()
        responses.add(
            responses.GET,
            (
                "https://test-api.no/api/check/regon/696969696/bank-account/"
                f"{13 * '69'}?date=2001-01-01"
            ),
            status=200,
            json={"result": {"accountAssigned": "TAK", "requestId": "aa111-aa111aaa"}},
            content_type="application/json",
        )

        assert client.check_regon(
            regon="696969696", account=f"{13 * '69'}", date=datetime.date(2001, 1, 1)
        ) == (True, "aa111-aa111aaa")

    @responses.activate
    def test_default_time(self, client):
        """Test that `today` date is used when no date is passed."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/nip/{SAMPLE_NIP}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subject": self.example_subject_dict,
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        with freeze_time("2001-01-01"):
            assert client.search_nip(nip=SAMPLE_NIP) == (
                self.example_subject,
                "aa111-aa111aaa",
            )

    @responses.activate
    def test_search_raw_set_true(self, client):
        """Test that direct server response is returned when `raw` is set to True."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/nip/{SAMPLE_NIP}?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subject": self.example_subject_dict,
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_nip(
            nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1), raw=True
        ) == {
            "result": {
                "subject": self.example_subject_dict,
                "requestId": "aa111-aa111aaa",
            }
        }

    @responses.activate
    def test_check_raw_set_true(self, client):
        """Test that direct server response is returned when `raw` is set to True."""
        self.set_up()
        responses.add(
            responses.GET,
            (
                f"https://test-api.no/api/check/nip/{SAMPLE_NIP}/bank-account/"
                f"{13 * '69'}?date=2001-01-01"
            ),
            status=200,
            json={"result": {"accountAssigned": "TAK", "requestId": "aa111-aa111aaa"}},
            content_type="application/json",
        )

        assert client.check_nip(
            nip=SAMPLE_NIP,
            account=f"{13 * '69'}",
            date=datetime.date(2001, 1, 1),
            raw=True,
        ) == {"result": {"accountAssigned": "TAK", "requestId": "aa111-aa111aaa"}}

    @pytest.mark.parametrize(
        "error_code", [error_code for error_code in ERROR_CODE_MAPPING]
    )
    @responses.activate
    def test_api_returns_400(self, error_code, client):
        """Test that `InvalidRequestData` is raised when the API returns 400."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/nip/{SAMPLE_NIP}?date=2001-01-01",
            status=400,
            json={"code": error_code, "message": "Message from the server"},
            content_type="application/json",
        )

        with pytest.raises(InvalidRequestData, match=ERROR_CODE_MAPPING[error_code]):
            client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1), raw=True)

    @responses.activate
    def test_api_returns_500(self, client):
        """Test that `UnknownExternalApiError` is raised when the API returns 400."""
        self.set_up()
        responses.add(
            responses.GET,
            f"https://test-api.no/api/search/nip/{SAMPLE_NIP}?date=2001-01-01",
            status=500,
            json={"message": "Uknown error"},
            content_type="application/json",
        )

        with pytest.raises(UnknownExternalApiError) as exception_info:
            client.search_nip(nip=SAMPLE_NIP, date=datetime.date(2001, 1, 1), raw=True)

        assert (
            'UnknownExternalApiError: status code: 500, data: {"message": "Uknown error"}'
            in str(exception_info.value)
        )

    def test_max_args_exceeded(self, client):
        """Test that error is raised when number of args exceeds allowed maximum."""
        with pytest.raises(MaximumParameterNumberExceeded) as exception_info:
            client.search_nips([SAMPLE_NIP] * (SearchRequest.PARAM_LIMIT + 1))

        assert str(exception_info.value) == (
            "MaximumParameterNumberExceeded: number of nips exceeds allowed maximum: "
            f"{SearchRequest.PARAM_LIMIT}"
        )

    @pytest.mark.parametrize(
        "nip, err_msg",
        (
            ("123", "ValidationError: nip `123` invalid length: 3, required 10"),
            ("", "ValidationError: nip `` invalid length: 0, required 10"),
            (
                "12345678901",
                "ValidationError: nip `12345678901` invalid length: 11, required 10",
            ),
            ("1234567890", "ValidationError: nip `1234567890` - invalid checksum"),
        ),
    )
    def test_invalid_nip(self, nip, err_msg, client):
        """Test that error is raised when given nip is invalid."""
        with pytest.raises(ValidationError) as exception_info:
            client.search_nip(nip)

        assert str(exception_info.value) == err_msg

    @pytest.mark.parametrize(
        "nips, err_msg",
        (
            (["123"], "ValidationError: nip `123` invalid length: 3, required 10"),
            ([""], "ValidationError: nip `` invalid length: 0, required 10"),
            (
                ["12345678901"],
                "ValidationError: nip `12345678901` invalid length: 11, required 10",
            ),
            (["1234567890"], "ValidationError: nip `1234567890` - invalid checksum"),
        ),
    )
    def test_invalid_nips(self, nips, err_msg, client):
        """Test that error is raised when given nips are invalid."""
        with pytest.raises(ValidationError) as exception_info:
            client.search_nips(nips)

        assert str(exception_info.value) == err_msg

    @pytest.mark.parametrize(
        "regon, err_msg",
        (
            (
                "123456",
                "ValidationError: regon `123456` invalid length: 6, required 9 or 14",
            ),
            ("", "ValidationError: regon `` invalid length: 0, required 9 or 14"),
            (
                "12345678901",
                "ValidationError: regon `12345678901` invalid length: 11, required 9 or 14",
            ),
            ("123456789", "ValidationError: regon `123456789` - invalid checksum"),
        ),
    )
    def test_invalid_regon(self, regon, err_msg, client):
        """Test that error is raised when given regon is invalid."""
        with pytest.raises(ValidationError) as exception_info:
            client.search_regon(regon)

        assert str(exception_info.value) == err_msg

    @pytest.mark.parametrize(
        "regons, err_msg",
        (
            (
                ["123456"],
                "ValidationError: regon `123456` invalid length: 6, required 9 or 14",
            ),
            ([""], "ValidationError: regon `` invalid length: 0, required 9 or 14"),
            (
                ["12345678901"],
                "ValidationError: regon `12345678901` invalid length: 11, required 9 or 14",
            ),
            (["123456789"], "ValidationError: regon `123456789` - invalid checksum"),
        ),
    )
    def test_invalid_regons(self, regons, err_msg, client):
        """Test that error is raised when given regons are invalid."""
        with pytest.raises(ValidationError) as exception_info:
            client.search_regons(regons)

        assert str(exception_info.value) == err_msg

    @pytest.mark.parametrize(
        "account, err_msg",
        (
            (
                "123456",
                "ValidationError: account `123456` invalid length: 6, required 26",
            ),
            ("", "ValidationError: account `` invalid length: 0, required 26"),
            (
                "0" * 27,
                f"ValidationError: account `{'0'*27}` invalid length: 27, required 26",
            ),
        ),
    )
    def test_invalid_account(self, account, err_msg, client):
        """Test that error is raised when given account is invalid."""
        with pytest.raises(ValidationError) as exception_info:
            client.search_account(account)

        assert str(exception_info.value) == err_msg

    @pytest.mark.parametrize(
        "accounts, err_msg",
        (
            (
                ["123456"],
                "ValidationError: account `123456` invalid length: 6, required 26",
            ),
            ([""], "ValidationError: account `` invalid length: 0, required 26"),
            (
                ["0" * 27],
                f"ValidationError: account `{'0'*27}` invalid length: 27, required 26",
            ),
        ),
    )
    def test_invalid_accounts(self, accounts, err_msg, client):
        """Test that error is raised when given accounts are invalid."""
        with pytest.raises(ValidationError) as exception_info:
            client.search_accounts(accounts)

        assert str(exception_info.value) == err_msg

    @pytest.mark.parametrize(
        "date, err_msg",
        (
            (
                "01-01-2019",
                "ValidationError: date `01-01-2019` is not a valid date, `YYYY-MM-DD` allowed",
            ),
            (
                "not a date",
                "ValidationError: date `not a date` is not a valid date, `YYYY-MM-DD` allowed",
            ),
        ),
    )
    def test_invalid_date(self, date, err_msg, client):
        """Test that error is raised when given date is invalid."""
        with pytest.raises(ValidationError) as exception_info:
            client.search_nip("0" * 10, date=date)

        assert str(exception_info.value) == err_msg
