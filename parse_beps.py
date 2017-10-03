from openpyxl import Workbook

from doe2_sim_parser.report_parser_beps import write_beps
from doe2_sim_parser.utils import Path_
from doe2_sim_parser.utils import convert_path

if __name__ == '__main__':
    path: Path_ = (
        r"tests/"
        r"test case - Baseline Design - BEPS Building Energy Performance.SIM")

    wb = Workbook()

    write_beps(wb=wb,
               report=convert_path(path).open('r').readlines())

    wb.save('temp.xlsx')
