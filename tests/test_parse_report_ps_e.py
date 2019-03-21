import pprint
from unittest import TestCase

from doe2_sim_parser.parse_report_ps_e import parse_ps_e
from doe2_sim_parser.utils.data_types import Report
from tests import SAMPLE_SIM_PS_E

pp = pprint.PrettyPrinter(indent=4, width=180)


class ParseReportESDTest(TestCase):
    maxDiff = None

    def setUp(self):
        with SAMPLE_SIM_PS_E.open() as f:
            self.report = Report(
                type_='normal_report',
                code='PS-E',
                name='Energy End-Use Summary for all Electric Meters',
                report=f.readlines(),
                report_no=None,
                page_no=None
            )

        self.report_csv = [
        ]

    def tearDown(self):
        pass

    def test_parse_es_d(self):
        pp.pprint(parse_ps_e([self.report]))
        self.assertSequenceEqual(parse_ps_e([self.report]), self.report_csv)
