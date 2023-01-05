"""Test fixtures."""
import datetime

import pytest

from vater import EntityPerson, Subject
from vater.client import Client

SAMPLE_NIP = "0" * 10
SAMPLE_REGON = "0" * 9
SAMPLE_ACCOUNT = "0" * 26
SAMPLE_DATE = "2001-01-01"


@pytest.fixture
def client() -> Client:
    """Yield vat register API client. Client connects to test API client."""
    return Client(base_url="https://wl-test.mf.gov.pl")


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
