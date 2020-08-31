import unittest
from bibleq import create_app

class TestFactory(unittest.TestCase):

    def test_config_loading(self):
        self.assertIsNot(create_app().testing, True)
        self.assertIs(create_app({'TESTING': True}).testing, True)