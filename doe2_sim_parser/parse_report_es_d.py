import re
from typing import List

from doe2_sim_parser.utils import parse_header
from doe2_sim_parser.utils.data_types import SliceFunc

Categories = [[
    "UTILITY-RATE",
    "RESOURCE",
    "METERS",
    "METERED\nENERGY\nUNITS/YR",
    "",
    "TOTAL\nCHARGE\n($)",
    "VIRTUAL\nRATE\n($/UNIT)",
    "RATE USED\nALL YEAR?",
]]

PATTERN_NO_BY_CATEGORY = re.compile(
    r"""
(?P<utility_rate>.+?)\s+
(?P<resource>(ELECTRICITY|NATURAL-GAS))\s+
(?P<meter>.+?)\s+
(?P<metered_energy_units>[\d\.]+)\s+
(?P<unit>[A-Z]+)\s+
(?P<total_charge>[\d\.]+)\s+
(?P<virtual_rate>[\d\.]+)\s+
(?P<rate_used_all_year>(YES|NO))
  """,
    flags=re.VERBOSE,
)

PATTERN_AVERAGE = re.compile(
    r"""
^\s+(?P<name>ENERGY\sCOST/(GROSS|NET)\sBLDG\sAREA):\s+(?P<value>[\d\.]+)$
""",
    flags=re.VERBOSE,
)


def parse_content(lines: List[str]):
    content = list()
    for line in filter(lambda x: x.strip(), lines):
        content.append(
            list(PATTERN_NO_BY_CATEGORY.search(line).groupdict().values()))
    return content


def parse_sum(lines: List[str]):
    return [["", "", "", "", "", lines[0].strip()]]


def parse_average(lines: List[str]):
    return list(
        map(
            lambda x: ["", "", "", "", *PATTERN_AVERAGE.search(x).groupdict().values()],
            lines,
        )
    )


SLICES_ES_D = (
    SliceFunc(name="header", slice=slice(0, 3), func_parse=parse_header),
    SliceFunc(
        name="categories", slice=slice(6, 8), func_parse=lambda x: Categories),
    SliceFunc(name="content", slice=slice(10, -6), func_parse=parse_content),
    SliceFunc(name="summary", slice=slice(-5, -4), func_parse=parse_sum),
    SliceFunc(name="percent", slice=slice(-2, None), func_parse=parse_average),
)


def parse_es_d(report: List[str]):
    es_d = list()
    for slice_ in SLICES_ES_D:
        es_d.extend(slice_.func_parse(report[slice_.slice]))

    return es_d
