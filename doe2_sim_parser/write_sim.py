"""
Write SIM reports into disk
"""

from collections import defaultdict
from typing import Dict, List

from doe2_sim_parser.utils.convert_path import convert_path
from doe2_sim_parser.utils.data_types import SIM, Path, Report


def write_sim(sim: SIM, folder: Path = None):
    """
    Write the entire sim report
    :param sim: a SIM object
    :param folder:
    :return:
    """
    dict_reports: Dict[str, List[str]] = defaultdict(list)

    for report in sim.normal_reports:  # type: Report
        dict_reports[report.code].extend(report.report)

    folder = convert_path(folder) if folder else sim.path.parent

    for code, report in dict_reports.items():  # type: str, list
        report_file = folder / "{sim_name} - {code}{suffix}".format(
            sim_name=sim.path.stem, code=code, suffix=sim.path.suffix)
        with report_file.open(mode="w") as file:
            file.writelines(report)
