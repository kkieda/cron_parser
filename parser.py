import re
from typing import Tuple

from model import Job, JobFactory, Schedule, ScheduleFactory


class ScheduleNumberParser:
    def __init__(self, all_values):
        self._all_values = sorted(all_values)

    @staticmethod
    def _parse_divider(input_string: str) -> Tuple[str, int]:
        input_string, divider_str = input_string.split("/")
        divider = int(divider_str)
        return input_string, divider

    @staticmethod
    def _parse_number(input_string: str) -> list[int]:
        try:
            return [int(input_string)]
        except ValueError:
            return []

    @staticmethod
    def _parse_range(input_string: str) -> list[int]:
        range_tokens = input_string.split("-")
        if len(range_tokens) != 2:
            return []
        return list(range(int(range_tokens[0]), int(range_tokens[1]) + 1))

    @staticmethod
    def _parse_list(input_string: str) -> list[int]:
        return [int(v) for v in input_string.split(",")]

    def parse(self, input_string: str) -> list[int]:
        values: list[int] = []
        value_divider = None

        if re.match(r"[\d\-*]+/\d+", input_string):
            input_string, value_divider = self._parse_divider(input_string)

        if input_string == "*":
            values = self._all_values

        elif input_string.isdigit():
            values = self._parse_number(input_string)

        elif "-" in input_string:
            values = self._parse_range(input_string)

        elif "," in input_string:
            values = self._parse_list(input_string)

        if value_divider:
            values = [v for v in values if v % value_divider == 0]

        return values


class StringScheduleFactory(ScheduleFactory):
    def __init__(self, input_string: str):
        self._input_string = input_string
        self._minutes_parser = ScheduleNumberParser(Schedule.ALL_MINUTES)
        self._hours_parser = ScheduleNumberParser(Schedule.ALL_HOURS)
        self._days_of_month_parser = ScheduleNumberParser(Schedule.ALL_DAYS_OF_MONTH)
        self._months_parser = ScheduleNumberParser(Schedule.ALL_MONTHS)
        self._days_of_week_parser = ScheduleNumberParser(Schedule.ALL_DAYS_OF_WEEK)

    def create(self) -> Schedule:
        tokens = self._input_string.split()
        if len(tokens) != 5:
            raise ValueError("Invalid cron line")

        return Schedule(
            minutes=self._minutes_parser.parse(tokens[0]),
            hours=self._hours_parser.parse(tokens[1]),
            days_of_month=self._days_of_month_parser.parse(tokens[2]),
            months=self._months_parser.parse(tokens[3]),
            days_of_week=self._days_of_week_parser.parse(tokens[4]),
        )


class StringJobFactory(JobFactory):
    def __init__(self, input_string: str):
        self._input_string = input_string.strip()

    def create(self) -> Job:
        # standard cron format e.g. '*/15 0 1,15 * 1-5 /usr/bin/find -a'
        if m := re.match(
            r"([*/\d,-]+)\s([*/\d,-]+)\s([*/\d,-]+)\s([*/\d,-]+)\s([*/\d,-]+)\s(.+)",
            self._input_string,
        ):
            *schedule_tokens, command = m.groups()
            schedule = StringScheduleFactory(" ".join(schedule_tokens)).create()
        else:
            raise ValueError("Invalid cron job string")

        return Job(
            command=command,
            schedule=schedule,
        )
