import re
from abc import ABCMeta, abstractmethod
from typing import List

PATTERN_REPORT_TITLE = re.compile(
    r'^(?P<report>REPORT|HOURLY\sREPORT)-\s'
    r'(?P<name>.+)'
)

PATTERN_NORMAL_REPORT_TITLE = re.compile(
    r'^(?P<code>[A-Z-]{4})\s'
    r'(?P<name>.+?)\s+(WEATHER\sFILE-)\s'
    r'(?P<weather>.+)'
)

PATTERN_HOURLY_REPORT_TILE = re.compile(
    r'^(?P<name>.*?)\s+HVAC\s+(WEATHER\sFILE-)\s'
    r'(?P<weather>.+)\sPg:\s+'
    r'(?P<report_page_no>\d+)\s-\s+'
    r'(?P<report_no>\d+)'
)


class SingleReport(object):
    def __init__(
            self, type_: str, name: str, report: List[str], code: str = None,
            report_no: int = None, page_no: int = None
    ):
        self.type = type_
        self.code = code
        self.name = name
        self.report_no = report_no
        self.report_page_no = page_no
        self.report = report
        self._report = None

    @classmethod
    def from_text(cls, text: List[str]):
        title = text[2]

        result = PATTERN_REPORT_TITLE.search(title).groupdict()

        if result['report'] == 'REPORT':
            name = PATTERN_NORMAL_REPORT_TITLE.search(result['name'])
            return cls(
                type_="normal",
                code=name.group("code"),
                name=name.group("name"),
                report=text,
            )
        elif result['report'] == 'HOURLY REPORT':
            name = PATTERN_HOURLY_REPORT_TILE.search(result['name'])
            return cls(
                type_="hourly",
                name=name.group("name"),
                report=text,
                report_no=int(name.group("report_no")),
                page_no=int(name.group("report_page_no"))
            )
        else:
            raise ValueError(text)


class Report(metaclass=ABCMeta):
    dict_subclass = {}
    type = None
    code = None
    name = None

    def __init__(self, type_: str, name: str, **kwargs):
        self.single_reports: List[SingleReport] = list()
        self.type = type_
        self.name = name
        self.reports = list()

    @abstractmethod
    def _parse_report(self):
        pass

    @classmethod
    def from_code(cls, code: str):
        return cls.dict_subclass.get(code, list())

    def append(self, report: SingleReport):
        self.reports.append(report)


Report.dict_subclass = {
    (subclass.name, subclass) for subclass in Report.__subclasses__()
}


class ReportBEPS(Report):
    type = 'normal_report'
    code = 'BEPS'
    name = 'Building Energy Performance'

    def __init__(
            self, type_: str, code: str, name: str, report: List[str]
    ):
        super(ReportBEPS, self).__init__(type_, code, name, report)

    def _parse_report(self):
        pass
