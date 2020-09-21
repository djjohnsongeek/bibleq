import unittest

from classes.Util import Util


class TestUtilClass(unittest.TestCase):

    def test_contains_upper(self):
        with self.assertRaises(TypeError):
            Util.contains_upper(1)

        self.assertTrue(Util.contains_upper('aaaA'))
        self.assertTrue(Util.contains_upper('sdkfja;!@$@!sdlkjfA'))
        self.assertFalse(Util.contains_upper('1213lij;paslid;lj!)(#*$)'))

    def test_contains_lower(self):
        with self.assertRaises(TypeError):
            Util.contains_lower(1)

        self.assertTrue(Util.contains_lower('aa!@##aaA'))
        self.assertTrue(Util.contains_lower('Asdkfja;!@$@!sdlkjfA'))
        self.assertFalse(Util.contains_lower('1213;PASLKJ!)(#*$)'))

    def test_contains_num(self):
        with self.assertRaises(TypeError):
            Util.contains_num(1)
    
        self.assertTrue(Util.contains_num('aa!@##aaA1'))
        self.assertTrue(Util.contains_num('7AsdkfdlkjfA'))
        self.assertFalse(Util.contains_num('dafPASLKJ!)(#*$)'))

    def test_authenticate(self):
        session = {}

        self.assertFalse(Util.authenticate(session, 1))

        session['user'] = {
            'first_name': 'Daniel',
            'last_name': 'Johnson',
            'account_level': 1,
        }

        self.assertTrue(Util.authenticate(session, 1))
        self.assertFalse(Util.authenticate(session, 2))
