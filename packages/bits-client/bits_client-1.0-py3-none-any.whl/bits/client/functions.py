"""ClientFunctions class file."""

from bits.client.baseclass import BaseClass


class ClientFunctions(BaseClass):
    """ClientFunctions class."""

    def __init__(self, verbose=False):
        """Initialize an BaseClient class instance."""
        BaseClass.__init__(self, verbose)

    def run_function(self, function_name, *args):
        """Run a client function by name."""
        getattr(self, function_name)(*args)
