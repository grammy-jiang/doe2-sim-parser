import re
from typing import Generator, Iterable, List


def chunks(list_: Iterable, n: int) -> Generator[List, None, None]:
    if list_:
        yield list_[:n]
        yield from chunks(list_[n:], n)


PATTERN_REPORT_HEAD = re.compile(
    r"""
^\x0c(?P<model>.+?)\s+(?P<engine>DOE-2\.\d+\-[\da-z]+)\s+(?P<date>[\/\d]+)\s+(?P<time>\d{1,2}:\d{1,2}:\d{1,2})\s+BDL\sRUN\s*(?P<run_time>\d+)
""",
    flags=re.VERBOSE,
)

PATTERN_REPORT_HOURLY_REPORT = re.compile(
    r"""
HOURLY\sREPORT\-\s(?P<name>.+?)\s+HVAC\s+WEATHER\sFILE-\s(?P<weather>.+?)\s+Pg:\s+(?P<page_no>\d+)\s-\s+(?P<report_no>\d+)
""",
    flags=re.VERBOSE,
)

PATTERN_REPORT_HOURLY_REPORT_HEAD_1 = re.compile(
    r"""
^(MMDDHH|\s{6})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{9})\s{1,3}(.{8,9})
""",
    flags=re.VERBOSE

)

PATTERN_REPORT_HOURLY_REPORT_HEAD_2 = re.compile(
    r"""
\s(DAILY|MONTHLY|YEARLY)\sSUMMARY(\s\(.+\))?
    """,
    flags=re.VERBOSE
)

PATTERN_REPORT_HOURLY_REPORT_CONTENT = re.compile(
    r"""
^(.{6})\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))\s{1,3}(\s*([\d\.\*]+))
    """,
    flags=re.VERBOSE
)

PATTERN_REPORT_TITLE = re.compile(
    r"""
^(?P<report>REPORT)-\s(?P<code>[A-Z\-]{4})\s(?P<name>.+?)\s+(?P<weather>WEATHER\sFILE)-\s(?P<weather_file>.+?)\s+$
""",
    flags=re.VERBOSE,
)


def parse_header(lines: str):
    return (
        list(PATTERN_REPORT_HEAD.search(lines[0]).groupdict().values()),
        list(PATTERN_REPORT_TITLE.search(lines[2]).groupdict().values()),
    )


PATTERN_METER = re.compile(
    r"""(?P<name>.+?)\s+(?P<type_>ELECTRICITY|NATURAL-GAS|STEAM|CHILLED-WATER)""",
    flags=re.VERBOSE,
)
