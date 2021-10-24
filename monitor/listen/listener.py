
import logging
import socket
import sqlite3
import typing

from monitor.collect.record import Record
from monitor.const import CONNECTION_MESSAGE, FIELD_SEPARATOR, LOCALHOST, MESSAGE_FORMAT, RECORD_TABLE

# buffer size for messages, in bytes
BUFFER_SIZE: int = 2048


def write_to_db(ctx: sqlite3.Connection, address, data: typing.List[str]):
    """
    Write the data from the decoded message to the database.

    Assumes that the data is in the order:

    ``address``
        The address of the machine this record is for.

    ``timestamp``
        The timestamp corresponding to this record.

    ``timestep``
        The timestep this record covers.

    ``cpu_used``
        The percentage of the CPU used.

    ``mem_used``
        The percentage of memory used.

    ``disk_used``
        The percentage of disk used.

    ``packets_received``
        The number of packets received in the last timestep. Does NOT correlate
        to the number of packets received since the previous timestamp in the
        table.

    ``packet_receipt_rate``
        The rate at which packets have been received, in packets per second.

    ``packets_dropped``
        The number of incoming interface packets dropped in the last timestep.
        Does NOT correlate to the number of packets dropped since the previous
        timestamp in the table.
    """
    ctx.execute(
        f'''
        INSERT INTO {RECORD_TABLE} VALUES (
            ?,  -- address
            ?,  -- timestamp
            ?,  -- timestep

            ?,  -- cpu_used
            ?,  -- mem_used
            ?,  -- disk_used

            ?,  -- packets_received
            ?,  -- packet_receipt_rate
            ?   -- packets_dropped
        );''', (address, *data))


class Listener:
    """
    Listens to a given port for data to store in the passed db context.
    """

    def __init__(self, port: int):
        self.host = LOCALHOST
        self.port = port

        # initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind socket to port and connect
        self.socket.bind((self.host, self.port))

        self.connected = True
        self.connected_devices = 0

    def store(self, ctx: sqlite3.Connection) -> bool:
        """
        Store any new messages in the passed database. Returns whether or not to
        continue listening.
        """
        if not self.connected:
            return False

        message, sender_address = self.socket.recvfrom(BUFFER_SIZE)
        sender_host, _sender_port = sender_address

        if message:
            decoded = message.decode(MESSAGE_FORMAT)
        else:
            logging.error('No message was received.')
            return False

        if decoded == CONNECTION_MESSAGE:
            self.connected_devices += 1
            logging.info('A new device has started sending information.')
            return True

        data = decoded.split(FIELD_SEPARATOR)
        write_to_db(ctx, sender_host, data)

        return True
