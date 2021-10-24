
# localhost
LOCALHOST: str = '0.0.0.0'
# Default port to send/receive from.
DEFAULT_PORT: int = 24000

# Path to watch disk usage in.
DU_PATH: str = '/'
# Name of the record table.
RECORD_TABLE: str = 'machine_stats'

# How often to prune outdated records from the table, in multiples of the
# current timestep.
DEFAULT_PRUNING_FREQUENCY: int = 5 * 24 * 60
# Default minimum age for records to be kept while pruning old records, in
# seconds. 432,000 seconds == 5 days
DEFAULT_PRUNING_THRESHOLD: int = 5 * 24 * 60 * 60
# Default for how often to poll for new stats, in seconds.
DEFAULT_TIMESTEP: int = 30


# Message that will be sent when connecting a new monitoring collector to a
# listener.
CONNECTION_MESSAGE: str = 'connected'
# Format to encode messages in.
MESSAGE_FORMAT: str = 'utf-8'
# Field separator in rows sent from the collector to the listener.
FIELD_SEPARATOR: str = '\u001f'
