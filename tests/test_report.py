import pprint
from unittest import TestCase

from doe2_sim_parser.report import SingleReport, Report
from tests import SAMPLE_SIM_BEPS, SAMPLE_SIM_BEPU, SAMPLE_SIM_ES_D

pp = pprint.PrettyPrinter(indent=4)


class SingleReportTest(TestCase):
    def setUp(self):
        self.reports = {
            'BEPS': {
                'report': SAMPLE_SIM_BEPS,
                'type': 'normal',
                'code': 'BEPS',
                'name': 'Building Energy Performance',
            },
            'BEPU': {
                'report': SAMPLE_SIM_BEPU,
                'type': 'normal',
                'code': 'BEPU',
                'name': 'Building Utility Performance',
            },
            'ES-D': {
                'report': SAMPLE_SIM_ES_D,
                'type': 'normal',
                'code': 'ES-D',
                'name': 'Energy Cost Summary',
            }
        }

    def test_single_report(self):
        for name, report in self.reports.items():
            with self.subTest(name=name):
                with report['report'].open(mode='r') as f:
                    _report = f.readlines()
                single_report = SingleReport.from_text(_report)
                self.assertEqual(single_report.type, report['type'])
                self.assertEqual(single_report.code, report['code'])
                self.assertEqual(single_report.name, report['name'])


class ReportTest(TestCase):
    def setUp(self):
        pass

    def test_report(self):
        pp.pprint(Report.__subclasses__())
