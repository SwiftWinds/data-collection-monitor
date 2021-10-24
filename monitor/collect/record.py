
import logging

from monitor.const import FIELD_SEPARATOR, MESSAGE_FORMAT, RECORD_TABLE
from monitor.collect.metrics import get_cpu_usage, get_disk_usage, \
    get_mem_usage, get_total_interface_packets_dropped_this_session, \
    get_total_packets_received_this_session


class Record:
    """A record of monitoring data."""

    def __init__(self, timestamp, timestep, previous=None):
        """
        Create a new monitor record for the given timestamp.

        :param timestamp: The current timestamp.
        :param timestep: The timestep that the monitor is running at.
        :param previous: The previous monitor record. If none is given, then
            this monitor record is taken to be for the purpose of attaining the
            packet receipt rate, and cannot be written to the database.
        """
        # The timestamp corresponding to this record.
        self.timestamp = timestamp
        # The timestep this record covers.
        self.timestep = timestep
        # The percentage of the CPU used.
        self.cpu_used = get_cpu_usage()
        # The percentage of memory used.
        self.mem_used = get_mem_usage()
        # The percentage of disk used.
        self.disk_used = get_disk_usage()

        # Whether this record is sendable. Is false for the first record
        # generated, since that record is only used to get a baseline for
        # the packet-related attributes.
        self._sendable = True
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
            self._sendable = False

    def send(self, sock):
        """Send the data in this record to the passed socket."""
        if self._sendable:
            try:
                sock.sendall(self.as_message().encode(MESSAGE_FORMAT))
            except Exception as e:
                logging.error(
                    f'An error was encountered while sending record data: {e}')

    def as_message(self) -> str:
        """
        Return the data in this ``Record`` in a format for sending to the
        listener. Returns an empty string if this record is not sendable
        (i.e., it is the initial record used to calculate the first packet
        receipt and loss values).
        """
        if self._sendable:
            return FIELD_SEPARATOR.join(map(str, [
                self.timestamp,
                self.timestep,

                self.cpu_used,
                self.mem_used,
                self.disk_used,

                self.packets_received,
                self.packet_receipt_rate,
                self.packets_dropped
            ]))
        else:
            return ''
