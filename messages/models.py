__author__ = 'Maxwell J. Resnick'
__docformat__ = 'reStructuredText'
import json
import datetime

class Message:
    """
    Represents a message.
    
    :param data
    :param sender
    .. py:attribute:: _initial base message obj, internal use
    """
    _initial = None

    def __init__(self, data=None, sender=None):
        self.is_valid(data, sender)
        self._initial.update({'create_timestamp': self.create_timestamp})

    def is_valid(self, data=None, sender=None):
        """checks for a valid message, sets .initial
        :returns: boolean
        :rtype: bool
        """
        assert sender is not None
        assert data is not None
        self._initial = {
                'sender': sender,
                'data': data}
        return True
    
    def create_timestamp(self):
        """creation timestamp, utc
        :return: datetime.datetime.utcnow()
        :rtype: object
        """
        return datetime.datetime.utcnow()

    def encode(self):
        """JSON encodes .initial
        :returns: json.dump
        :rtype: str
        """
        return json.dump(initial) 
