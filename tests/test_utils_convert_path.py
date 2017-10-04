from pathlib import Path
from unittest import TestCase

from doe2_sim_parser.utils.convert_path import convert_path


class ConvertPathTest(TestCase):
    def test_str(self):
        path = 'test'
        self.assertIsInstance(convert_path(path), Path)

    def test_path(self):
        path = Path('test')
        self.assertIsInstance(convert_path(path), Path)
