from src.formatter import JobFormatter
from src.model import Job, Schedule


def test_formatter_should_return_correct_string():
    job = Job(
        command="/usr/bin/find",
        schedule=Schedule(
            minutes=[0, 15, 30, 45],
            hours=[0],
            days_of_month=[1, 15],
            months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            days_of_week=[1, 2, 3, 4, 5],
        ),
    )

    job_str = JobFormatter().format_job(job)
    assert (
        job_str
        == """minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find"""
    )
