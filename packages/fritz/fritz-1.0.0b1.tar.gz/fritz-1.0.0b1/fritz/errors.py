"""
fritz.errors
~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""


class FritzError(Exception):
    """Generic Exception class for Fritz Errors."""

    def __init__(self,
                 message,
                 status_code=None):
        """
        Args:
            message (str): Error message
            status_code (Optional[int]): Status Code of response.
        """
        super(FritzError, self).__init__(message)
        self._message = message
        self.status_code = status_code

    def __str__(self):
        return self._message or "<empty message>"

    def __repr__(self):
        return "%s(message=%r, status_code=%r)" % (
            self.__class__.__name__,
            self._message,
            self.status_code,
        )


class FritzNotInitializedError(FritzError):
    """Error when Python SDK not initialized."""
    def __init__(self):
        message = ("`fritz.configure` not called.  Please call "
                   "`fritz.configure` with your API Key and Project UID.")
        super(FritzNotInitializedError, self).__init__(self, message)
