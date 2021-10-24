"""
Common base for subcommands.
"""

import argparse

from monitor.util.string_manip import camel_kebab


class Subcommand():
    def __init__(self, subparsers: argparse._SubParsersAction):
        self.name = camel_kebab(self.__class__.__name__)
        parser = subparsers.add_parser(self.name, help=self.__doc__)
        self.arguments(parser)

    def entry_point(self, _args: argparse.Namespace) -> int:
        """Accepts an ``argparse.Namespace`` and returns a status code."""
        return 0

    def arguments(self, _parser: argparse.ArgumentParser):
        """Add arguments for this subcommand to the passed subparser."""
