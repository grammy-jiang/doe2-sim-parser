import re
from collections import namedtuple
from typing import List

from doe2_sim_parser.parse_report_es_d import parse_header
from doe2_sim_parser.utils import chunks
from doe2_sim_parser.utils.data_types import SliceFunc

Meter = namedtuple("Meter", ["name", "type_"])
Categories = [[
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
]]

PATTERN_METER = re.compile(
    r"""(?P<name>.+)\s{2}(?P<type_>ELECTRICITY|NATURAL\-GAS)""",
    flags=re.VERBOSE)

PATTERN_NO_BY_CATEGORY = re.compile(
    r"""
^\s+
(?P<unit>[A-Z]+)\s*
(?P<LIGHTS>\d+\.)\s*
(?P<TASK_LIGHTS>\d+\.)\s*
(?P<MISC_EQUIP>\d+\.)\s*
(?P<SPACE_HEATING>\d+\.+)\s*
(?P<SPACE_COOLING>\d+\.)\s*
(?P<HEAT_REJECT>\d+\.)\s*
(?P<PUMPS_AUX>\d+\.)\s*
(?P<VENT_FANS>\d+\.)\s*
(?P<REFRIG_DISPLAY>\d+\.)\s*
(?P<HT_PUMP_SUPPLEM>\d+\.)\s*
(?P<DOMEST_HOT_WTR>\d+\.)\s*
(?P<EXT_USAGE>\d+\.)\s*
(?P<TOTAL>\d+\.)
""",
    flags=re.VERBOSE,
)

PATTERN_TOTAL_ENERGY = re.compile(
    r"""
\s+
(?P<name>TOTAL\s(ELECTRICITY|NATURAL-GAS))\s+
(?P<value>\d+\.)\s
(?P<unit>[A-Z]+)\s+
(?P<value_per_gross_area_1>\d+\.\d+)\s+
(?P<unit_per_gross_area_1>[A-Z]+)\s+
(?P<unit_area_1>/SQFT-YR\sGROSS-AREA)\s+
(?P<value_per_gross_area_2>\d+\.\d+)\s
(?P<unit_per_gross_area_2>[A-Z]+)\s+
(?P<unit_area_2>/SQFT-YR\sNET-AREA)
""",
    flags=re.VERBOSE,
)

PATTERN_PERCENT_AND_HOURS = re.compile(
    r"""\s+(?P<name>.+?)\s+=\s+(?P<value>\d+[.\d]*)""", flags=re.VERBOSE)


def parse_content(lines: List[str]):
    content = []
    for l_1, l_2 in chunks(list(filter(lambda x: x.strip(), lines)), 2):
        meter = PATTERN_METER.search(l_1).groupdict().values()
        no_by_category = PATTERN_NO_BY_CATEGORY.search(l_2).groupdict().values()
        content.append([*meter, *no_by_category])
    return content


def parse_total(lines: List[str]):
    total = []
    for line in filter(lambda x: x.strip(), lines):
        total.append(list(PATTERN_TOTAL_ENERGY.search(line).groups()))
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


SLICES_BEPU = (
    SliceFunc(name="header", slice=slice(0, 3), func_parse=parse_header),
    SliceFunc(
        name="categories", slice=slice(5, 7), func_parse=lambda x: Categories),
    SliceFunc(name="content", slice=slice(9, -15), func_parse=parse_content),
    SliceFunc(name="total", slice=slice(-12, -10), func_parse=parse_total),
    SliceFunc(name="percent", slice=slice(-8, -4), func_parse=parse_percent),
    SliceFunc(
        name="note",
        slice=slice(-3, -2),
        func_parse=lambda x: [[x[0].strip()]]),
)


def parse_bepu(report: List[str]):
    bepu = list()

    for slice_ in SLICES_BEPU:
        bepu.extend(slice_.func_parse(report[slice_.slice]))

    return bepu
