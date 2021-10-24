"""
Monitor server statistics.

Dependencies:
* ``psutil``: https://pypi.org/project/psutil/
"""
import argparse
import sys
import typing

import monitor.collect as collect
from monitor.util.subcommand import Subcommand

# List of available subcommands' constructors.
SUBCOMMAND_CONSTRUCTORS = [collect.Collect]


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='which', required=True)

    subcommands = subcommand_mapping([constructor(subparsers)
                                      for constructor in SUBCOMMAND_CONSTRUCTORS])

    args = parser.parse_args()
    return subcommands[args.which](args)


SubcommandEntryPoint = typing.Callable[[argparse.Namespace], int]


def subcommand_mapping(subcommand_objects: typing.List[Subcommand]) -> typing.Dict[str, SubcommandEntryPoint]:
    """Map subcommand names to entry points."""
    return {
        subcommand.name: subcommand.entry_point for subcommand in subcommand_objects
    }


if __name__ == '__main__':
    sys.exit(main())
