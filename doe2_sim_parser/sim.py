import logging
import re
from collections import UserDict
from pathlib import Path
from typing import Generator, List, Union

from doe2_sim_parser.report import SingleReport, Report
from doe2_sim_parser.utils.convert_path import convert_path

PATTERN_REPORT_HEAD = re.compile(
    r"""
^\x0c
(?P<model>.+?)\s+
(?P<engine>DOE-2\.\d+\-[\da-z]+)\s+
(?P<date>\d{1,2}/\d{1,2}/\d{4})\s+
(?P<time>\d{1,2}:\d{1,2}:\d{1,2})\s+BDL\sRUN\s+
(?P<run_time>\d+)
""",
    flags=re.VERBOSE,
)


class SIM(UserDict):
    name = 'SIM'

    def __init__(self, path: Path):
        super(SIM, self).__init__()

        self.path = convert_path(path)
        self.normal_reports: List[SingleReport] = list()
        self.hourly_reports: List[SingleReport] = list()

    @classmethod
    def from_path(cls, path: Union[str, Path]):
        if isinstance(path, str):
            return cls(Path(path))
        elif isinstance(path, Path):
            return cls(path)
        else:
            raise TypeError('An unknown type of path is found: %s', path)

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)

    def _read_sim(self) -> Generator[SingleReport, None, None]:
        report: List[str] = []
        with self.path.open(mode='r') as f:
            for line in f.readlines():
                if PATTERN_REPORT_HEAD.search(line):
                    if report:
                        yield SingleReport.from_text(report)
                    report: List[str] = [line]
                else:
                    report.append(line)
            else:
                yield SingleReport.from_text(report)

    def _register_report(self, report: SingleReport):
        if report.type == 'normal':
            self.normal_reports.append(report)
            self[report.code].append(report)
        elif report.type == 'hourly':
            self.hourly_reports.append(report)
        else:
            raise TypeError(
                'An unknown type of report is found: %s',
                report.report
            )

    def split(self):
        if not self.is_split():
            for report in self._read_sim():
                self._register_report(report)

    def is_split(self) -> bool:
        if self.normal_reports and self.hourly_reports:
            return True
        else:
            return False

    def __missing__(self, key):
        self[key] = Report.from_code(key)
        return self[key]
