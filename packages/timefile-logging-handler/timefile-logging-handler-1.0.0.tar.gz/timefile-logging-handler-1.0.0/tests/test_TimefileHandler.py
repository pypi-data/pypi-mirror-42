# coding=utf-8
import os
import time
import logging
from unittest import TestCase

from timefile_handler.handler import TimefileHandler

current_path = os.path.dirname(os.path.abspath(__file__))
raw_filename = os.path.join(current_path, 'app_%Y%m%d_%H%M%S.log')


class TestTimefileHandler(TestCase):
    def setUp(self):
        self.handler = TimefileHandler(raw_filename, 'a')
        standard = logging.Formatter("%(asctime)s||%(levelname)s||%(name)s||%(filename)s:%(funcName)s:%(lineno)d||%(message)s")
        self.handler.setFormatter(standard)

    def test_file_exist(self):
        logger = logging.getLogger(__name__)
        logger.addHandler(self.handler)

        logger.error("Tesing file exist")
        self.assertEqual(self.handler.getFilename(), time.strftime(raw_filename))

    def test_file_changed(self):
        logger = logging.getLogger(__name__)
        logger.addHandler(self.handler)
        logger.error("Testing before file changed")
        filename = self.handler.getFilename()
        time.sleep(2)
        logger.warning("Testing after file changed")
        new_filename = self.handler.getFilename()

        self.assertNotEqual(filename, new_filename)

    def tearDown(self):
        import glob
        for f in glob.glob(os.path.join(current_path, '*.log')):
            try:
                os.remove(f)
            except Exception:
                pass
