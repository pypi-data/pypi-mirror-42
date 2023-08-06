"""BaseClient class file."""

from bits.client.baseclass import BaseClass


class BaseClient(BaseClass):
    """BaseClient class."""

    def __init__(self, auth, verbose=False):
        """Initialize an BaseClient class instance."""
        BaseClass.__init__(self, verbose)
        self.auth = auth
        # set verbose
        if auth.verbose:
            self.verbose = auth.verbose
