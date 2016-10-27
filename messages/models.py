import json
import datetime


class BaseMessage:
    """
    Represents a message.

    :param data
    :param sender
    .. py:attribute:: _initial message obj before encode, internal use
    """
    
    _initial = {}  # type: Dict[str, str]
    
    def __init__(self, data=None, sender=None):
        self.is_valid(data, sender)
        self._initial.update({'create_timestamp': self.create_timestamp()})

    def is_valid(self, data=None, sender=None):
        """checks for a valid message, sets .initial
        :returns: boolean
        :rtype: bool
        """
        # TODO
        assert sender is not None
        assert data is not None
        self.sender = sender
        self.data = data
        return True

    def create_timestamp(self):
        """creation timestamp, utc
        :return: datetime.datetime.utcnow()
        :rtype: object
        """
        return datetime.datetime.utcnow().isoformat()

    def encode(self):
        """JSON encodes .initial
        :returns: json.dump
        :rtype: bytes
        """
        return json.dumps(self._initial)
