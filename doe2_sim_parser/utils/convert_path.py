import pathlib
from typing import Callable
from typing import Dict
from typing import TypeVar

Path_ = TypeVar('Path_',
                str,
                pathlib.Path,
                pathlib.PosixPath,
                pathlib.PurePath,
                pathlib.WindowsPath)

Path = TypeVar('Path',
               pathlib.Path,
               pathlib.PosixPath,
               pathlib.PurePath,
               pathlib.WindowsPath)

path_converter: Dict[Path_, Callable] = {
    str: lambda x: pathlib.Path(x),
    pathlib.Path: lambda x: x,
    pathlib.PosixPath: lambda x: x,
    pathlib.PurePath: lambda x: x,
    pathlib.WindowsPath: lambda x: x}


def convert_path(path: Path_):
    type_ = type(path)
    if type_ in path_converter:
        return path_converter[type_](path)
    else:
        raise TypeError(type_)
