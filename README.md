# data-collection-monitor #
Data collection for UCSB SNL servers.
```console
usage: snl-monitor [-h] [-s TIMESTEP] [-p]
                   [--pruning-frequency PRUNING_FREQUENCY]
                   [--pruning-threshold PRUNING_THRESHOLD]
                   db

positional arguments:
  db                    Location of the database where packet loss data will
                        be stored.

optional arguments:
  -h, --help            show this help message and exit
  -s TIMESTEP, --timestep TIMESTEP
                        How often to poll for new stats, in seconds.
  -p, --prune           Prune old entries from the database.
  --pruning-frequency PRUNING_FREQUENCY
                        How often to prune outdated records from the table, in
                        multiples of the timestep.
  --pruning-threshold PRUNING_THRESHOLD
                        Minimum age for records to be kept while pruning old
                        records, in seconds.
```

## Installation ##
The application is built using `setuptools`, `wheel`, and a build tool such as
`build`. After installing `build`, `setuptools`, and `wheel`, run:
```console
$ python3 -m pip install .
```
You will then be able to run the application as `snl-monitor`.

## Development ##
Set up for development with:

```console
$ python3 -m pip install -e .
```

## Dependencies ##
- [`psutil`](https://pypi.org/project/psutil/)
