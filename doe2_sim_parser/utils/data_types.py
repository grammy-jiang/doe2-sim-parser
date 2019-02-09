from collections import namedtuple
from pathlib import Path as _Path
from typing import List, Tuple, TypeVar

Path = TypeVar("Path", str, _Path)
Report = namedtuple(
    "Report",
    [
        "type_",  # normal_report or hourly_report
        "code",  # only normal_report
        "name",  # only normal_report
        "report",  # type: List
    ],
)
SIM = namedtuple(
    "SIM",
    [
        "path",  # type: _Path
        "normal_reports",  # type: Tuple[Report]
        "hourly_reports",  # type: Tuple[Report]
    ],
)

SliceFunc = namedtuple("SliceFunc", ["name", "slice", "func_parse"])
