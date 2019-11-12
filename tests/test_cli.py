"""Test cli module."""
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from vater.cli import cli

SAMPLE_ACCOUNT = 26 * "1"
SAMPLE_NIP = 10 * "1"
SAMPLE_REGON = 14 * "1"

CLI_CHECK_METHODS = ("check-nip", "check-regon")


@pytest.mark.parametrize(
    "command, params",
    (
        ("search-account", [SAMPLE_ACCOUNT]),
        ("search-accounts", [SAMPLE_ACCOUNT]),
        ("search-nip", [SAMPLE_NIP]),
        ("search-nips", [SAMPLE_NIP]),
        ("search-regon", [SAMPLE_REGON]),
        ("search-regons", [SAMPLE_REGON]),
    ),
)
def test_search_commands(command, params):
    """Test that proper client search methods are called."""
    runner = CliRunner()
    method_name = command.replace("-", "_")

    with patch(f"vater.client.Client.{method_name}") as mock_method:
        runner.invoke(cli, [command] + params)

    mock_method.assert_called()


@pytest.mark.parametrize(
    "command, params",
    (
        ("check-nip", [SAMPLE_NIP, SAMPLE_ACCOUNT]),
        ("check-regon", [SAMPLE_REGON, SAMPLE_ACCOUNT]),
    ),
)
def test_check_commands(command, params):
    """Test that proper client check methods are called."""
    runner = CliRunner()
    method_name = command.replace("-", "_")

    with patch(f"vater.client.Client.{method_name}") as mock_method:
        runner.invoke(cli, [command] + params)

    mock_method.assert_called()
