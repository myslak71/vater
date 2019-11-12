"""Schemas and models module."""
import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from marshmallow import Schema, fields, post_load


@dataclass
class Company:
    """Class representing company in vat payers register."""

    company_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    nip: Optional[str]
    pesel: Optional[str]


class CompanySchema(Schema):
    """Schema for company entity."""

    company_name = fields.String(data_key="companyName", required=True, allow_none=True)
    first_name = fields.String(data_key="firstName", required=True, allow_none=True)
    last_name = fields.String(data_key="lastName", required=True, allow_none=True)
    nip = fields.String(required=True, allow_none=True)
    pesel = fields.String(allow_none=True, required=True)

    @post_load
    def make_company(self, data: Dict[str, str], **kwargs: Any) -> Company:
        """Create a company instance."""
        return Company(**data)


@dataclass
class Subject:
    """Class representing subject in vat payers register."""

    name: str
    nip: Optional[str]
    status_vat: Optional[str]
    regon: Optional[str]
    pesel: Optional[str]
    krs: Optional[str]
    residence_address: Optional[str]
    working_address: Optional[str]
    representatives: Optional[List[Company]]
    authorized_clerks: Optional[List[Company]]
    partners: Optional[List[Company]]
    registration_legal_date: Optional[datetime.date]
    registration_denial_basis: Optional[str]
    registration_denial_date: Optional[datetime.date]
    restoration_basis: Optional[str]
    restoration_date: Optional[datetime.date]
    removal_basis: Optional[str]
    removal_date: Optional[datetime.date]
    account_numbers: Optional[List[str]]
    has_virtual_accounts: Optional[bool]


class SubjectSchema(Schema):
    """Schema for subject entity."""

    name = fields.String()
    nip = fields.String(allow_none=True)
    status_vat = fields.String(data_key="statusVat", allow_none=True)
    regon = fields.String(allow_none=True)
    pesel = fields.String(allow_none=True)
    krs = fields.String(allow_none=True)
    residence_address = fields.String(data_key="residenceAddress", allow_none=True)
    working_address = fields.String(data_key="workingAddress", allow_none=True)
    representatives = fields.List(fields.Nested(CompanySchema), allow_none=True)
    authorized_clerks = fields.List(
        fields.Nested(CompanySchema), data_key="authorizedClerks", allow_none=True
    )
    partners = fields.List(fields.Nested(CompanySchema))
    registration_legal_date = fields.Date(
        data_key="registrationLegalDate", allow_none=True
    )
    registration_denial_basis = fields.String(
        data_key="registrationDenialBasis", allow_none=True
    )
    registration_denial_date = fields.Date(
        data_key="registrationDenialDate", allow_none=True
    )
    restoration_basis = fields.String(data_key="restorationBasis", allow_none=True)
    restoration_date = fields.Date(data_key="restorationDate", allow_none=True)
    removal_basis = fields.String(data_key="removalBasis", allow_none=True)
    removal_date = fields.Date(data_key="removalDate", allow_none=True)
    account_numbers = fields.List(
        fields.String(), data_key="accountNumbers", allow_none=True
    )
    has_virtual_accounts = fields.Boolean(
        data_key="hasVirtualAccounts", allow_none=True
    )

    @post_load
    def make_subject(self, data: dict, **kwargs: Any) -> Subject:
        """Create a subject instance."""
        return Subject(**data)
