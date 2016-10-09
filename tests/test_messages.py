import unittest
import datetime
from .models import Message


class MessageTestCase(unittest.TestCase):
    """tests for messages"""
    DATA = { 'sender': 'stuff', 
            'data': 'stuff', }  
    def setUp(self, *args, **kwargs):
        self.message = Message
        print(self.shortDescription())

    def test_is_valid_true(self):
        """is valid should return true if kwargs are not none"""
        self.assertTrue(self.message(**self.DATA))

    def test_has_timestamp(self):
        """when a message obj is created, there should be a timestamp"""
        message = self.message(**self.DATA)
        self.assertIsInstance(message.create_timestamp(), datetime.datetime)

    def test_assert_is_raiseed(self):
        """if either sender or data is not set, an AssertionError is raised"""
        data = {'data': 'ddd'}
        data2 = {'sender': 'stuff'}
        with self.assertRaises(AssertionError):
            self.message(**data)
            self.message(**data2)

    def test_is_valid_set_initial(self):
        """is_valid sets initial"""
        self.assertDictEqual(self.DATA,
                             self.message(**self.DATA)._initial)

if __name__ == '__main__':
    unittest.main()
