from io import StringIO
from unittest.mock import patch

from src.model import Job, Schedule
from src.printer import JobPrinter


def test_printer_should_print_in_correct_format():
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

    with patch("sys.stdout", new=StringIO()) as fake_out:
        JobPrinter().print_job(job)
        assert (
            fake_out.getvalue()
            == """minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
"""
        )
