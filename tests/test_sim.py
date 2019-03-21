import pprint
from unittest import TestCase

from doe2_sim_parser.sim import SIM
from tests import SAMPLE_SIM

pp = pprint.PrettyPrinter(indent=4)


class SIMTest(TestCase):
    def setUp(self):
        self.sim = SAMPLE_SIM

    def test_sim(self):
        sim = SIM.from_path(self.sim)
        sim.split()
        pp.pprint(sim.path)
        for k, v in sim.items():
            print(k, len(v))
