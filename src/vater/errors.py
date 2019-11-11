"""Errors module."""

from typing import Optional

# Following code mapping comes from API docs
ERROR_CODE_MAPPING = {
    "WL-100": "Unexpected server error.",
    "WL-101": "Date cannot be empty.",
    "WL-102": "Date has invalid format. YYYY-MM-DD allowed.",
    "WL-103": "Date cannot be future date.",
    "WL-104": "REGON cannot be empty.",
    "WL-105": "REGON has invalid length. 9 or 14 character required.",
    "WL-106": "REGON contains invalid characters. Only digits are allowed.",
    "WL-107": "Invalid REGON.",
    "WL-108": "Account cannot be empty.",
    "WL-109": "Account has invalid length. 26 digits required.",
    "WL-110": "Account contains invalid characters. Only digits are allowed.",
    "WL-111": "Invalid account.",
    "WL-112": "NIP cannot be empty.",
    "WL-113": "NIP has invalid length. 10 digits required.",
    "WL-114": "NIP is invalid type. Only digits are allowed.",
    "WL-115": "NIP is invalid.",
    "WL-118": "Date has value preceding registry range.",
    "WL-130": "Max request arguments exceeded",
    "WL-190": "Invalid Request.",
    "WL-195": "Database has been updated. Send a request again.",
    "WL-196": "Database is being updated, Try again later.",
}


class ApiError(Exception):
    """Base class for all API errors."""


class InvalidRequestData(ApiError):
    """Base class for invalid request errors."""


class InvalidField(InvalidRequestData):
    """Raised if known error from external API is returned."""


class UnknownExternalApiError(Exception):
    """Raised when unknown error from vat register site occurs."""

    def __init__(self, status_code: int, data: Optional[str]) -> None:
        """Assign status code and data to the instance."""
        self.status_code = status_code
        self.data = data

    def __str__(self) -> str:
        """Get error representation."""
        return (
            f"{self.__class__.__name__}: status code: {self.status_code}, "
            f"data: {self.data}"
        )


class ClientError(Exception):
    """Base class for all vater client errors."""


class MaximumParameterNumberExceeded(ClientError):
    """Raised when arguments number exceeds allowed maximum."""

    def __init__(self, param: str, maximum: int) -> None:
        """Assign parameter name."""
        self.param = param
        self.maximum = maximum

    def __str__(self) -> str:
        """Get error representation."""
        return (
            f"{self.__class__.__name__}: number of {self.param} "
            f"exceeds allowed maximum: {self.maximum}"
        )


class ValidationError(ClientError):
    """Raised during parameter validation."""

    def __init__(self, param, msg) -> None:
        """Initialize the instance."""
        self.param = param
        self.msg = msg

    def __str__(self) -> str:
        """Get validation error representation."""
        return f"{self.__class__.__name__}: {self.param} {self.msg}"
