import re
from collections import defaultdict, OrderedDict
from typing import List, Dict, Tuple

from doe2_sim_parser.utils import (PATTERN_REPORT_HOURLY_REPORT_HEAD_1,
                                   PATTERN_REPORT_HOURLY_REPORT_CONTENT)
from doe2_sim_parser.utils.data_types import SliceFunc, Report

PATTERN_VARIABLE = re.compile(r'(-{4}\([\s\d]{2}\))')


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


def get_columns(report: Report):
    column_slices = list()
    for match in PATTERN_VARIABLE.finditer(report.report[10]):
        column_slices.append(slice(*match.span()))

    columns = ['MM', 'DD', 'HH']
    for slice_ in column_slices:
        columns.append(
            ' '.join(
                map(
                    lambda x: x[slice_].strip(),
                    (report.report[4], *report.report[6:9])
                )
            )
        )

    return columns


def parse_single_page_hourly_report(report: Report) -> Dict[Tuple, List[str]]:
    _lines: List = list()

    for line in report.report[11:35]:
        _lines.append(
            (
                (line[0:2], line[2:4], line[4:6]),
                line[6:].split()
            )
        )

    hourly_report: Dict[Tuple, List[str]] = OrderedDict(_lines)

    return hourly_report


def parse_one_hourly_report(report: Dict[int, List[Report]]):
    _reports: Dict = defaultdict(list)

    for no, reports in report.items():
        _reports[('MM', 'DD', 'HH')].extend(get_columns(reports[0])[3:])

        for report in reports:
            _ = parse_single_page_hourly_report(report)
            for k, v in _.items():
                _reports[k].extend(v)

    return _reports


def group_hourly_report(report: List[Report]):
    dict_hourly_report = defaultdict(dict)

    for _report in report:
        _ = dict_hourly_report[_report.name]
        if _report.report_no not in _:
            _.update({_report.report_no: list()})
        _[_report.report_no].append(_report)

    return dict_hourly_report


def parse_hourly_report(report: List[Report]):
    hourly_reports = defaultdict(list)
    _hourly_reports = group_hourly_report(report)

    for report_name, reports in _hourly_reports.items():
        one_report = parse_one_hourly_report(reports)
        for k, v in one_report.items():
            hourly_reports[k].extend(v)

    list_hourly_report = list()

    for k, v in hourly_reports.items():
        list_hourly_report.append(
            (*k, *v)
        )

    return list_hourly_report
