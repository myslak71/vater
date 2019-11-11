"""Validators module."""
import datetime
import re
from typing import Dict, Generator, Iterable, Union

from vater.errors import ValidationError


def nip_validator(value: str) -> str:
    """Check if given value is a valid nip number."""
    weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)

    def wrapper() -> str:
        value_len = len(value)
        if value_len != 10:
            raise ValidationError(
                "nip", f"`{value}` invalid length: {value_len}, required 10"
            )

        sum_value = sum(s[0] * int(s[1]) for s in zip(weights, value))
        if sum_value % 11 != int(value[-1]):
            raise ValidationError("nip", f"`{value}` - invalid checksum")

        return value

    return wrapper()


def nips_validator(values_iter: Iterable[str]) -> Generator[str, None, None]:
    """Check if given iterable contains valid nip numbers."""
    return (nip_validator(value) for value in values_iter)


def regon_validator(value: str) -> str:
    """Check if a given value is valid regon number."""
    valid_len = (9, 14)
    weights: Dict[int, tuple] = {
        9: (8, 9, 2, 3, 4, 5, 6, 7),
        14: (2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8),
    }

    def wrapper() -> str:
        value_len = len(value)
        if value_len not in valid_len:
            raise ValidationError(
                "regon", f"`{value}` invalid length: {value_len}, required 9 or 14"
            )
        sum_value = sum(s[0] * int(s[1]) for s in zip(weights[value_len], value))
        if sum_value % 11 != int(value[-1]):
            raise ValidationError("regon", f"`{value}` - invalid checksum")
        return value

    return wrapper()


def regons_validator(values_iter: Iterable[str]) -> Generator[str, None, None]:
    """Check if given iterable contains valid regon numbers."""
    return (regon_validator(value) for value in values_iter)


def account_validator(value: str) -> str:
    """Check if a given value is valid account number."""
    value_len = len(value)
    if value_len != 26:
        raise ValidationError(
            "account", f"`{value}` invalid length: {value_len}, required 26"
        )
    return value


def accounts_validator(values_iter: Iterable[str]) -> Generator[str, None, None]:
    """Check if given iterable contains valid account numbers."""
    return (account_validator(value) for value in values_iter)


def date_validator(value: Union[datetime.date, str]) -> str:
    """Check if a given value may be evaluated to `YYYY-MM-DD` date format."""

    reg = re.compile(r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$")

    def wrapper() -> str:
        value_str = str(value)
        if reg.match(value_str):
            return value_str

        raise ValidationError(
            "date", f"`{value}` is not a valid date, `YYYY-MM-DD` allowed"
        )

    return wrapper()
