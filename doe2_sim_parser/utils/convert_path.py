from pathlib import Path, PosixPath, WindowsPath
from typing import Callable, Dict

from doe2_sim_parser.utils.data_types import Path as _Path

path_converter: Dict[Path, Callable] = {
    str: Path,
    PosixPath: lambda x: x,
    WindowsPath: lambda x: x,
}


def convert_path(path: _Path) -> Path:
    return path_converter.get(type(path))(path)
