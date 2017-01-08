"""Messages to be sent between systems"""
__author__ = 'Maxwell J. Resnick'
__docformat__ = 'reStructuredText'

from . import models

class Message(object):
    """
    generates message obj.
    :param dict data: data for message.
    """
    @staticmethod
    def create(data):
        """factory for creating an object"""
        sender = 'this machine'
        return models.BaseMessage(data, sender)
