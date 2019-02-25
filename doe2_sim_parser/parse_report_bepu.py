import re
from collections import namedtuple
from typing import List

from doe2_sim_parser.parse_report_es_d import parse_header
from doe2_sim_parser.utils import PATTERN_METER, chunks
from doe2_sim_parser.utils.data_types import SliceFunc

Meter = namedtuple("Meter", ["name", "type_"])
Categories = [
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
^\s+
(?P<name>TOTAL\s(ELECTRICITY|NATURAL-GAS|STEAM|CHILLED-WATE))\s+
(?P<value>\d+\.)\s
(?P<unit>KWH|THERM|MBTU+)\s+
(?P<value_per_gross_area_1>\d+\.\d+)\s
(?P<unit_per_gross_area_1>KWH|THERM|MBTU)\s+
(?P<unit_area_1>/SQFT-YR\sGROSS-AREA)\s+
(?P<value_per_gross_area_2>\d+\.\d+)\s
(?P<unit_per_gross_area_2>KWH|THERM|MBTU)\s+
(?P<unit_area_2>/SQFT-YR\sNET-AREA)
""",
    flags=re.VERBOSE,
)

PATTERN_PERCENT_AND_HOURS = re.compile(
    r"""\s+(?P<name>.+?)\s+=\s+(?P<value>\d+[.\d]*)""", flags=re.VERBOSE
)


def parse_contents(lines: List[str]):
    content = []
    counter = None

    for i, [l_1, l_2, l_3] in enumerate(chunks(lines, 3)):
        if l_1 == "\n" and l_2 == "\n" and l_3 == "\n":
            counter = i

            break
        else:
            meter = PATTERN_METER.search(l_1).groupdict().values()
            no_by_category = PATTERN_NO_BY_CATEGORY.search(l_2).groupdict().values()
            content.append([*meter, *no_by_category])

    total = []

    for line in lines[(counter + 1) * 3 :]:
        total.append(list(PATTERN_TOTAL_ENERGY.search(line).groups()))

    return [*content, *total]


def parse_percent(lines: List[str]):
    percent = []

    for line in lines:
        _ = PATTERN_PERCENT_AND_HOURS.search(line).groupdict().values()
        percent.append(list(_))

    return percent


SLICES_BEPU = (
    SliceFunc(name="header", slice=slice(0, 3), func_parse=parse_header),
    SliceFunc(name="categories", slice=slice(5, 7), func_parse=lambda x: Categories),
    SliceFunc(name="contents", slice=slice(9, -10), func_parse=parse_contents),
    SliceFunc(name="percent", slice=slice(-8, -4), func_parse=parse_percent),
    SliceFunc(name="note", slice=slice(-3, -2), func_parse=lambda x: [[x[0].strip()]]),
)


def parse_bepu(report: List[str]):
    bepu = list()

    for slice_ in SLICES_BEPU:
        lines = slice_.func_parse(report[slice_.slice])
        bepu.extend(lines)

    return bepu
