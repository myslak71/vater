"""Test fixtures."""
import pytest

from vater.client import Client


@pytest.fixture
def client() -> Client:
    """Yield vat register API client."""
    return Client(base_url="https://test-api.no")
