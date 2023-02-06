"""Schemas and models module."""
import datetime
from enum import Enum

from pydantic import Field, validator
from pydantic.main import BaseModel


class EntityPerson(BaseModel):
    """Class representing company in VAT payers register."""

    company_name: str | None = Field(..., alias="companyName")
    first_name: str | None = Field(..., alias="firstName")
    last_name: str | None = Field(..., alias="lastName")
    nip: str | None
    pesel: str | None

    class Config:
        allow_population_by_field_name = True


class Subject(BaseModel):
    """Class representing subject in VAT payers register."""

    name: str
    nip: str | None
    status_vat: str | None = Field(..., alias="statusVat")
    regon: str | None
    pesel: str | None
    krs: str | None
    residence_address: str | None = Field(..., alias="residenceAddress")
    working_address: str | None = Field(..., alias="workingAddress")
    representatives: list[EntityPerson] | None
    authorized_clerks: list[EntityPerson] | None = Field(..., alias="authorizedClerks")
    partners: list[EntityPerson] | None
    registration_legal_date: datetime.date | None = Field(
        ..., alias="registrationLegalDate"
    )
    registration_denial_basis: str | None = Field(..., alias="registrationDenialBasis")
    registration_denial_date: datetime.date | None = Field(
        ..., alias="registrationDenialDate"
    )
    restoration_basis: str | None = Field(..., alias="restorationBasis")
    restoration_date: datetime.date | None = Field(..., alias="restorationDate")
    removal_basis: str | None = Field(..., alias="removalBasis")
    removal_date: datetime.date | None = Field(..., alias="removalDate")
    account_numbers: list[str] = Field(..., alias="accountNumbers")
    has_virtual_accounts: bool | None = Field(..., alias="hasVirtualAccounts")

    class Config:
        allow_population_by_field_name = True


def validate_request_date_time(cls, value: datetime.datetime) -> datetime.datetime:
    """Validate if `request_date_time` has valid format."""
    if isinstance(value, datetime.datetime):
        return value

    return datetime.datetime.strptime(value, "%d-%m-%Y %H:%M:%S")


class EntityItem(BaseModel):
    """Represents entity item."""

    subject: Subject | None
    request_id: str = Field(..., alias="requestId")
    request_date_time: datetime.datetime = Field(..., alias="requestDateTime")

    _validate_request_date_time = validator(
        "request_date_time", pre=True, allow_reuse=True
    )(validate_request_date_time)

    class Config:
        allow_population_by_field_name = True


class EntityList(BaseModel):
    """Represents entity list."""

    subjects: list[Subject]
    request_id: str = Field(..., alias="requestId")
    request_date_time: datetime.datetime = Field(..., alias="requestDateTime")

    _validate_request_date_time = validator(
        "request_date_time", pre=True, allow_reuse=True
    )(validate_request_date_time)

    class Config:
        allow_population_by_field_name = True


class Entry(BaseModel):
    """Represents single entry in entry list."""

    identifier: str
    subjects: list[Subject]


class EntryList(BaseModel):
    """Represents a list of entries."""

    entries: list[Entry]
    request_id: str = Field(..., alias="requestId")
    request_date_time: datetime.datetime = Field(..., alias="requestDateTime")

    _validate_request_date_time = validator(
        "request_date_time", pre=True, allow_reuse=True
    )(validate_request_date_time)

    class Config:
        allow_population_by_field_name = True


class AccountAssignedEnum(Enum):
    """Represents possible account assigned values."""

    TAK = "TAK"
    NIE = "NIE"


class EntityCheck(BaseModel):
    """Represents single entity check."""

    account_assigned: bool = Field(..., alias="accountAssigned")
    request_id: str = Field(..., alias="requestId")
    request_date_time: datetime.datetime = Field(..., alias="requestDateTime")

    _validate_request_date_time = validator(
        "request_date_time", pre=True, allow_reuse=True
    )(validate_request_date_time)

    class Config:
        allow_population_by_field_name = True

    @validator("account_assigned", pre=True)
    def parse_account_assigned(cls, value: str) -> bool:
        """Get boolean representation of account assigned."""
        if isinstance(value, bool):
            return value

        try:
            return AccountAssignedEnum(value) == AccountAssignedEnum.TAK
        except (TypeError, ValueError):
            raise ValueError(f"Invalid `account_assigned`: {value}")
