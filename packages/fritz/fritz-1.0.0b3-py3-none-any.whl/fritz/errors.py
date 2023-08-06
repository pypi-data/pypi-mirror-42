"""
fritz.errors
~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""


class FritzError(Exception):
    """Generic Exception class for Fritz Errors."""

    def __init__(self, message, status_code=None):
        """
        Args:
            message (str): Error message
            status_code (Optional[int]): Status Code of response.
        """
        super().__init__(message)
        self._message = message
        self.status_code = status_code

    def __str__(self):
        return self._message or "<empty message>"

    def __repr__(self):
        cls_name = self.__class__.__name__

        return (
            f"{cls_name}(message={self._message} "
            f"status_code={self.status_code})"
        )


class FritzNotInitializedError(FritzError):
    """Error when Python SDK not initialized."""

    def __init__(self):
        message = (
            "`fritz.configure` not called.  Please call "
            "`fritz.configure` with your API Key and Project UID."
        )
        super().__init__(message)


class InvalidFritzConfigError(FritzError):
    """Error when Fritz config contains invalid options."""

    def __init__(self, path):
        message = (
            f"Fritz configuration file at {path} contains invalid options"
        )
        super().__init__(message)
