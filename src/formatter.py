from .model import Job


class JobFormatter:
    @staticmethod
    def _get_values_str(values) -> str:
        return " ".join(map(str, values))

    @staticmethod
    def _format_line(name, values_str) -> str:
        return f"{name:13} {values_str}"

    def format_job(self, job: Job) -> str:
        schedule = job.schedule
        lines = [
            self._format_line("minute", self._get_values_str(schedule.minutes)),
            self._format_line("hour", self._get_values_str(schedule.hours)),
            self._format_line(
                "day of month", self._get_values_str(schedule.days_of_month)
            ),
            self._format_line("month", self._get_values_str(schedule.months)),
            self._format_line(
                "day of week", self._get_values_str(schedule.days_of_week)
            ),
            self._format_line("command", job.command),
        ]
        return "\n".join(lines)
