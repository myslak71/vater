"""This module contains logic for different API request types."""
import datetime
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Union

import requests
from requests import Response

from vater.errors import (
    ERROR_CODE_MAPPING,
    InvalidRequestData,
    MaximumParameterNumberExceeded,
    UnknownExternalApiError,
)
from vater.models import Subject, SubjectSchema


class RequestType(ABC):
    """Base class for all request types."""

    def __init__(self, url_pattern: str, *args, validators=None, **kwargs) -> None:
        """Initialize instance parameters."""
        self.params: Dict[str, Any] = {}
        self.url_pattern = url_pattern
        self.validators = {} if validators is None else validators
        self.validated_params: dict = {}

    def _get_url(self) -> None:
        """Interpolate endpoint url."""
        url = self.url_pattern

        for key, value in self.validated_params.items():  # type: ignore
            if f"{{{key}}}" in self.url_pattern:
                if isinstance(value, (str, datetime.date)):
                    url = url.replace(f"{{{key}}}", str(value))
                else:
                    url = url.replace(f"{{{key}}}", ",".join(value))

        self.url = self.client.base_url + url  # type: ignore

    def register_params(self, **kwargs: Any) -> None:
        """Register parameters to the instance."""
        self.client = kwargs.pop("client")
        self.params = kwargs

        if self.params["date"] is None:  # type: ignore
            self.params["date"] = datetime.date.today()  # type: ignore

    def validate(self) -> None:
        """Validate given parameters."""
        for param, value in self.params.items():  # type: ignore
            try:
                for validator in self.validators[param]:
                    self.validated_params[param] = validator(value)
            except KeyError:
                self.validated_params[param] = value

    def send_request(self) -> Response:
        """Get response from the API."""
        self._get_url()
        response = requests.get(self.url)

        if response.status_code == 400:
            raise InvalidRequestData(ERROR_CODE_MAPPING[response.json()["code"]])
        elif response.status_code != 200:
            raise UnknownExternalApiError(response.status_code, response.text)

        return response

    @abstractmethod
    def result(self):
        """Return request result."""


class CheckRequest(RequestType):
    """Class for check requests type."""

    def result(self) -> Union[dict, Tuple[bool, str]]:
        """Return check result if account is assigned to the subject and request id."""
        self.validate()
        response = self.send_request()

        if self.params.get("raw"):  # type: ignore
            return response.json()

        result = response.json()["result"]

        return result["accountAssigned"] == "TAK", result["requestId"]


class SearchRequest(RequestType):
    """Class for search requests type."""

    PARAM_LIMIT = 30

    def __init__(self, url_pattern: str, many: bool = False, *args, **kwargs) -> None:
        """Initialize additional `many` attribute."""
        super().__init__(url_pattern, *args, **kwargs)
        self.many = many

    def validate(self) -> None:
        """Validate given parameters."""
        super().validate()

        if not self.many:
            return

        param = ({*self.params} - {"raw", "date"}).pop()  # type: ignore

        if len(self.params[param]) > self.PARAM_LIMIT:  # type: ignore
            raise MaximumParameterNumberExceeded(param, self.PARAM_LIMIT)

    def result(self) -> Union[dict, Tuple[Union[List[Subject], Subject], str]]:
        """Return subject/subjects mapped to the specific parameter and request id."""
        self.validate()
        response = self.send_request()

        if self.params.get("raw"):  # type: ignore
            return response.json()

        result = response.json()["result"]
        subjects = SubjectSchema().load(
            result["subjects" if self.many else "subject"], many=self.many
        )

        return subjects, result["requestId"]
