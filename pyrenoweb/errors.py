"""Define package errors."""


class RenowebError(Exception):
    """Define a base error."""

    pass


class InvalidApiKey(RenowebError):
    """Define an error related to invalid or missing API key."""

    pass


class RequestError(RenowebError):
    """Define an error related to invalid requests."""

    pass


class ResultError(RenowebError):
    """Define an error related to the result returned from a request."""

    pass


class MunicipalityError(RenowebError):
    """Define an error if municipality is not supported by the API."""

    pass
