"""Errors module."""

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
    "WL-116": "Field `nazwa podmiotu` cannot be empty.",
    "WL-117": (
        "Field `nazwa podmiotu` is too short - at least 5 characters are required"
    ),
    "WL-118": "Date has value preceding registry range.",
    "WL-130": "Max request arguments exceeded",
    "WL-190": "Invalid Request.",
    "WL-191": "Daily requests limit for this IP has been reached..",
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


class ClientError(Exception):
    """Base class for all vater client errors."""


class InvalidDateError(ClientError):
    """Raised when date validation fails."""


class InvalidNipError(ClientError):
    """Raised when NIP validation fails."""


class InvalidRegonError(ClientError):
    """Raised when REGON validation fails."""


class InvalidAccountError(ClientError):
    """Raised when bank account validation fails."""


class UnexpectedServerResponse(ClientError):
    """Raised when unexpected response is returned from server."""
