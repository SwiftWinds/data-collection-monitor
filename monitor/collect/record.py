
from monitor.collect.const import RECORD_TABLE
from monitor.collect.metrics import get_cpu_usage, get_disk_usage, \
    get_mem_usage, get_total_interface_packets_dropped_this_session, \
    get_total_packets_received_this_session


class Record:
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
        # The percentage of disk used.
        self.disk_used = get_disk_usage()

        # Whether this record is writable to the database.
        self._writable = True
        # How many packets have been received so far in this session.
        self._total_packets_received_so_far = \
            get_total_packets_received_this_session()
        # How many incoming interface packets have been dropped so far in this session.
        self._total_packets_dropped_so_far = \
            get_total_interface_packets_dropped_this_session()
        if previous:
            # The number of packets received in the last timestep. Does NOT
            # correlate to the number of packets received since the previous
            # timestamp in the table.
            self.packets_received = self._total_packets_received_so_far - \
                previous._total_packets_received_so_far
            # The rate at which packets have been received, in packets per
            # second.
            self.packet_receipt_rate = \
                self.packets_received / (self.timestamp - previous.timestamp)
            # The number of interface packets dropped in the last timestep.
            # Does NOT correlate to the number of interface packets dropped
            # since the previous timestamp in the table.
            self.packets_dropped = self._total_packets_dropped_so_far - \
                previous._total_packets_dropped_so_far
        else:
            self._writable = False

    def write(self, ctx):
        """Write this record to the passed database context."""
        if self._writable:
            ctx.execute(
                f'INSERT INTO {RECORD_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?);',
                (
                    self.timestamp,
                    self.cpu_used,
                    self.mem_used,
                    self.disk_used,

                    self.packets_received,
                    self.packet_receipt_rate,
                    self.packets_dropped,
                ),
            )
