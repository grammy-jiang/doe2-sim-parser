from unittest import TestCase

from doe2_sim_parser.parse_report_es_d import parse_es_d
from tests import SAMPLE_SIM_ES_D


class ParseReportESDTest(TestCase):
    maxDiff = None

    def setUp(self):
        with SAMPLE_SIM_ES_D.open() as f:
            self.report = f.readlines()

        self.report_csv = [
            ["sample", "DOE-2.2-48z", "2/24/2019", "4:28:19", "1"],
            ["REPORT", "ES-D", "Energy Cost Summary", "WEATHER FILE", "CHICAGO, IL"],
            [
                "UTILITY-RATE",
                "RESOURCE",
                "METERS",
                "METERED\nENERGY\nUNITS/YR",
                "",
                "TOTAL\nCHARGE\n($)",
                "VIRTUAL\nRATE\n($/UNIT)",
                "RATE USED\nALL YEAR?",
            ],
            [
                "SCE TOU-8A Elec Rate",
                "ELECTRICITY",
                "EM1",
                "5020082.",
                "KWH",
                "972198.",
                "0.1937",
                "YES",
            ],
            [
                "SoCalGas GN-10 Gas Rate",
                "NATURAL-GAS",
                "FM1",
                "46804.",
                "THERM",
                "24958.",
                "0.5332",
                "YES",
            ],
            ["", "", "", "", "", "997156."],
            ["", "", "", "", "ENERGY COST/GROSS BLDG AREA", "1.33"],
            ["", "", "", "", "ENERGY COST/NET BLDG AREA", "1.33"],
        ]

    def tearDown(self):
        pass

    def test_parse_es_d(self):
        self.assertSequenceEqual(parse_es_d(self.report), self.report_csv)
