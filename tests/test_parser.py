from parser import ScheduleNumberParser, StringJobFactory, StringScheduleFactory

import pytest


@pytest.fixture
def schedule_number_parser():
    return ScheduleNumberParser(list(range(1, 11)))


def test_schedule_number_parser_should_parse_integers(schedule_number_parser):
    values = schedule_number_parser.parse("10")

    assert values == [10]


def test_schedule_number_parser_should_parse_asterisk(schedule_number_parser):
    values = schedule_number_parser.parse("*")

    assert values == list(range(1, 11))


def test_schedule_number_parser_should_parse_range(schedule_number_parser):
    values = schedule_number_parser.parse("0-30")

    assert values == list(range(0, 31))


@pytest.mark.parametrize("input_string", ["-", "-30", "20-", "a-20"])
def test_schedule_number_parser_should_not_parse_invalid_range(
    schedule_number_parser, input_string
):
    with pytest.raises(ValueError):
        schedule_number_parser.parse(input_string)


def test_string_schedule_factory_should_not_parse_no_values():
    string_schedule_factory = StringScheduleFactory("* * * * 5-1")

    with pytest.raises(ValueError):
        schedule = string_schedule_factory.create()
        print(schedule.minutes, schedule.days_of_week)


@pytest.mark.parametrize(
    "input_string",
    [
        "-1 * * * *",
        "60 * * * *",
        "* -1 * * *",
        "* 24 * * *",
        "* * 0 * *",
        "* * 32 * *",
        "* * * 0 *",
        "* * * 13 *",
        "* * * * -1",
        "* * * * 7",
    ],
)
def test_string_schedule_factory_should_not_parse_invalid_values(input_string):
    string_schedule_factory = StringScheduleFactory(input_string)

    with pytest.raises(ValueError):
        string_schedule_factory.create()


@pytest.mark.parametrize(
    "input_string,command,minutes",
    [
        ("*/15 0 1,15 * 1-5 /usr/bin/find", "/usr/bin/find", [0, 15, 30, 45]),
        (
            "* 0,2 1,15 * 1-5 /usr/bin/find -a",
            "/usr/bin/find -a",
            list(range(0, 60)),
        ),
        ("15 0 15 2 1-5 /usr/bin/find a bc ", "/usr/bin/find a bc", [15]),
    ],
)
def test_string_job_factory_should_parse_valid_string(input_string, command, minutes):
    job_factory = StringJobFactory(input_string)

    job = job_factory.create()
    assert job.command == command
    assert job.schedule.minutes == minutes


@pytest.mark.parametrize(
    "input_string",
    [
        "invalid",
        "*/15 0 1,15 * 1-5 ",
        "* 0,2 1,15 w 1-5 /usr/bin/find",
        "1555 0 15 2 1-5 /usr/bin/find",
        "1555 0 15 , 1-5 /usr/bin/find",
        "1555 0 15 2 - /usr/bin/find",
    ],
)
def test_string_job_factory_should_not_parse_invalid_string(input_string):
    job_factory = StringJobFactory(input_string)

    with pytest.raises(ValueError):
        job_factory.create()
