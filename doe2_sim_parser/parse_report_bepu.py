import re
from collections import namedtuple
from typing import Generator, Iterable, List

Meter = namedtuple("Meter", ["name", "type_"])
Categories = [[
    "METER", "TYPE", "UNIT",
    "LIGHTS", "TASK\nLIGHTS", "MISC\nEQUIP", "SPACE\nHEATING", "SPACE\nCOOLING",
    "HEAT\nREJECT", "PUMPS\n& AUX", "VENT\nFANS", "REFRIG\nDISPLAY",
    "HT PUMP\nSUPPLEN", "DOMEST\nHOT WTR", "EXT\nUSAGE", "TOTAL",
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
^\s+
(?P<unit>[A-Z]+)\s+
(?P<LIGHTS>[\d.]+)\s+
(?P<TASK_LIGHTS>[\d.]+)\s+
(?P<MISC_EQUIP>[\d.]+)\s+
(?P<SPACE_HEATING>[\d.]+)\s+
(?P<SPACE_COOLING>[\d.]+)\s+
(?P<HEAT_REJECT>[\d.]+)\s+
(?P<PUMPS_AUX>[\d.]+)\s+
(?P<VENT_FANS>[\d.]+)\s+
(?P<REFRIG_DISPLAY>[\d.]+)\s+
(?P<HT_PUMP_SUPPLEM>[\d.]+)\s+
(?P<DOMEST_HOT_WTR>[\d.]+)\s+
(?P<EXT_USAGE>[\d.]+)\s+
(?P<TOTAL>[\d.]+)
   """,
    flags=re.VERBOSE,
)

pattern_total_energy = re.compile(
    r"""
\s+
(?P<name>TOTAL\s(ELECTRICITY|NATURAL-GAS))\s+
(?P<value>[\d\.]+)\s
(?P<unit>[A-Z]+)\s+
(?P<value_per_gross_area_1>[\d\.]+)\s+
(?P<unit_per_gross_area_1>[A-Z]+)\s+
(?P<unit_area_1>/SQFT-YR\sGROSS-AREA)\s+
(?P<value_per_gross_area_2>[\d\.]+)\s
(?P<unit_per_gross_area_2>[A-Z]+)\s+
(?P<unit_area_2>/SQFT-YR\sNET-AREA)
""",
    flags=re.VERBOSE,
)

pattern_percent_and_hours = re.compile(
    r"""
\s+
(?P<name>.+?)
\s+
=
\s+
(?P<value>\d+[.\d]*)
""",
    flags=re.VERBOSE,
)


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


def parse_no_by_category(line: str):
    return PATTERN_NO_BY_CATEGORY.search(line).groupdict().values()


def parse_content(lines: List[str]):
    return list(map(
        lambda x: [*parse_meter(x[0]), *parse_no_by_category(x[1])],
        chunks(list(filter(lambda x: x.strip(), lines)), 2),
    ))


def parse_total(lines: List[str]):
    return tuple(
        map(lambda x: list(pattern_total_energy.search(x).groups()), lines))


def parse_percent(lines: List[str]):
    return tuple(list(
        map(lambda x: list(
            pattern_percent_and_hours.search(x).groupdict().values()),
            lines)
    ))


SliceFunc = namedtuple("SliceFunc", ["name", "slice", "func_parse"])

SLICES_BEPU = (
    SliceFunc(
        name="header", slice=slice(0, 3), func_parse=parse_header
    ),
    SliceFunc(
        name="categories", slice=slice(5, 7), func_parse=lambda x: Categories
    ),
    SliceFunc(
        name="content", slice=slice(9, -16), func_parse=parse_content
    ),
    SliceFunc(
        name="total", slice=slice(-12, -10), func_parse=parse_total
    ),
    SliceFunc(
        name="percent", slice=slice(-8, -4), func_parse=parse_percent
    ),
    SliceFunc(
        name="note", slice=slice(-3, -2), func_parse=lambda x: [[x[0].strip()]]
    ),
)


def parse_bepu(report: List[str]):
    bepu = list()
    for slice_ in SLICES_BEPU:
        bepu.extend(slice_.func_parse(report[slice_.slice]))

    return bepu
