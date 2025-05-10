"""Infisical exceptions module."""


class InfisicalHTTPError(Exception):
    """Infisical HTTP error."""

    def __init__(self, err_json: dict) -> None:
        """Initialize the Infisical HTTP error.

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
        """Return the error type based on the status code."""
        if 400 <= status_code <= 499:  # noqa: PLR2004
            return "Client Error"
        return "Server Error"


class InfisicalResourceError(Exception):
    """Custom exception for Infisical resource errors."""
