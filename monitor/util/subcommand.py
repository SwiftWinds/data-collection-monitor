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

    def arguments(self, parser: argparse.ArgumentParser):
        """Adds arguments for ``monitor listen``."""
        parser.add_argument(
            'db',
            type=pathlib.Path,
            help='Location of the database where packet loss data will be stored.',
        )
        parser.add_argument(
            '-s', '--timestep',
            type=int,
            default=DEFAULT_TIMESTEP,
            help='How often to poll for new stats, in seconds.',
        )
        parser.add_argument(
            '-p', '--prune',
            action='store_true',
            help='Prune old entries from the database.',
        )
        parser.add_argument(
            '--pruning-frequency',
            type=int,
            default=DEFAULT_PRUNING_FREQUENCY,
            help='How often to prune outdated records from the table, in '
            'multiples of the timestep.',
        )
        parser.add_argument(
            '--pruning-threshold',
            type=int,
            default=DEFAULT_PRUNING_THRESHOLD,
            help='Minimum age for records to be kept while pruning old records, '
            'in seconds.',
        )
