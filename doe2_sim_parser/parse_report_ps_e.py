import pprint
import re
from collections import defaultdict
from typing import List, Dict

from doe2_sim_parser.utils import chunks
from doe2_sim_parser.utils.data_types import Report

pp = pprint.PrettyPrinter(indent=4, width=180)

Cat = [
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

PATTERN_METER = re.compile(
    r"""^REPORT-\sPS-E\sEnergy\sEnd-Use\sSummary\sfor\sall\s
    (?P<meter>(Electric|Fuel|Steam|CHW)\sMeters)\s+WEATHER\sFILE-\s
    (?P<weather>.+?)\s+$
    """, flags=re.VERBOSE
)

PATTERN_SPLITTER = re.compile(r'-{7,8}')


def get_slices(line: str) -> List[slice]:
    slices = [slice(0, 12), ]

    for _ in PATTERN_SPLITTER.finditer(line):
        slices.append(slice(*_.span()))

    return slices


def group_by_meter(reports: List[Report]) -> Dict[str, List[Report]]:
    dict_report = defaultdict(list)
    for report in reports:
        meter = PATTERN_METER.search(report.report[2]).group('meter')
        dict_report[meter].append(report)
    return dict_report


def parse_ps_e(reports: List[Report]):
    ps_e = group_by_meter(reports)

    ps_e_parse = list()

    for meter, reports_ in ps_e.items():
        report_parsed = [[meter, *Cat]]
        slices = get_slices(reports_[0].report[7])
        for meter_group in chunks(reports_[0].report[9:], 7):
            for line in meter_group[:-1]:
                report_parsed.append([line[x].strip() for x in slices])
        for meter_group in chunks(reports_[1].report[5:32], 7):
            for line in meter_group[:-1]:
                report_parsed.append([line[x].strip() for x in slices])
        ps_e_parse.extend(report_parsed)

    return ps_e_parse
