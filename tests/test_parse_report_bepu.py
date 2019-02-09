from unittest import TestCase

from doe2_sim_parser.parse_report_bepu import parse_bepu
from tests import SAMPLE_SIM_BEPU


class ParseReportBEPUTest(TestCase):
    def setUp(self):
        with SAMPLE_SIM_BEPU.open() as f:
            self.report = f.readlines()

        self.report_csv = [
            ["sample", "DOE-2.2-48z", "2/03/2019", "13:58:04", "BDL RUN", "1"],
            [
                "REPORT",
                "BEPU",
                "Building Utility Performance",
                "WEATHER FILE",
                "CHICAGO, IL",
            ],
            [
                "METER",
                "TYPE",
                "UNIT",
                "LIGHTS",
                "TASK\nLIGHTS",
                "MISC\nEQUIP",
                "SPACE\nHEATING",
                "SPACE\nCOOLING",
                "HEAT\nREJECT",
                "PUMPS\n& AUX",
                "VENT\nFANS",
                "REFRIG\nDISPLAY",
                "HT PUMP\nSUPPLEN",
                "DOMEST\nHOT WTR",
                "EXT\nUSAGE",
                "TOTAL",
            ],
            [
                "EM1",
                "ELECTRICITY",
                "KWH",
                "69156.",
                "0.",
                "92425.",
                "0.",
                "25606.",
                "0.",
                "2116.",
                "22465.",
                "0.",
                "0.",
                "0.",
                "0.",
                "211768.",
            ],
            [
                "FM1",
                "NATURAL-GAS",
                "THERM",
                "0.",
                "0.",
                "0.",
                "3417.",
                "0.",
                "0.",
                "0.",
                "0.",
                "0.",
                "0.",
                "410.",
                "0.",
                "3827.",
            ],
            [
                "TOTAL ELECTRICITY",
                "ELECTRICITY",
                "211768.",
                "KWH",
                "8.471",
                "KWH",
                "/SQFT-YR GROSS-AREA",
                "8.471",
                "KWH",
                "/SQFT-YR NET-AREA",
            ],
            [
                "TOTAL NATURAL-GAS",
                "NATURAL-GAS",
                "3827.",
                "THERM",
                "0.153",
                "THERM",
                "/SQFT-YR GROSS-AREA",
                "0.153",
                "THERM",
                "/SQFT-YR NET-AREA",
            ],
            [
                "PERCENT OF HOURS ANY SYSTEM ZONE OUTSIDE OF THROTTLING RANGE",
                "2.35"
            ],
            ["PERCENT OF HOURS ANY PLANT LOAD NOT SATISFIED", "0.00"],
            ["HOURS ANY ZONE ABOVE COOLING THROTTLING RANGE", "59"],
            ["HOURS ANY ZONE BELOW HEATING THROTTLING RANGE", "6"],
            ["NOTE:  ENERGY IS APPORTIONED HOURLY TO ALL END-USE CATEGORIES."],
        ]

    def tearDown(self):
        pass

    def test_parse_beps(self):
        self.assertSequenceEqual(parse_bepu(self.report), self.report_csv)
