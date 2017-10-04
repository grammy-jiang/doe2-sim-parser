from collections import namedtuple
from pathlib import Path
from typing import Tuple
from typing import TypeVar

Path_ = TypeVar('Path_', str, Path)
Report = namedtuple('Report', [
    'type_',  # normal_report or hourly_report
    'code',  # only normal_report
    'name',  # only normal_report
    'report'  # only normal_report
])
SIM = namedtuple('SIM', [
    'path',  # type: Path
    'normal_reports',  # type: Tuple[Report]
    'hourly_reports'  # type: Tuple[Report]
])
