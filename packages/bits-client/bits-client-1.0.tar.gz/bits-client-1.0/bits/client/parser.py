"""ClientParser class file."""

import argparse

from bits.client.baseclient import BaseClient


class ClientParser(BaseClient):
    """ClientParser class definition."""

    argparse = argparse

    def __init__(self, auth, verbose=False):
        """Initialize a ClientParser instance."""
        BaseClient.__init__(self, auth, verbose)
        # set verbose
        if auth.verbose:
            self.verbose = auth.verbose
