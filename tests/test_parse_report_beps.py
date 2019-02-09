from unittest import TestCase

from doe2_sim_parser.parse_report_beps import parse_beps
from tests import SAMPLE_SIM_BEPS


class ParseReportBEPSTest(TestCase):
    def setUp(self):
        with SAMPLE_SIM_BEPS.open() as f:
            self.report = f.readlines()

        self.report_csv = [
            ["sample", "DOE-2.2-48z", "2/03/2019", "13:58:04", "BDL RUN", "1"],
            ["REPORT", "BEPS Building Energy Performance", "WEATHER FILE",
             "CHICAGO, IL"],
            ["METER", "TYPE", "UNIT", "LIGHTS", "TASK\nLIGHTS", "MISC\nEQUIP",
             "SPACE\nHEATING", "SPACE\nCOOLING", "HEAT\nREJECT", "PUMPS\n& AUX",
             "VENT\nFANS", "REFRIG\nDISPLAY", "HT PUMP\nSUPPLEN",
             "DOMEST\nHOT WTR", "EXT\nUSAGE", "TOTAL"],
            ["EM1", "ELECTRICITY", "MBTU", "236.0", "0.0", "315.4", "0.0",
             "87.4", "0.0", "7.2", "76.7", "0.0", "0.0", "0.0", "0.0", "722.8"],
            ["FM1", "NATURAL-GAS", "MBTU", "0.0", "0.0", "0.0", "341.7", "0.0",
             "0.0", "0.0", "0.0", "0.0", "0.0", "41.0", "0.0", "382.7"],
            ["", "", "MBTU", "236.0", "0.0", "315.4", "341.7", "87.4", "0.0",
             "7.2", "76.7", "0.0", "0.0", "41.0", "0.0", "1105.5"],
            ["TOTAL SITE ENERGY", "1105.48", "MBTU", "44.2",
             "KBTU/SQFT-YR GROSS-AREA", "44.2", "KBTU/SQFT-YR NET-AREA"],
            ["TOTAL SOURCE ENERGY", "2551.00", "MBTU", "102.0",
             "KBTU/SQFT-YR GROSS-AREA", "102.0", "KBTU/SQFT-YR NET-AREA"],
            ["PERCENT OF HOURS ANY SYSTEM ZONE OUTSIDE OF THROTTLING RANGE",
             "2.35"],
            ["PERCENT OF HOURS ANY PLANT LOAD NOT SATISFIED", "0.00"],
            ["HOURS ANY ZONE ABOVE COOLING THROTTLING RANGE", "59"],
            ["HOURS ANY ZONE BELOW HEATING THROTTLING RANGE", "6"],
            ["NOTE:  ENERGY IS APPORTIONED HOURLY TO ALL END-USE CATEGORIES."]
        ]

    def tearDown(self):
        pass

    def test_parse_beps(self):
        self.assertSequenceEqual(parse_beps(self.report), self.report_csv)
