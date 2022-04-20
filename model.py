from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Schedule:
    ALL_MINUTES = set(range(0, 60))
    ALL_HOURS = set(range(0, 24))
    ALL_DAYS_OF_MONTH = set(range(1, 32))
    ALL_MONTHS = set(range(1, 13))
    ALL_DAYS_OF_WEEK = set(range(0, 7))

    minutes: list[int]
    hours: list[int]
    days_of_month: list[int]
    months: list[int]
    days_of_week: list[int]

    def _validate(self):
        if not self.minutes or not all(v in self.ALL_MINUTES for v in self.minutes):
            raise ValueError("Invalid schedule minutes")

        if not self.hours or not all(v in self.ALL_HOURS for v in self.hours):
            raise ValueError("Invalid schedule hours")

        if not self.days_of_month or not all(
            v in self.ALL_DAYS_OF_MONTH for v in self.days_of_month
        ):
            raise ValueError("Invalid schedule days of month")

        if not self.months or not all(v in self.ALL_MONTHS for v in self.months):
            raise ValueError("Invalid schedule months")

        if not self.days_of_week or not all(
            v in self.ALL_DAYS_OF_WEEK for v in self.days_of_week
        ):
            raise ValueError("Invalid schedule days of week")

    def __post_init__(self):
        self._validate()


class ScheduleFactory(ABC):
    @abstractmethod
    def create(self) -> Schedule:
        pass


@dataclass
class Job:
    command: str
    schedule: Schedule


class JobFactory(ABC):
    @abstractmethod
    def create(self) -> Job:
        pass
