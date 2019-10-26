"""Test client module."""
import datetime

import pytest
import responses
from freezegun import freeze_time

from vater.errors import ERROR_CODE_MAPPING, InvalidRequestData, UnknownExternalApiError
from vater.models import Company, Subject


class TestSubjectSearch:
    """Test class for search methods."""

    def set_up(self):
        """Set up test environment."""
        self.example_subject_dict = {
            "name": "Eminem",
            "nip": 5 * "69",
            "statusVat": "Active",
            "regon": 9 * "7",
            "pesel": 11 * "7",
            "krs": 5 * "69",
            "residenceAddress": "8 mile",
            "workingAddress": "8 mile",
            "representatives": [
                {
                    "companyName": "Moby Dick Inc",
                    "firstName": "sir Richard",
                    "lastName": "Lion Heart",
                    "nip": 5 * "69",
                    "pesel": 11 * "7",
                }
            ],
            "authorizedClerks": [
                {
                    "companyName": "Moby Dick Inc",
                    "firstName": "sir Richard",
                    "lastName": "Lion Heart",
                    "nip": 5 * "69",
                    "pesel": 11 * "7",
                }
            ],
            "partners": [
                {
                    "companyName": "Moby Dick Inc",
                    "firstName": "sir Richard",
                    "lastName": "Lion Heart",
                    "nip": 5 * "69",
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
            "accountNumbers": [26 * "1"],
            "hasVirtualAccounts": False,
        }
        self.example_subject = Subject(
            name="Eminem",
            nip="6969696969",
            status_vat="Active",
            regon="777777777",
            pesel="77777777777",
            krs="6969696969",
            residence_address="8 mile",
            working_address="8 mile",
            representatives=[
                Company(
                    company_name="Moby Dick Inc",
                    first_name="sir Richard",
                    last_name="Lion Heart",
                    nip="6969696969",
                    pesel="77777777777",
                )
            ],
            authorized_clerks=[
                Company(
                    company_name="Moby Dick Inc",
                    first_name="sir Richard",
                    last_name="Lion Heart",
                    nip="6969696969",
                    pesel="77777777777",
                )
            ],
            partners=[
                Company(
                    company_name="Moby Dick Inc",
                    first_name="sir Richard",
                    last_name="Lion Heart",
                    nip="6969696969",
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
            account_numbers=["11111111111111111111111111"],
            has_virtual_accounts=False,
        )

    @responses.activate
    def test_search_nip(self, client):
        """Test proper subject and request identifier are returned for valid nip."""
        self.set_up()
        responses.add(
            responses.GET,
            "https://test-api.no/api/search/nip/6969696969?date=2001-01-01",
            status=200,
            json={
                "result": {
                    "subject": self.example_subject_dict,
                    "requestId": "aa111-aa111aaa",
                }
            },
            content_type="application/json",
        )

        assert client.search_nip(nip="6969696969", date=datetime.date(2001, 1, 1)) == (
            self.example_subject,
            "aa111-aa111aaa",
        )

    @responses.activate
    def test_search_nips(self, client):
        """Test proper subjects and request identifier are returned for valid nips."""
        self.set_up()
        responses.add(
            responses.GET,
            "https://test-api.no/api/search/nips/6969696969?date=2001-01-01",
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
            nips=["6969696969"], date=datetime.date(2001, 1, 1)
        ) == ([self.example_subject], "aa111-aa111aaa")

    @responses.activate
    def test_search_regon(self, client):
        """Test proper subject and request identifier are returned for valid regon."""
        self.set_up()
        responses.add(
            responses.GET,
            "https://test-api.no/api/search/regon/696969696?date=2001-01-01",
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
            regon="696969696", date=datetime.date(2001, 1, 1)
        ) == (self.example_subject, "aa111-aa111aaa")

    @responses.activate
    def test_search_regons(self, client):
        """Test proper subjects and request identifier are returned for valid regons."""
        self.set_up()
        responses.add(
            responses.GET,
            "https://test-api.no/api/search/regons/696969696?date=2001-01-01",
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
            regons=["696969696"], date=datetime.date(2001, 1, 1)
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
            f"https://test-api.no/api/search/bank-accounts/{13 * '69'}?date=2001-01-01",
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
            accounts=[f"{13 * '69'}"], date=datetime.date(2001, 1, 1)
        ) == ([self.example_subject], "aa111-aa111aaa")

    @responses.activate
    def test_check_nip(self, client):
        """Test proper tuple is returned for valid nip and account."""
        self.set_up()
        responses.add(
            responses.GET,
            (
                "https://test-api.no/api/check/nip/6969696969/bank-account/"
                f"{13 * '69'}?date=2001-01-01"
            ),
            status=200,
            json={"result": {"accountAssigned": "TAK", "requestId": "aa111-aa111aaa"}},
            content_type="application/json",
        )

        assert client.check_nip(
            nip="6969696969", account=f"{13 * '69'}", date=datetime.date(2001, 1, 1)
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
            "https://test-api.no/api/search/nip/6969696969?date=2001-01-01",
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
            assert client.search_nip(nip="6969696969") == (
                self.example_subject,
                "aa111-aa111aaa",
            )

    @responses.activate
    def test_search_raw_set_true(self, client):
        """Test that direct server response is returned when `raw` is set to True."""
        self.set_up()
        responses.add(
            responses.GET,
            "https://test-api.no/api/search/nip/6969696969?date=2001-01-01",
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
            nip="6969696969", date=datetime.date(2001, 1, 1), raw=True
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
                "https://test-api.no/api/check/nip/6969696969/bank-account/"
                f"{13 * '69'}?date=2001-01-01"
            ),
            status=200,
            json={"result": {"accountAssigned": "TAK", "requestId": "aa111-aa111aaa"}},
            content_type="application/json",
        )

        assert client.check_nip(
            nip="6969696969",
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
            "https://test-api.no/api/search/nip/6969696969?date=2001-01-01",
            status=400,
            json={"code": error_code, "message": "Message from the server"},
            content_type="application/json",
        )

        with pytest.raises(InvalidRequestData, match=ERROR_CODE_MAPPING[error_code]):
            client.search_nip(
                nip="6969696969", date=datetime.date(2001, 1, 1), raw=True
            )

    @responses.activate
    def test_api_returns_500(self, client):
        """Test that `UnknownExternalApiError` is raised when the API returns 400."""
        self.set_up()
        responses.add(
            responses.GET,
            "https://test-api.no/api/search/nip/6969696969?date=2001-01-01",
            status=500,
            json={"message": "Uknown error"},
            content_type="application/json",
        )

        with pytest.raises(UnknownExternalApiError) as exception_info:
            client.search_nip(
                nip="6969696969", date=datetime.date(2001, 1, 1), raw=True
            )

        assert (
            'UnknownExternalApiError: status code: 500, data: {"message": "Uknown error"}'
            in str(exception_info.value)
        )
