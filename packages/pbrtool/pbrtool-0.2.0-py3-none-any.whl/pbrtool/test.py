import unittest
import os
from pbrtool.pbrtool import PBRTool


class TestPBR(unittest.TestCase):
    def setUp(self):
        self.pbrtool = PBRTool()

    def test_create_setup_cfg(self):
        path = self.pbrtool._create_setup_cfg()
        self.assertTrue(os.path.exists(path))

    def test_create_setup_py(self):
        path = self.pbrtool._create_setup_py()
        self.assertTrue(os.path.exists(path))

    def test_md_to_rst(self):
        self.pbrtool.md2rst()
        self.assertTrue(os.path.exists(
            os.path.join(self.pbrtool.path, 'README.rst')))


if __name__ == "__main__":
    unittest.main()
