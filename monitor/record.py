
from . import RECORD_TABLE
from .metrics import get_cpu_usage, get_mem_usage, get_total_packets_received_this_session


class MonitorRecord:
    """A record of monitoring data."""

    def __init__(self, timestamp, previous=None):
        """
        Create a new monitor record for the given timestamp.

        :param timestamp: The current timestamp.
        :param previous: The previous monitor record. If none is given, then
            this monitor record is taken to be for the purpose of attaining the
            packet receipt rate, and cannot be written to the database.
        """
        # The timestamp corresponding to this record.
        self.timestamp = timestamp
        # The percentage of the CPU used.
        self.cpu_used = get_cpu_usage()
        # The percentage of memory used.
        self.mem_used = get_mem_usage()

        # Whether this record is writable to the database.
        self._writable = True
        # How many packets have been received so far in this session.
        self._total_packets_received_so_far = get_total_packets_received_this_session()
        if previous:
            # The number of packets received since the last time step.
            self.packets_received = self._total_packets_received_so_far - \
                previous._total_packets_received_so_far
            # The rate at which packets have been received, in packets per second.
            self.packet_receipt_rate = \
                self.packets_received / (self.timestamp - previous.timestamp)
            # The number of packets lost since the last time step.
            self.kernel_packets_dropped = -1  # TODO: find kernel packets lost
        else:
            self._writable = False

    def write(self, ctx):
        """Write this record to the passed database context."""
        if self._writable:
            ctx.execute(
                f'INSERT INTO {RECORD_TABLE} VALUES (?, ?, ?, ?, ?, ?);',
                (
                    self.timestamp,
                    self.cpu_used,
                    self.mem_used,
                    self.packets_received,
                    self.packet_receipt_rate,
                    self.kernel_packets_dropped,
                ),
            )
