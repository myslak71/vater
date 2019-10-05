"""Errors module."""

from typing import Optional

ERROR_CODE_MAPPING = {
    "WL-100": "Unexpected server error.",
    "WL-101": "Field `date` cannot be empty.",
    "WL-102": "Field `date` has invalid format. YYYY-MM-DD allowed.",
    "WL-103": "Field `date` cannot be feature date.",
    "WL-112": "Field `NIP` cannot be empty.",
    "WL-113": "Field `NIP` has invalid length. 10 digits required.",
    "WL-114": "Field `NIP` is invalid type. Only digits are allowed.",
    "WL-115": "Field `NIP` is invalid.",
    "WL-118": "Field `date` has value preceding registry range.",
    "WL-130": "Max request arguments exceeded",
    "WL-190": "Invalid Request.",
    "WL-195": "Database has been updated. Send a request again.",
    "WL-196": "Database is being updated, Try again later.",
}


class InvalidRequestData(Exception):
    """Base class for invalid request errors."""


class InvalidField(InvalidRequestData):
    """Raised if known error from external API is returned."""


class InvalidNipsNumber(InvalidRequestData):
    """Raised when number of nips is invalid."""


class UnknownExternalApiError(Exception):
    """Raised when unknown error from vat register site occurs."""

    def __init__(self, status_code: int, data: Optional[str]) -> None:
        """Assign status code and data to the instance."""
        self.status_code = status_code
        self.data = data

    def __repr__(self) -> str:
        """Get error representation."""
        return (
            f"{self.__class__.__name__}: status code: {self.status_code}, "
            f"data: {self.data}"
        )
