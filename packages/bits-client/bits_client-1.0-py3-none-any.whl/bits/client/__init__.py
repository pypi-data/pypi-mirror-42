"""Client class file."""

import argparse
import sys

from bits.client.baseclient import BaseClient


class Client(BaseClient):
    """Client class."""

    def __init__(self, auth, apps=[]):
        """Initialize an Client class instance."""
        BaseClient.__init__(self, auth)

        # define apps
        self.apps = apps

    def get_args(self):
        """Get the command line arguments."""
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--verbose', help="verbose", action="store_true")
        parser.add_argument('-y', '--yes', help="yes", action="store_true")
        parser.add_argument('app', help="app", choices=self.apps)
        parser.add_argument('args', nargs=argparse.REMAINDER)
        flags = parser.parse_args(sys.argv[1:])

        # check for verbose flag (-v or --verbose)
        if flags.verbose:
            self.auth.verbose = True

        # check for yes flag (-y or --yes)
        if flags.yes:
            self.auth.yes = True

        # check for "verbose" argument
        if 'verbose' in flags.args:
            self.auth.verbose = True
            flags.args.remove('verbose')

        return flags.app, flags.args

    def parse_args(self):
        """Parse the arguments and run the command."""
        # Get app name and arguments
        app_name, app_args = self.get_args()

        # Import the client module
        client = __import__('bitsapiclient.client.%s' % (app_name), fromlist=[app_name])

        # Create a parser
        parser = client.Parser(self.auth)

        # Parse the arguments and run the command
        parser.get_args(app_args)
