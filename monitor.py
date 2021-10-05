
import argparse
import pathlib
import sqlite3


# Name of the record table.
RECORD_TABLE = 'monitor_record'


class MonitorRecord:
    """A record of data held by the """

    def __init__(self, timestamp, cpu_used, mem_used, packets_lost):
        self.timestamp = timestamp
        self.cpu_used = cpu_used
        self.mem_used = mem_used
        self.packets_lost = packets_lost

    def write(self, ctx):
        """Write this record to the passed database context."""
        ctx.execute(
            f'INSERT INTO {RECORD_TABLE} VALUES (?, ?, ?, ?);',
            (self.timestamp,
            self.cpu_used,
            self.mem_used,
            self.packets_lost)
        )


def main(args: argparse.Namespace):
    ctx = sqlite3.connect(args.db)

    with ctx:
        ctx.execute(f'''CREATE TABLE IF NOT EXISTS {RECORD_TABLE} (
            timestamp TEXT,
            cpu_used REAL,
            mem_used REAL,
            packets_lost INTEGER,

            PRIMARY KEY (timestamp)
        );''')
        ctx.commit()

        rec_1 = MonitorRecord('2021-10-04T09:39:01', 50, 78, 2000)
        rec_2 = MonitorRecord('2021-10-05T02:39:40', 23, 2, 20000)
        rec_3 = MonitorRecord('2021-10-06T17:22:03', 80, 17, 42)

        rec_1.write(ctx)
        rec_2.write(ctx)
        rec_3.write(ctx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'db',
        type=pathlib.Path,
        help='Location of the database where packet loss data will be stored.'
    )
    main(parser.parse_args())
