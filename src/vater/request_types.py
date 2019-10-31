"""This module contains logic for different API request types."""
import datetime
from typing import List, Tuple, Union

import requests
from requests import Response

from vater.errors import (
    ERROR_CODE_MAPPING,
    InvalidRequestData,
    MaximumArgumentsNumberExceeded,
    UnknownExternalApiError,
)
from vater.models import Subject, SubjectSchema


class RequestType:
    """Base class for all request types."""

    def __init__(self, url_pattern: str, *args, **kwargs) -> None:
        """Initialize instance parameters."""
        self.url_pattern = url_pattern
        self.args = None
        self.kwargs = None

    def _get_url(self) -> None:
        """Interpolate endpoint url."""
        url = self.url_pattern

        if self.kwargs["date"] is None:  # type: ignore
            self.kwargs["date"] = datetime.date.today()  # type: ignore

        for key, value in self.kwargs.items():  # type: ignore
            if f"{{{key}}}" in self.url_pattern:
                if isinstance(value, (str, datetime.date)):
                    url = url.replace(f"{{{key}}}", str(value))
                else:
                    url = url.replace(f"{{{key}}}", ",".join(value))

        self.url = self.args[0].base_url + url  # type: ignore

    def register_args(self, *args, **kwargs):
        """Register parameters to the instance."""
        self.args = args
        self.kwargs = kwargs

    def validate(self) -> None:
        """Validate registered parameters."""

    def send_request(self) -> Response:
        """Get response from the API."""
        self._get_url()
        response = requests.get(self.url)

        if response.status_code == 400:
            raise InvalidRequestData(ERROR_CODE_MAPPING[response.json()["code"]])
        elif response.status_code != 200:
            raise UnknownExternalApiError(response.status_code, response.text)

        return response

    def result(self):
        """Return request result."""


class CheckRequest(RequestType):
    """Class for check requests type."""

    def result(self) -> Union[dict, Tuple[bool, str]]:
        """Return check result if account is assigned to the subject and request id."""
        response = self.send_request()

        if self.kwargs.get("raw"):  # type: ignore
            return response.json()

        result = response.json()["result"]

        return result["accountAssigned"] == "TAK", result["requestId"]


class SearchRequest(RequestType):
    """Class for search requests type."""

    PARAM_LIMIT = 30

    def __init__(self, url_pattern: str, many: bool = False) -> None:
        """Initialize additional `many` attribute."""
        super().__init__(url_pattern)
        self.many = many

    def validate(self) -> None:
        """Validate given parameters."""
        if not self.many:
            return

        parameter = ({*self.kwargs} - {"raw", "date"}).pop()  # type: ignore

        if len(self.kwargs[parameter]) > self.PARAM_LIMIT:  # type: ignore
            raise MaximumArgumentsNumberExceeded(parameter, self.PARAM_LIMIT)

    def result(self) -> Union[dict, Tuple[Union[List[Subject], Subject], str]]:
        """Return subject/subjects mapped to the specific parameter and request id."""
        self.validate()

        response = self.send_request()

        if self.kwargs.get("raw"):  # type: ignore
            return response.json()

        result = response.json()["result"]
        subjects = SubjectSchema().load(
            result["subjects" if self.many else "subject"], many=self.many
        )

        return subjects, result["requestId"]
