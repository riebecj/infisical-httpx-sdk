"""Infisical HTTPX SDK Exceptions."""


class InfisicalCredentialsError(Exception):
    """Base `Exception` for raising Infisical credentials errors."""


class InfisicalHTTPError(Exception):
    """Infisical API HTTP Error."""

    def __init__(self, err_json: dict) -> None:
        """Initialize the Infisical HTTP error.

        Parses the `message`, `statusCode`, *optional* `details`, and the [error type][^.__err_type__] from
        the error JSON response and formats them into a more detailed `Exception`.

        Args:
            err_json (dict): The error JSON response from the server.
        """
        message = err_json["message"]
        status_code = err_json["statusCode"]
        details = err_json.get("details")
        msg = f"{self.__err_type__(status_code)} {status_code}: {message}"
        if details:
            msg += f" - {details}"
        super().__init__(msg)

    def __err_type__(self, status_code: int) -> str:
        """Return the error type based on the status code.

        This provides more context in the exception that's raised by specifying
        if it's a `Client Error` or `Server Error` based on status code.

        Returns:
            (str): The error type. Specifically, `Client Error` or `Server Error`.
        """
        if 400 <= status_code <= 499:  # noqa: PLR2004
            return "Client Error"
        return "Server Error"


class InfisicalResourceError(Exception):
    """Custom exception for Infisical resource errors.

    Works like any other `Exception`. Pass a `str` message to the constructor and it will be raised.
    """
