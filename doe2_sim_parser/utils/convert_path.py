from pathlib import Path
from pathlib import PosixPath
from pathlib import WindowsPath
from typing import Callable
from typing import Dict

from .data_types import Path_

path_converter: Dict[Path_, Callable] = {
    str: lambda x: Path(x),
    PosixPath: lambda x: x,
    WindowsPath: lambda x: x}


def convert_path(path: Path_) -> Path:
    type_ = type(path)
    if type_ in path_converter:
        return path_converter[type_](path)
    else:
        raise TypeError(type_)
