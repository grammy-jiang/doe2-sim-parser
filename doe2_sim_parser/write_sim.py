from pathlib import Path
from typing import Iterable

from .utils.convert_path import convert_path
from .utils.data_types import Path_
from .utils.data_types import Report


def write_sim(file: Path_, reports: Iterable[Report]):
    file: Path = convert_path(file)
    return file.write_text(''.join(map(lambda x: ''.join(x.report), reports)))
