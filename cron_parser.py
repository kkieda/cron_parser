#!/usr/bin/env python

import argparse
from parser import StringJobFactory

from printer import JobPrinter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="cron_line",
        help="Cron string e.g. '*/15 0 1,15 * 1-5 /usr/bin/find'",
    )
    return parser.parse_args()


def main(cron_line: str):
    job = StringJobFactory(cron_line).create()
    JobPrinter().print_job(job)


if __name__ == "__main__":
    args = parse_args()
    main(args.cron_line)
