import argparse
import logging
import urllib
import socket
import time

from monitor.const import CONNECTION_MESSAGE, DEFAULT_PORT, DEFAULT_TIMESTEP, \
    LOCALHOST, MESSAGE_FORMAT
from monitor.collect.record import Record
from monitor.util.subcommand import Subcommand


class Collect(Subcommand):
    """Collect metrics for monitoring."""

    def entry_point(self, args: argparse.Namespace) -> int:
        # initialize socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind socket to port and connect
        sock.bind((LOCALHOST, args.port))

        dest = urllib.parse.urlsplit('//' + args.destination)
        sock.connect((dest.hostname, dest.port))

        # send a connected message so listener can know how many devices are
        # sending info
        try:
            sock.sendall(CONNECTION_MESSAGE.encode(MESSAGE_FORMAT))
        except Exception as e:
            logging.error('Could not connect: ' + e)
            return 1

        previous = time.time()
        previous_rec = Record(previous, args.timestep)
        while True:
            now = time.time()
            # lock the loop to the system clock
            # https://stackoverflow.com/a/25251804
            time.sleep(args.timestep - (now - previous) % args.timestep)

            rec = Record(time.time(), args.timestep, previous_rec)
            rec.send(sock)
            previous_rec = rec

    def arguments(self, parser: argparse.ArgumentParser):
        """Adds arguments for ``monitor collect``."""
        parser.add_argument(
            'destination',
            help='Destination host and port to send monitoring data to.',
        )
        parser.add_argument(
            '-p', '--port',
            type=int,
            default=DEFAULT_PORT,
            help='Which port to send from.'
        )
        parser.add_argument(
            '-s', '--timestep',
            type=int,
            default=DEFAULT_TIMESTEP,
            help='How often to poll for new stats, in seconds.',
        )
