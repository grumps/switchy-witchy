import unittest
import datetime
from switchywitchy.messages.models import BaseMessage


class MessageTestCase(unittest.TestCase):
    """tests for messages"""
    DATA = { 'sender': 'stuff', 
            'data': 'stuff', }  
    def setUp(self, *args, **kwargs):
        self.message = BaseMessage
        print(self.shortDescription())

    def test_is_valid_true(self):
        """is valid should return true if kwargs are not none"""
        self.assertTrue(self.message(**self.DATA))

    def test_has_timestamp(self):
        """when a message obj is created, there should be a timestamp"""
        message = self.message(**self.DATA)
        ts_format = '%Y-%m-%dT%H:%M:%S.%f'
        # just make sure the timestamp parses correctly
        assert datetime.datetime.strptime(
                message.create_timestamp(),
                ts_format)

    def test_assert_is_raised(self):
        """if either sender or data is not set, an AssertionError is raised"""
        data = {'data': 'ddd'}
        data2 = {'sender': 'stuff'}
        with self.assertRaises(AssertionError):
            self.message(**data)
            self.message(**data2)

    def test_is_valid_set_initial(self):
        """is_valid sets initial"""
        message = self.message(**self.DATA)
        # we don't want to compare timestamps
        message._initial.pop('create_timestamp') 
        self.assertEqual(message.sender,
                self.DATA['sender'])
        self.assertEqual(message.data,
                self.DATA['data'])
