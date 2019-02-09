import pprint
from unittest import TestCase

from doe2_sim_parser.parse_report_es_d import parse_es_d
from tests import SAMPLE_SIM_ES_D

pp = pprint.PrettyPrinter(indent=4)


class ParseReportESDTest(TestCase):
    def setUp(self):
        with SAMPLE_SIM_ES_D.open() as f:
            self.report = f.readlines()

        self.report_csv = [
            ["sample", "DOE-2.2-48z", "2/03/2019", "13:58:04", "BDL RUN", "1"],
            ['REPORT', 'ES-D Energy Cost Summary', 'WEATHER FILE',
             'CHICAGO, IL'],
            ["UTILITY-RATE", "RESOURCE", "METERS", "METERED\nENERGY\nUNITS/YR",
             "TOTAL\nCHARGE\n($)", "VIRTUAL\nRATE\n($/UNIT)",
             "RATE USED\nALL YEAR?"],
            ['SCE GS-2 Elec Rate', 'ELECTRICITY', 'EM1', '211768.', 'KWH',
             '35072.', '0.1656', 'YES'],
            ['SoCalGas GN-10 Gas Rate', 'NATURAL-GAS', 'FM1', '3827.', 'THERM',
             '2617.', '0.6837', 'YES'],
            ['TOTAL ELECTRICITY', 'ELECTRICITY', '211768.', 'KWH', '8.471',
             'KWH', '/SQFT-YR GROSS-AREA', '8.471', 'KWH', '/SQFT-YR NET-AREA'],
            ['TOTAL NATURAL-GAS', 'NATURAL-GAS', '3827.', 'THERM', '0.153',
             'THERM', '/SQFT-YR GROSS-AREA', '0.153', 'THERM',
             '/SQFT-YR NET-AREA'],
            ["PERCENT OF HOURS ANY SYSTEM ZONE OUTSIDE OF THROTTLING RANGE",
             "2.35"],
            ["PERCENT OF HOURS ANY PLANT LOAD NOT SATISFIED", "0.00"],
            ["HOURS ANY ZONE ABOVE COOLING THROTTLING RANGE", "59"],
            ["HOURS ANY ZONE BELOW HEATING THROTTLING RANGE", "6"],
            ["NOTE:  ENERGY IS APPORTIONED HOURLY TO ALL END-USE CATEGORIES."]
        ]

    def tearDown(self):
        pass

    def test_parse_es_d(self):
        es_d = parse_es_d(self.report)
        pp.pprint(es_d)
        self.assertSequenceEqual(parse_es_d(self.report), self.report_csv)
