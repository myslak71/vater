"""Utils module for vater."""
import re
from typing import List

from vater.errors import InvalidNipsNumber
from vater.models import Subject


def validate_nips(nips: str) -> List[str]:
    """Validate nip numbers."""
    nips_list = re.findall(r"\d{10}", nips)

    if not nips_list:
        raise InvalidNipsNumber("At least one nip number is required.")
    elif len(nips_list) > 300:
        raise InvalidNipsNumber("Number of nips cannot exceed 300.")

    return nips_list


def camel_to_snake(value: str) -> str:
    """Convert given camelCase string to snake_case string."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(value: str) -> str:
    """Convert given snake_case string to camelCase string."""
    components = value.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
