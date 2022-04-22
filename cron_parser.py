#!/usr/bin/env python

import argparse

from src.formatter import JobFormatter
from src.parser import JobParser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="cron_line", help="Cron string e.g. '*/15 0 1,15 * 1-5 /usr/bin/find'"
    )
    return parser.parse_args()


def main(cron_line: str):
    job = JobParser().parse(cron_line)
    job_str = JobFormatter().format_job(job)
    print(job_str)


if __name__ == "__main__":
    args = parse_args()
    main(args.cron_line)
