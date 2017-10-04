import os
from pathlib import Path
from unittest import TestCase

from doe2_sim_parser.parse_sim import parse_report
from doe2_sim_parser.parse_sim import parse_sim
from doe2_sim_parser.parse_sim import read_sim
from doe2_sim_parser.utils.data_types import Report
from doe2_sim_parser.utils.data_types import SIM

CWD = Path(os.getcwd())


class ParseReportTest(TestCase):
    def test_parse_normal_report(self):
        report = (
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
            '  MAXIMUM TOWER SUPPLY TEMPERATURE WAS  89.4F ON  7/19 AT 14:00\n')

        report_parsed = parse_report(report)
        self.assertIsInstance(report_parsed, Report)
        self.assertEqual(report_parsed.type_, 'normal_report')
        self.assertEqual(report_parsed.code, 'PS-H')
        self.assertEqual(report_parsed.name,
                         'Loads and Energy Usage for     Open Tower')
        self.assertEqual(report_parsed.report, report)

    def test_parse_hourly_report(self):
        report = (
            '\x0c05 proposed                                                                      DOE-2.2-48t    9/10/2017    16:19:00  BDL RUN  1\n',
            '                                                                                                                        \n',
            'HOURLY REPORT- Hourly Report                     HVAC                            WEATHER FILE- EPW MACAU,-,MAC      Pg:  365 -  3\n',
            '---------------------------------------------------------------------------------------------------------------------------------\n',
            '        FM1        FM1        FM1        FM1        FM1     \n',
            '                                                            \n',
            '            REFG       SUPP        DHW        EXT      TOTAL\n',
            '         END USE    END USE    END USE    END USE      USAGE\n',
            '        BTU        BTU        BTU        BTU        BTU     \n',
            '                                                            \n',
            '        ----( 9)   ----(10)   ----(11)   ----(12)   ----(20)\n',
            '1231 1         0.         0.         0.         0.         0.\n',
            '1231 2         0.         0.         0.         0.         0.\n',
            '1231 3         0.         0.         0.         0.         0.\n',
            '1231 4         0.         0.         0.         0.         0.\n',
            '1231 5         0.         0.         0.         0.         0.\n',
            '1231 6         0.         0.         0.         0.         0.\n',
            '1231 7         0.         0.         0.         0.         0.\n',
            '1231 8         0.         0.         0.         0.         0.\n',
            '1231 9         0.         0.         0.         0.         0.\n',
            '123110         0.         0.         0.         0.         0.\n',
            '123111         0.         0.         0.         0.         0.\n',
            '123112         0.         0.         0.         0.         0.\n',
            '123113         0.         0.         0.         0.         0.\n',
            '123114         0.         0.         0.         0.         0.\n',
            '123115         0.         0.         0.         0.         0.\n',
            '123116         0.         0.         0.         0.         0.\n',
            '123117         0.         0.         0.         0.         0.\n',
            '123118         0.         0.         0.         0.         0.\n',
            '123119         0.         0.         0.         0.         0.\n',
            '123120         0.         0.         0.         0.         0.\n',
            '123121         0.         0.         0.         0.         0.\n',
            '123122         0.         0.         0.         0.         0.\n',
            '123123         0.         0.         0.         0.         0.\n',
            '123124         0.         0.         0.         0.         0.\n',
            '\n',
            ' DAILY SUMMARY (DEC 31)\n',
            '    MN         0.         0.         0.         0.         0.\n',
            '    MX         0.         0.         0.         0.         0.\n',
            '    SM         0.         0.         0.         0.         0.\n',
            '    AV         0.         0.         0.         0.         0.\n',
            '\n',
            ' MONTHLY SUMMARY (DEC)\n',
            '    MN         0.         0.         0.         0.         0.\n',
            '    MX         0.         0.         0.         0.    546492.\n',
            '    SM         0.         0.         0.         0.  21997594.\n',
            '    AV         0.         0.         0.         0.     29567.\n',
            '\n',
            ' YEARLY SUMMARY\n',
            '    MN         0.         0.         0.         0.         0.\n',
            '    MX         0.         0.         0.         0.    738826.\n',
            '    SM         0.         0.         0.         0. 278138368.\n',
            '    AV         0.         0.         0.         0.     31751.\n')

        report_parsed = parse_report(report)
        self.assertIsInstance(report_parsed, Report)
        self.assertEqual(report_parsed.type_, 'hourly_report')
        self.assertEqual(report_parsed.code, None)
        self.assertEqual(report_parsed.name, None)
        self.assertEqual(report_parsed.report, report)


class ReadSIMTest(TestCase):
    def test_read_sim(self):
        if CWD.stem == 'tests':
            path = CWD / 'test case.SIM'
        else:
            path = CWD / 'tests' / 'test case.SIM'
        # path = cwd / Path(
        #     'tests/test case.SIM'
        # )
        for report in read_sim(path):
            self.assertIsInstance(report, Report)


class ParseSIMTest(TestCase):
    def test_parse_sim(self):
        if CWD.stem == 'tests':
            path = CWD / 'test case.SIM'
        else:
            path = CWD / 'tests' / 'test case.SIM'

        sim = parse_sim(path)
        self.assertIsInstance(sim, SIM)
        self.assertIsInstance(sim.path, Path)
        self.assertIsInstance(sim.normal_reports, tuple)
        for report in sim.normal_reports:
            self.assertIsInstance(report, Report)
            self.assertEqual(report.type_, 'normal_report')
        self.assertIsInstance(sim.hourly_reports, tuple)
        for report in sim.hourly_reports:
            self.assertIsInstance(report, Report)
            self.assertEqual(report.type_, 'hourly_report')
