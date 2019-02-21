import logging

from collections import defaultdict
from typing import Generator, List, Tuple

from doe2_sim_parser.utils import (
    PATTERN_REPORT_HEAD, PATTERN_REPORT_HOURLY_REPORT, PATTERN_REPORT_TITLE)
from doe2_sim_parser.utils.convert_path import convert_path
from doe2_sim_parser.utils.data_types import SIM, Path, Report

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


def parse_report(report: Tuple[str]) -> Report:
    """
    parse a report into two types of normal and hourly
    :param report:
    :return:
    """
    result = PATTERN_REPORT_TITLE.search(report[2])

    if result:
        return Report(
            type_="normal_report",
            code=result.group("code"),
            name=result.group("name").strip(),
            report=report,
        )
    elif PATTERN_REPORT_HOURLY_REPORT.search(report[2]):
        return Report(
            type_="hourly_report", code=None, name=None, report=report)
    else:
        raise ValueError(report)


def read_sim(path: Path) -> Generator[Report, None, None]:
    """
    read a sim report and yield the reports of it one by one, with parsed the
    report name
    :param path: the path of sim report
    :return: a Report object contained the report code, name and content of it
    """
    report: List[str] = []
    with path.open() as sim:
        for line in sim.readlines():
            if PATTERN_REPORT_HEAD.search(line):
                if report:
                    yield parse_report(tuple(report))
                report: List[str] = [line]
            else:
                report.append(line)
        else:
            yield parse_report(tuple(report))


def split_sim(path: Path) -> SIM:
    """
    split sim into two different types - normal and hourly
    :param path: the path to the sim report
    :return: a SIM object contained all of the parsed reports with reports name
    and contents
    """
    logger.info('Receive sim: %s', path)

    path: Path = convert_path(path)
    dict_ = defaultdict(list)

    for report in read_sim(path):  # type: Report
        dict_[report.type_].append(report)

    logger.info('This sim has %s normal reports, %s hourly reports',
                len(dict_["normal_report"]),
                len(dict_["hourly_report"]))

    return SIM(
        path=path,
        normal_reports=tuple(dict_["normal_report"]),
        hourly_reports=tuple(dict_["hourly_report"]),
    )
