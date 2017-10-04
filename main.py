import logging

from doe2_sim_parser import SIM
from doe2_sim_parser.settings import TARGET_REPORTS
from doe2_sim_parser.parse_sim import parse_sim
from doe2_sim_parser.parse_sim import write_sim

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sim_path = r'tests/test case.SIM'

    # path, reports = parse_sim(sim_path)

    sim: SIM = parse_sim(sim_path)

    for report_obj in sim.reports:
        if report_obj.code in TARGET_REPORTS:
            write_sim(report_obj, sim.path)
        else:
            logger.info(
                '{} is not mentioned in the settings'.format(report_obj.code))
