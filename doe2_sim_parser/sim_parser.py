import re
from collections import namedtuple
from itertools import starmap
from typing import Generator
from typing import List
from typing import Tuple

from .utils import Path
from .utils import Path_
from .utils import convert_path

Report = namedtuple('Report', ['code', 'name', 'report'])
SIM = namedtuple('SIM', ['path', 'normal_reports', 'hourly_reports'])


def parse_report(path: Path) -> Generator[Tuple[str], None, None]:
    """
    each time yield a tuple within a report
    :param path:
    :return:
    """

    report_head = re.compile(
        r'''
^
(?P<model>.+?)\s+
(?P<engine>DOE-2\..+?)\s+
(?P<date>[\/\d]+)\s+
(?P<time>\d{2}:\d{2}:\d{2})\s+
BDL\sRUN\s+
(?P<run_time>\d+)
''',
        flags=re.VERBOSE)

    report: List[str] = []
    for line in path.open().readlines():
        if report_head.search(line):
            if report:
                yield tuple(report)
            report: List[str] = [line]
        else:
            report.append(line)
    else:
        yield tuple(report)


def parse_sim(path: Path_) -> SIM:
    report_title = re.compile(
        r'''
REPORT-\s
(?P<code>[A-Z\-]{4})\s
(?P<name>.+)
WEATHER\sFILE\-\s
(?P<weather>[^\s].+[^\s])\s+
''',
        flags=re.VERBOSE)

    report_hourly_report = re.compile(
        r'''
HOURLY\sREPORT\-\sHourly\sReport\s+
HVAC\s+
WEATHER\sFILE\-\sEPW\sMACAU,\-,MAC\s+
Pg:\s+
\d+\s\-\s+\d
''',
        flags=re.VERBOSE
    )

    path: Path = convert_path(path)

    _normal_reports: List = []
    _hourly_reports: List = []

    for report in parse_report(path):
        if report_title.search(report[2]):
            _normal_reports.append(report)
        elif report_hourly_report.search(report[2]):
            _hourly_reports.append(Report(code='hourly_report',
                                          name=None,
                                          report=report))
        else:
            raise ValueError(report)
    else:
        reports: List[Report] = tuple(starmap(
            lambda x, y: Report(code=x.group('code'),
                                name=x.group('name').strip(),
                                report=y),
            map(lambda x: (report_title.search(x[2]), x),
                _normal_reports)))

    return SIM(path=path, normal_reports=reports,
               hourly_reports=_hourly_reports)


def write_sim(file: Path_, reports: List[Report]):
    file: Path = convert_path(file)
    return file.write_text(''.join(map(lambda x: ''.join(x.report), reports)))
