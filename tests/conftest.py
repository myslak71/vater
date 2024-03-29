"""Test fixtures."""
import pytest

from vater.client import Client


@pytest.fixture
def client() -> Client:
    """Yield vat register API client. Client connects to test API client."""
    return Client(base_url="https://wl-test.mf.gov.pl")
