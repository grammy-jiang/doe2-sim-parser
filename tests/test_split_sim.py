import logging
from pathlib import Path
from unittest import TestCase

from doe2_sim_parser.split_sim import parse_report, read_sim, split_sim
from doe2_sim_parser.utils.data_types import SIM, Report
from tests import SAMPLE_SIM

from doe2_sim_parser.split_sim import logger as split_sim_logger

class ParseReportTest(TestCase):
    def test_parse_normal_report(self):
        report = (
            "\x0c05 proposed                                                                      DOE-2.2-48t    9/10/2017    16:19:00  BDL RUN  1\n",
            "                                                                                                                        \n",
            "REPORT- PS-H Loads and Energy Usage for     Open Tower                                      WEATHER FILE- EPW MACAU,-,MAC     \n",
            "--------------------------------------------------------------------------------------------------------------(CONTINUED)--------\n",
            "           ==========  ==========  ==========  ==========     ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====\n",
            "\n",
            "YR    SUM    8802.100    8639.917       0.000       0.000 LOAD3682   463   804   479   504   514   375   563   535   270   571  8760\n",
            "     PEAK    3048.030       8.403       0.000       0.000 ELEC2946  1077  1024   185   254   150    59     2     1     0     0  5698\n",
            "  MON/DAY        6/23        7/19        0/ 0        0/ 0\n",
            "\n",
            "  MAXIMUM TOWER SUPPLY TEMPERATURE WAS  89.4F ON  7/19 AT 14:00\n",
        )

        report_parsed = parse_report(report)
        self.assertIsInstance(report_parsed, Report)
        self.assertEqual(report_parsed.type_, "normal_report")
        self.assertEqual(report_parsed.code, "PS-H")
        self.assertEqual(report_parsed.name,
                         "Loads and Energy Usage for     Open Tower")
        self.assertEqual(report_parsed.report, report)

    def test_parse_hourly_report(self):
        report_1 = (
            "\x0csample                                                                           DOE-2.2-48z    2/22/2019    23:17:20  BDL RUN  1",
            "                                                                                                                        ",
            "HOURLY REPORT- Hourly Report                     HVAC                            WEATHER FILE- CHICAGO, IL          Pg:    1 -  1",
            "---------------------------------------------------------------------------------------------------------------------------------",
            "MMDDHH   EM1         EM1         EM1         EM1         EM1         EM1         EM1         EM1         EM1         EM1     ",
            "                                                                                                                             ",
            "            LIGHT        TASK       EQUIP        HEAT        COOL       HTREJ         AUX        VENT        REFG        SUPP",
            "          END USE     END USE     END USE     END USE     END USE     END USE     END USE     END USE     END USE     END USE",
            "         KWH         KWH         KWH         KWH         KWH         KWH         KWH         KWH         KWH         KWH     ",
            "                                                                                                                             ",
            "         ----( 1)    ----( 2)    ----( 3)    ----( 4)    ----( 5)    ----( 6)    ----( 7)    ----( 8)    ----( 9)    ----(10)",
            " 1 1 1       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 2       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 3       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 4       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 5       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 6       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 7       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 8       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 9       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 110       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 111       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 112       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 113       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 114       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 115       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 116       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 117       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 118       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 119       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 120       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 121       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 122       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 123       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 124       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            "",
            " DAILY SUMMARY (JAN  1)",
            "    MN       0.430       1.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            "    MX       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            "    SM      10.322       0.000     113.613       0.000       0.000       0.000      12.000       0.000       0.000       0.000",
            "    AV       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
        )

        report_2 = (
            "\x0csample                                                                           DOE-2.2-48z    2/22/2019    23:17:20  BDL RUN  1",
            "                                                                                                                        ",
            "HOURLY REPORT- Hourly Report 2                   HVAC                            WEATHER FILE- EPW Kunming,Yunnan,C Pg:    1 -  1",
            "---------------------------------------------------------------------------------------------------------------------------------",
            "MMDDHH   EM1         EM1         EM1         EM1         EM1         EM1         EM1         EM1         EM1         EM1     ",
            "                                                                                                                             ",
            "            LIGHT        TASK       EQUIP        HEAT        COOL       HTREJ         AUX        VENT        REFG        SUPP",
            "          END USE     END USE     END USE     END USE     END USE     END USE     END USE     END USE     END USE     END USE",
            "         KWH         KWH         KWH         KWH         KWH         KWH         KWH         KWH         KWH         KWH     ",
            "                                                                                                                             ",
            "         ----( 1)    ----( 2)    ----( 3)    ----( 4)    ----( 5)    ----( 6)    ----( 7)    ----( 8)    ----( 9)    ----(10)",
            " 1 1 1       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 2       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 3       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 4       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 5       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 6       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 7       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 8       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 1 9       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 110       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 111       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 112       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 113       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 114       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 115       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 116       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 117       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 118       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 119       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 120       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 121       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 122       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 123       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            " 1 124       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            "",
            " DAILY SUMMARY (JAN  1)",
            "    MN       0.430       1.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            "    MX       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
            "    SM      10.322       0.000     113.613       0.000       0.000       0.000      12.000       0.000       0.000       0.000",
            "    AV       0.430       0.000       4.734       0.000       0.000       0.000       0.500       0.000       0.000       0.000",
        )
        for i, report in enumerate([report_1, report_2]):
            with self.subTest(i=i):
                report_parsed = parse_report(report)
                self.assertIsInstance(report_parsed, Report)
                self.assertEqual(report_parsed.type_, "hourly_report")
                self.assertEqual(report_parsed.code, None)
                self.assertEqual(report_parsed.name, None)
                self.assertEqual(report_parsed.report, report)


class ReadSIMTest(TestCase):
    def test_read_sim(self):
        for report in read_sim(SAMPLE_SIM):
            self.assertIsInstance(report, Report)


class ParseSIMTest(TestCase):
    def test_parse_sim(self):
        with self.assertLogs(logger=split_sim_logger, level=logging.INFO) as cm:
            sim = split_sim(SAMPLE_SIM)
        self.assertEqual(
            cm.output,
            ['INFO:doe2_sim_parser.split_sim:Receive sim: {}'.format(SAMPLE_SIM),
             'INFO:doe2_sim_parser.split_sim:This sim has 460 normal reports, 1095 hourly reports']
        )

        self.assertIsInstance(sim, SIM)
        self.assertIsInstance(sim.path, Path)
        self.assertIsInstance(sim.normal_reports, tuple)

        for report in sim.normal_reports:
            self.assertIsInstance(report, Report)
            self.assertEqual(report.type_, "normal_report")
        self.assertIsInstance(sim.hourly_reports, tuple)

        for report in sim.hourly_reports:
            self.assertIsInstance(report, Report)
            self.assertEqual(report.type_, "hourly_report")
