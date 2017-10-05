import re
from collections import defaultdict
from pathlib import Path
from typing import Generator
from typing import List
from typing import Tuple

from .utils import Path_
from .utils import convert_path
from .utils.data_types import Report
from .utils.data_types import SIM

pattern_report_title = re.compile(
    r'''
REPORT-\s
(?P<code>[A-Z\-]{4})\s
(?P<name>.+)
WEATHER\sFILE\-\s
(?P<weather>[^\s].+[^\s])\s+
''',
    flags=re.VERBOSE)

pattern_report_hourly_report = re.compile(
    r'''
HOURLY\sREPORT\-\sHourly\sReport\s+
HVAC\s+
WEATHER\sFILE\-\sEPW\sMACAU,\-,MAC\s+
Pg:\s+
\d+\s\-\s+\d
''',
    flags=re.VERBOSE)

pattern_report_head = re.compile(
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


def parse_report(report: Tuple[str]) -> Report:
    result = pattern_report_title.search(report[2])
    if result:
        return Report(type_='normal_report',
                      code=result.group('code'),
                      name=result.group('name').strip(),
                      report=report)
    elif pattern_report_hourly_report.search(report[2]):
        return Report(type_='hourly_report',
                      code=None,
                      name=None,
                      report=report)
    else:
        raise ValueError(report)


def read_sim(path: Path) -> Generator[Report, None, None]:
    """
    each time yield a tuple within a report
    :param path:
    :return:
    """
    report: List[str] = []
    with path.open() as f:
        for line in f.readlines():
            if pattern_report_head.search(line):
                if report:
                    yield parse_report(tuple(report))
                report: List[str] = [line]
            else:
                report.append(line)
        else:
            yield parse_report(tuple(report))


def parse_sim(path: Path_) -> SIM:
    path: Path = convert_path(path)
    dict_ = defaultdict(list)
    for report in read_sim(path):  # type: Report
        dict_[report.type_].append(report)

    return SIM(path=path, normal_reports=tuple(dict_['normal_report']),
               hourly_reports=tuple(dict_['hourly_report']))
