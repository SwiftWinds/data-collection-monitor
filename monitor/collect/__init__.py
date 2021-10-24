import argparse
import pathlib
import sqlite3
import time

from monitor.collect.const import DEFAULT_PRUNING_FREQUENCY, \
    DEFAULT_PRUNING_THRESHOLD, DEFAULT_TIMESTEP, RECORD_TABLE
from monitor.collect.record import Record
from monitor.util.functional import throttle
from monitor.util.subcommand import Subcommand


def create_table(ctx):
    """
    Create the table for the monitoring records, if it does not already exist.
    """
    ctx.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {RECORD_TABLE} (
            -- The timestamp corresponding to this record, in UTC time.
            timestamp TEXT,
            -- The percentage of the CPU used.
            cpu_used REAL,
            -- The percentage of memory used.
            mem_used REAL,
            -- The percentage of disk used.
            disk_used REAL,

            -- The number of packets received since the last timestep. Does NOT
            -- correlate to the number of packets received since the previous
            -- timestamp in the table.
            packets_received INTEGER,
            -- The rate at which packets have been received, in packets per
            -- second.
            packet_receipt_rate REAL,
            -- The number of interface packets dropped in the last timestep.
            -- Does NOT correspond to the number of interface packets dropped
            -- since the previous timestamp in the table.
            packets_dropped INTEGER,

            PRIMARY KEY (timestamp)
        );'''
    )


def prune_old_records(ctx, max_age):
    """Prunes old records from the database."""
    ctx.execute(
        f'''
        DELETE FROM {RECORD_TABLE} WHERE
            strftime('%s', 'now') - timestamp > ?
        ;''',
        (max_age,)
    )


class Collect(Subcommand):
    """Collect metrics for monitoring."""

    def entry_point(self, args: argparse.Namespace) -> int:
        ctx = sqlite3.connect(args.db)

        pruning_frequency = 0 if not args.prune else args.pruning_frequency
        prune = throttle(prune_old_records, pruning_frequency)

        with ctx:
            create_table(ctx)
            # SQLite for Python is set up to execute batches of statements, so
            # we need to manually tell it to update the database.
            ctx.commit()

            previous = time.time()
            previous_rec = Record(previous)
            while True:
                now = time.time()
                # lock the loop to the system clock
                # https://stackoverflow.com/a/25251804
                time.sleep(args.timestep - (now - previous) % args.timestep)

                rec = Record(time.time(), previous_rec)
                rec.write(ctx)
                previous_rec = rec

                prune(ctx, args.pruning_threshold)

                ctx.commit()

    def arguments(self, parser: argparse.ArgumentParser):
        """Adds arguments for ``monitor collect``."""
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
