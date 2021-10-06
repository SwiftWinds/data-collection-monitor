
# Name of the record table.
RECORD_TABLE: str = 'monitor_record'

# How often to prune outdated records from the table, in multiples of the
# current timestep.
DEFAULT_PRUNING_FREQUENCY: int = 5 * 24 * 60
# Default minimum age for records to be kept while pruning old records, in seconds.
# 432,000 seconds == 5 days
DEFAULT_PRUNING_THRESHOLD = 5 * 24 * 60 * 60
# Default for how often to poll for new stats, in seconds.
DEFAULT_TIMESTEP: int = 30
