from unittest import TestCase

from doe2_sim_parser.parse_report_es_d import parse_es_d
from tests import SAMPLE_SIM_ES_D


class ParseReportESDTest(TestCase):
    def setUp(self):
        with SAMPLE_SIM_ES_D.open() as f:
            self.report = f.readlines()

        self.report_csv = [
            ["sample", "DOE-2.2-48z", "2/03/2019", "13:58:04", "BDL RUN", "1"],
            [
                "REPORT", "ES-D", "Energy Cost Summary", "WEATHER FILE",
                "CHICAGO, IL"
            ],
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
                "SCE GS-2 Elec Rate",
                "ELECTRICITY",
                "EM1",
                "211768.",
                "KWH",
                "35072.",
                "0.1656",
                "YES",
            ],
            [
                "SoCalGas GN-10 Gas Rate",
                "NATURAL-GAS",
                "FM1",
                "3827.",
                "THERM",
                "2617.",
                "0.6837",
                "YES",
            ],
            ["", "", "", "", "", "37689."],
            ["", "", "", "", "ENERGY COST/GROSS BLDG AREA", "1.51"],
            ["", "", "", "", "ENERGY COST/NET BLDG AREA", "1.51"],
        ]

    def tearDown(self):
        pass

    def test_parse_es_d(self):
        es_d = parse_es_d(self.report)
        with open("sample - ES-D.csv", "w") as f:
            import csv

            fwriter = csv.writer(f)

            for line in es_d:
                fwriter.writerow(line)

        self.assertSequenceEqual(parse_es_d(self.report), self.report_csv)
