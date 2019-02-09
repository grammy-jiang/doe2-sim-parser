import pprint
import re
from collections import namedtuple
from typing import Generator, Iterable, List

Meter = namedtuple("Meter", ["name", "type_"])
Categories = [[
    "UTILITY-RATE", "RESOURCE", "METERS", "METERED\nENERGY\nUNITS/YR",
    "TOTAL\nCHARGE\n($)", "VIRTUAL\nRATE\n($/UNIT)", "RATE USED\nALL YEAR?"
]]

PATTERN_REPORT_HEAD = re.compile(
    r"""
^\x0c(?P<model>.+?)\s+(?P<engine>DOE-2\..+?)\s+(?P<date>[\/\d]+)\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<bdl_run>BDL\sRUN)\s+(?P<run_time>\d+)
""",
    flags=re.VERBOSE,
)

PATTERN_REPORT_TITLE = re.compile(
    r"""
^(?P<report>REPORT)-\s(?P<report_name>.+?)\s+(?P<weather>WEATHER\sFILE)-\s(?P<weather_file>.+?)\s+$
""",
    flags=re.VERBOSE
)

pattern_meter = re.compile(
    r"""(?P<name>.+)\s{2}(?P<type_>ELECTRICITY|NATURAL\-GAS)""",
    flags=re.VERBOSE,
)

PATTERN_NO_BY_CATEGORY = re.compile(
    r"""
(?P<utility_rate>.+?)\s+(?P<resource>(ELECTRICITY|NATURAL-GAS))\s+(?P<meter>.+?)\s+(?P<metered_energy_units>[\d\.]+)\s+(?P<unit>[A-Z]+)\s+(?P<total_charge>[\d\.]+)\s+(?P<virtual_rate>[\d\.]+)\s+(?P<rate_used_all_year>(YES|NO))
  """,
    flags=re.VERBOSE,
)

pattern_total_energy = re.compile(
    r"""
\s+
(?P<name>TOTAL\sSITE\sENERGY|TOTAL\sSOURCE\sENERGY)
\s+
(?P<value>\d+\.\d+)
\s
(?P<unit>MBTU)
\s+
(?P<value_per_gross_area>\d+\.\d+)
\s+
(?P<unit_per_gross_area>KBTU\/SQFT\-YR\sGROSS\-AREA)
\s+
(?P<value_per_net_area>\d+\.\d+)
\s+
(?P<unit_per_net_area>KBTU\/SQFT\-YR\sNET\-AREA)
""",
    flags=re.VERBOSE,
)

PATTERN_AVERAGE = re.compile(
    r"""
^\s+(?P<name>ENERGY\sCOST/(GROSS|NET)\sBLDG\sAREA):\s+(?P<value>[\d\.]+)$
""",
    flags=re.VERBOSE,
)

pp = pprint.PrettyPrinter(indent=4, width=180)


def chunks(list_: Iterable, n: int) -> Generator[List, None, None]:
    if list_:
        yield list_[:n]
        yield from chunks(list_[n:], n)


def parse_header(lines: str):
    return (list(PATTERN_REPORT_HEAD.search(lines[0]).groupdict().values()),
            list(PATTERN_REPORT_TITLE.search(lines[2]).groupdict().values()))


def parse_meter(line: str):
    _ = pattern_meter.search(line)
    return list(_.groupdict().values())


def parse_content(lines: List[str]):
    content = list()
    for line in filter(lambda x: x.strip(), lines):
        content.append(
            list(PATTERN_NO_BY_CATEGORY.search(line).groupdict().values()))

    return content


def parse_sum(lines: List[str]):
    return [["", "", "", "", "", lines[0].strip()]]


def parse_total(lines: List[str]):
    return tuple(
        map(lambda x: list(pattern_total_energy.search(x).groups()), lines))


def parse_average(lines: List[str]):
    return tuple(list(
        map(lambda x: list(
            PATTERN_AVERAGE.search(x).groupdict().values()),
            lines)
    ))


SliceFunc = namedtuple("SliceFunc", ["name", "slice", "func_parse"])

SLICES_ES_D = (
    SliceFunc(
        name="header", slice=slice(0, 3), func_parse=parse_header
    ),
    SliceFunc(
        name="categories", slice=slice(6, 8), func_parse=lambda x: Categories
    ),
    SliceFunc(
        name="content", slice=slice(10, -6), func_parse=parse_content
    ),
    SliceFunc(
        name="summary", slice=slice(-5, -4), func_parse=parse_sum
    ),
    # SliceFunc(
    #     name="total", slice=slice(-11, -9), func_parse=parse_total
    # ),
    SliceFunc(
        name="percent", slice=slice(-1), func_parse=parse_average
    ),
    # SliceFunc(
    #     name="note", slice=slice(-3, -2), func_parse=lambda x: [[x[0].strip()]]
    # ),
)


def parse_es_d(report: List[str]):
    es_d = list()
    for slice_ in SLICES_ES_D:
        es_d.extend(slice_.func_parse(report[slice_.slice]))

    return es_d
