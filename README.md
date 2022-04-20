# Cron Expression Parser

Script which parses a cron string and expands each field to show the times at which it will run.

### Requirements

    Python >= 3.10

### Basic usage

    ./cron_parser.py '*/10 0 1,13 * 1-5 /usr/bin/find -a'

### Example output

    minute        0 10 20 30 40 50
    hour          0
    day of month  1 13
    month         1 2 3 4 5 6 7 8 9 10 11 12
    day of week   1 2 3 4 5
    command       /usr/bin/find -a


### Dev setup in virtual environment

    pip install -r requirements-dev.txt


### Running test suite

    tox
