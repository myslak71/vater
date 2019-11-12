"""
Module containing integration tests with API.

Data is taken from the test API data available here:
https://www.gov.pl/attachment/5e7f6a61-d6de-4841-891b-ef8122353445
"""


def test_search_nip(client):
    """Test that subject and request identifier are returned for valid test nip."""
    subject, request_id = client.search_nip("3245174504")

    assert subject is not None


def test_search_nips(client):
    """Test that subjects and request identifier are returned for valid test nips."""
    subjects, request_id = client.search_nips(
        ["3245174504", "1854510877", "7250018312"]
    )

    assert len(subjects) == 3


def test_search_regon(client):
    """Test that subject and request identifier are returned for valid test regon."""
    subject, request_id = client.search_regon("887012068")

    assert subject is not None


def test_search_regons(client):
    """Test that subject and request identifier are returned for valid test regon."""
    subjects, request_id = client.search_regons(["755016841", "216973362", "862391869"])

    assert len(subjects) == 3


def test_search_account(client):
    """Test that subjects and request identifier are returned for valid test account."""
    subjects, request_id = client.search_account("70506405335016096312945164")

    assert len(subjects) != 0


def test_search_accounts(client):
    """Test that subjects and request identifier are returned for valid test accounts."""
    subjects, request_id = client.search_accounts(
        [
            "70506405335016096312945164",
            "20028681823250598006154766",
            "31872831997646186715413833",
        ]
    )

    assert len(subjects) == 3


def test_check_nip(client):
    """Test that account is assigned to the nip."""
    is_assigned, request_id = client.check_nip(
        "8655104670", "41146786026458860703735932"
    )

    assert is_assigned


def test_check_regon(client):
    """Test that account is assigned to the nip."""
    is_assigned, request_id = client.check_regon(
        "730371613", "41146786026458860703735932"
    )

    assert is_assigned
