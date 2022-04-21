from .model import Job


class JobPrinter:
    @staticmethod
    def _get_values_str(values):
        return " ".join(map(str, values))

    @staticmethod
    def _print_line(name, values_str):
        print(f"{name:13} {values_str}")

    def print_job(self, job: Job):
        schedule = job.schedule
        self._print_line("minute", self._get_values_str(schedule.minutes))
        self._print_line("hour", self._get_values_str(schedule.hours))
        self._print_line("day of month", self._get_values_str(schedule.days_of_month))
        self._print_line("month", self._get_values_str(schedule.months))
        self._print_line("day of week", self._get_values_str(schedule.days_of_week))
        self._print_line("command", job.command)
