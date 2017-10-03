import re
from collections import namedtuple
from itertools import starmap
from typing import Generator, Tuple
from typing import List

from .utils import Path
from .utils import Path_
from .utils import convert_path

Report = namedtuple('Report', ['code', 'name', 'report'])
SIM = namedtuple('SIM', ['path', 'reports'])


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

    path: Path = convert_path(path)
    reports: Tuple[Report] = tuple(
        starmap(lambda x, y: Report(code=x.group('code'),
                                    name=x.group('name').strip(),
                                    report=y),
                filter(lambda x: x[0],
                       map(lambda x: (report_title.search(x[2]), x),
                           parse_report(path)))))

    return SIM(path=path, reports=reports)


def write_sim(file: Path_, code: str, reports: List[Report]):
    file: Path = convert_path(file)
    return file.write_text(''.join(map(lambda x: ''.join(x.report), reports)))
