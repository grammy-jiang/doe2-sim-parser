import os
import shutil
import tempfile
from itertools import chain
from pathlib import Path
from unittest import TestCase

from doe2_sim_parser.settings import TARGET_REPORTS
from doe2_sim_parser.utils.convert_path import convert_path
from doe2_sim_parser.utils.data_types import Report
from doe2_sim_parser.write_sim import write_sim

CWD = Path(os.getcwd())


class WriteSIMTest(TestCase):
    def setUp(self):
        self.target_reports = dict(map(lambda x: x[1:3], TARGET_REPORTS))
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_write_sim(self):
        reports = (
            Report(
                type_='normal_report',
                code='PS-H',
                name='Loads and Energy Usage',
                report=(
                    '\x0c05 proposed                                                                      DOE-2.2-48t    9/10/2017    16:19:00  BDL RUN  1\n',
                    '                                                                                                                        \n',
                    'REPORT- PS-H Loads and Energy Usage for     Open Tower                                      WEATHER FILE- EPW MACAU,-,MAC     \n',
                    '--------------------------------------------------------------------------------------------------------------(CONTINUED)--------\n',
                    '           ==========  ==========  ==========  ==========     ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====\n',
                    '\n',
                    'YR    SUM    8802.100    8639.917       0.000       0.000 LOAD3682   463   804   479   504   514   375   563   535   270   571  8760\n',
                    '     PEAK    3048.030       8.403       0.000       0.000 ELEC2946  1077  1024   185   254   150    59     2     1     0     0  5698\n',
                    '  MON/DAY        6/23        7/19        0/ 0        0/ 0\n',
                    '\n',
                    '  MAXIMUM TOWER SUPPLY TEMPERATURE WAS  89.4F ON  7/19 AT 14:00\n')),
        )

        code = 'PS-H'
        file = convert_path(
            self.test_dir) / 'test case - PS-H {name}.SIM'.format(
            name=self.target_reports[code].replace('/', '_'))

        result = write_sim(file, reports)
        self.assertEqual(result, 1032)

        with file.open() as f:
            self.assertSequenceEqual(
                f.readlines(),
                tuple(chain(*map(lambda report: report.report, reports))))
