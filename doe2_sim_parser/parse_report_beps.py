import re
from typing import List

from doe2_sim_parser.utils import PATTERN_METER, chunks, parse_header
from doe2_sim_parser.utils.data_types import SliceFunc, Report

Cat = [
    [
        "METER",
        "TYPE",
        "UNIT",
        "LIGHTS",
        "TASK\nLIGHTS",
        "MISC\nEQUIP",
        "SPACE\nHEATING",
        "SPACE\nCOOLING",
        "HEAT\nREJECT",
        "PUMPS\n& AUX",
        "VENT\nFANS",
        "REFRIG\nDISPLAY",
        "HT PUMP\nSUPPLEN",
        "DOMEST\nHOT WTR",
        "EXT\nUSAGE",
        "TOTAL",
    ]
]

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

PATTER_TOTAL_ENERGY = re.compile(
    r"""
\s+
(?P<name>TOTAL\sSITE\sENERGY|TOTAL\sSOURCE\sENERGY)\s+
(?P<value>\d+\.\d+)\s
(?P<unit>MBTU)\s+
(?P<value_per_gross_area>\d+\.\d+)\s+
(?P<unit_per_gross_area>KBTU\/SQFT\-YR\sGROSS\-AREA)\s+
(?P<value_per_net_area>\d+\.\d+)\s+
(?P<unit_per_net_area>KBTU\/SQFT\-YR\sNET\-AREA)
""",
    flags=re.VERBOSE,
)

PATTERN_PERCENT_AND_HOURS = re.compile(
    r"""\s+(?P<name>.+?)\s+=\s+(?P<value>\d+[.\d]*)""", flags=re.VERBOSE
)


def parse_meter(line: str):
    return list(PATTERN_METER.search(line).groupdict().values())


def parse_no_by_category(line: str):
    return PATTERN_NO_BY_CATEGORY.search(line).groupdict().values()


def parse_content(lines: List[str]):
    _lines = list(filter(lambda x: x.strip(), lines))
    content = []

    for line in chunks(_lines, 2):
        content.append([*parse_meter(line[0]), *parse_no_by_category(line[1])])

    return content


def parse_sum(lines: List[str]):
    sum_ = []

    for line in lines:
        sum_.append(["", "", *parse_no_by_category(line)])

    return sum_


def parse_total(lines: List[str]):
    total = []

    for line in lines:
        _ = PATTER_TOTAL_ENERGY.search(line).groups()
        total.append(list(_))

    return total


def parse_percent(lines: List[str]):
    return tuple(
        list(
            map(
                lambda x: list(
                    PATTERN_PERCENT_AND_HOURS.search(x).groupdict().values()
                ),
                lines,
            )
        )
    )


SLICES_BEPS = (
    SliceFunc(name="header", slice=slice(0, 3), func_parse=parse_header),
    SliceFunc(name="categories", slice=slice(5, 7), func_parse=lambda x: Cat),
    SliceFunc(name="content", slice=slice(9, -17), func_parse=parse_content),
    SliceFunc(name="summary", slice=slice(-15, -14), func_parse=parse_sum),
    SliceFunc(name="total", slice=slice(-11, -9), func_parse=parse_total),
    SliceFunc(name="percent", slice=slice(-8, -4), func_parse=parse_percent),
    SliceFunc(name="note", slice=slice(-3, -2),
              func_parse=lambda x: [[x[0].strip()]]),
)


def parse_beps(report: List[Report]):
    beps = list()
    for slice_ in SLICES_BEPS:
        lines = report[0].report[slice_.slice]
        _ = slice_.func_parse(lines)
        beps.extend(_)

    return beps
