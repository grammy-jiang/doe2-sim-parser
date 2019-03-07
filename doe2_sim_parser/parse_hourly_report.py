from collections import defaultdict
from typing import List, Dict

from doe2_sim_parser.utils import (PATTERN_REPORT_HOURLY_REPORT_HEAD_1,
                                   PATTERN_REPORT_HOURLY_REPORT_CONTENT)
from doe2_sim_parser.utils.data_types import SliceFunc, Report


def parse_headers(lines: List[str]):
    headers: List[List[str]] = list()
    for line in lines:
        headers.append(
            list(
                map(
                    lambda x: x.strip(),
                    PATTERN_REPORT_HOURLY_REPORT_HEAD_1.search(line).groups()
                )
            )
        )

    return headers


def parse_content(lines: List[str]):
    contents: List[List[str]] = list()
    for line in lines:
        contents.append(
            list(
                map(
                    lambda x: x.strip(),
                    PATTERN_REPORT_HOURLY_REPORT_CONTENT.search(line).groups()
                )
            )
        )

    return contents


SLICES_HOURLY_REPORT = (
    SliceFunc(name="header", slice=slice(4, 5), func_parse=parse_headers),
    SliceFunc(name="header", slice=slice(6, 9), func_parse=parse_headers),
    SliceFunc(name="header", slice=slice(11, 35), func_parse=parse_content),
)


def parse_single_hourly_report(report: Report):
    hourly_report: List[List[str]] = list()
    for slice_ in SLICES_HOURLY_REPORT:
        lines = report.report[slice_.slice]
        _ = slice_.func_parse(lines)
        hourly_report.extend(_)

    return hourly_report


def parse_one_hourly_report(report: Dict[int, List[Report]]):
    _ = report
    return _


def group_hourly_report(report: List[Report]):
    dict_hourly_report = defaultdict(dict)

    for _report in report:
        _ = dict_hourly_report[_report.name]
        if _report.report_no not in _:
            _.update({_report.report_no: list()})
        _[_report.report_no].append(_report)

    return dict_hourly_report


def parse_hourly_report(report: List[Report]):
    hourly_report = group_hourly_report(report)

    for report_name, reports in hourly_report.items():
        one_report = parse_one_hourly_report(reports)

        # for report_no, _reports in reports.items():
        #     for _report in _reports:
        #         _ = parse_single_hourly_report(_report)

    # for slice_ in SLICES_HOURLY_REPORT:
    #     lines = _report.report[slice_.slice]
    #     _ = slice_.func_parse(lines)
    #     hourly_report.extend(_)

    return hourly_report
