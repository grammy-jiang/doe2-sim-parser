import logging
import pprint

from doe2_sim_parser import Path_, split_sim

logger = logging.getLogger(__name__)

pp = pprint.PrettyPrinter(indent=4, width=120)

if __name__ == '__main__':
    path_sim: Path_ = r'../tests/test case - Baseline Design.SIM'
    path_xlsx: Path_ = r'../tests/test case.xlsx'

    # split SIM
    target_folder: Path_ = r'target'

    result = split_sim(path_sim, target_folder=target_folder)

    # result = split_sim(path_sim, target_folder=target_folder,
    #                    target_reports=['BEPS', 'BEPU'])

    pp.pprint(result)

    # save to xlsx file
    # result = transfer_sim2xlsx(path_sim, path_xlsx)
