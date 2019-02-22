import shutil
import tempfile
from unittest import TestCase

from doe2_sim_parser.split_sim import split_sim
from doe2_sim_parser.utils.convert_path import convert_path
from doe2_sim_parser.write_sim import write_sim
from tests import SAMPLE_SIM


class WriteSIMTest(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_write_sim(self):
        sim = split_sim(SAMPLE_SIM)
        result = write_sim(sim, self.test_dir)

        files = set(convert_path(self.test_dir).iterdir())

        report_code = set(
            convert_path(self.test_dir) / "{sim_name} - {code}{suffix}".format(
                sim_name=sim.path.stem,
                code=report.code,
                suffix=sim.path.suffix) for report in sim.normal_reports)
        report_code.add(
            convert_path(
                self.test_dir) / "{sim_name} - hourly report{suffix}".format(
                sim_name=sim.path.stem, suffix=sim.path.suffix))
        self.assertSetEqual(files, report_code)
