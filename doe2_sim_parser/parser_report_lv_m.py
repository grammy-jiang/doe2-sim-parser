import re
from typing import List

from doe2_sim_parser.utils import parse_header
from doe2_sim_parser.utils.data_types import SliceFunc

Cat = [
    [
        "",
        "ENGLISH",
        "MULTIPLIED BY   GIVES",
        "METRIC",
        "MULTIPLIED BY   GIVES",
        "ENGLISH",
    ]
]

PATTERN_CONTENT = re.compile(
    r"""
^\s{8,10}
(?P<no>\d+)\s{8}
(?P<ip_unit>.+?)\s+
(?P<ip_value>\d+\.\d{6})\s{3}
(?P<si_unit>.+?)\s+
(?P<si_value>\d+\.\d{6})\s{3}
(?P<ip_unit_2>.+?)\s*$
""",
    flags=re.VERBOSE,
)


def parse_content(lines: List[str]) -> List[List[str]]:
    content = list()
    for line in filter(lambda x: x.strip(), lines):
        _ = PATTERN_CONTENT.search(line).groupdict().values()
        content.append(list(_))
    return content


SLICES = (
    SliceFunc(name="header", slice=slice(0, 3), func_parse=parse_header),
    SliceFunc(name="categories", slice=slice(4, 6), func_parse=lambda x: Cat),
    SliceFunc(name="content", slice=slice(7, None), func_parse=parse_content),
)


def parse_lv_m(report: List[str]) -> List[List[str]]:
    lv_m = list()
    for slice_ in SLICES:
        lines = report[slice_.slice]
        _ = slice_.func_parse(lines)
        lv_m.extend(_)

    return lv_m
