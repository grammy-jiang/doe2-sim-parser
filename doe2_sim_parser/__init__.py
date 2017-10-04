import pprint
from collections import defaultdict
from itertools import starmap
from typing import Dict
from typing import Iterable

from .settings import TARGET_REPORTS
from .parse_sim import Report
from .parse_sim import SIM
from .parse_sim import parse_sim
from .parse_sim import write_sim
from .utils.convert_path import Path
from .utils.convert_path import Path_
from .utils.convert_path import convert_path

pp = pprint.PrettyPrinter(indent=4, width=120)

_TARGET_REPORTS = dict(map(lambda x: x[1:3], TARGET_REPORTS))


def split_sim(path_sim: Path_,
              target_folder: Path_,
              target_reports: Iterable = TARGET_REPORTS) -> Dict[str, int]:
    """

    :param path_sim:
    :param target_folder:
    :param target_reports:
    :return: a dictionary with report code as key, the size of the report as
    value
    """
    path_sim: Path = convert_path(path_sim)
    target_folder: Path = convert_path(target_folder)

    if not target_folder.is_dir():
        target_folder.mkdir()

    if target_reports == TARGET_REPORTS:
        target_reports: Dict = _TARGET_REPORTS
    elif isinstance(target_reports, list):
        target_reports = dict(
            map(lambda x: (x, _TARGET_REPORTS[x]),
                target_reports))
    else:
        raise TypeError(type(target_reports))

    sim: SIM = parse_sim(path_sim)

    buffer = defaultdict(list)

    for report in sim.normal_reports:  # type: Report
        if report.code in target_reports:
            buffer[report.code].append(report)

    return dict(
        (*starmap(
            lambda file, code, reports: (code, write_sim(file, reports)),
            starmap(lambda code, reports: (
                target_folder / '{SIM} - {code} {name}.SIM'.format(
                    SIM=path_sim.stem,
                    code=code,
                    name=target_reports[code].replace('/', '_')),
                code,
                reports),
                    buffer.items())),
         ('normal_reports', write_sim(
             file=target_folder / '{SIM} - {code}.SIM'.format(
                 SIM=path_sim.stem,
                 code='normal_reports'),
             reports=sim.normal_reports)),
         ('hourly_reports', write_sim(
             file=target_folder / '{SIM} - {code}.SIM'.format(
                 SIM=path_sim.stem,
                 code='hourly_reports'),
             reports=sim.hourly_reports)))
    )


def transfer_sim2xlsx(path_sim: Path_, path_xlsx: Path_):
    path_sim: Path = convert_path(path_sim)
    path_xlsx: Path = convert_path(path_xlsx)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
