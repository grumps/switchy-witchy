#-*- coding: utf-8 -*-
"""Traps capture varying events within the system"""
__author__ = "Maxwell J. Resnick"
__docformat__ = "reStructuredText"

import logging

import collections
import json

import psutil
import curio
import arrow

from .machines import StateMachineMixin

logger = logging.getLogger(__name__)


class Trap(StateMachineMixin):
    """
    An alarm or trigger, to be tripped by a process.
    Property handling is as follows:

        - Properties are assigned by default values, but are also overridden based on the configuartion of the application being watched.
        - The underlying process properties are utilized are set by prefixing the property key with `process_`
        - Properties for the trap are set by prefixing the keys in configuration with `watch_`
    """
    PROPERTIES = {
        "watch": {
            "max_cpu_usage": "30",
            "max_memory": "60",
            "heartbeat_interval": "5",
            "lower_control": "10",
            "upper_control":  "10"}
    }

    def __init__(self, properties, app_queue):
        # sets default attributes
        self.state = None
        self.process = None
        for key, value in self.PROPERTIES["watch"].items():
            setattr(self, key, value)
        self.properties = self.handle_properties(properties)
        self.memory_stats = collections.OrderedDict()
        self.cpu_stats = collections.OrderedDict()
        self.queue = curio.Queue()
        self.app_queue = app_queue
        super().__init__()

    def handle_properties(self, properties):
        """
        pops off the default trap properties, setting
        them to this instance. This is before it is passed
        down to the :class:`Proc`

        :param dict properties: dictionary of properties
        :returns: properties sans trap properties
        :rtype: dict
        """
        handled_properties = {}
        for key in properties.keys():
            property_type, property_key = key.split("_", maxsplit=1)
            try:
                if property_key in self.PROPERTIES[property_type]:
                    setattr(self, property_key, properties[key])
            except KeyError:
                if property_type == "process":
                    handled_properties.update(
                        {property_key: properties[key]})
        return handled_properties

    def check_status(self, threshold=None, current_value=None):
        """
        compare threshold value to, current value
        fail if current value
        """
        if threshold < current_value:
            return "FAIL"
        return "PASS"

    async def check_cpu(self):
        """
        checks cpu, emits check to queue
        """
        # TODO needs to be a subprocess
        current_cpu = self.process.cpu_percent(interval=1)
        current_time = arrow.utcnow().timestamp
        logger.debug("{} max_cpu_usage {} current_usage {}".format(
            current_time, self.max_cpu_usage, current_cpu))
        status = self.check_status(
            threshold=self.max_cpu_usage, current_value=current_cpu)
        logger.debug("{} check cpu status is: {}".format(current_time, status))
        self.cpu_stats[current_time] = (current_cpu, status)
        await self.queue.put(("cpu_utilization", current_time, self.cpu_stats))

    async def check_memory(self):
        """
        checks memory, emits status to queue
        """
        current_memory = self.process.memory_percent()
        current_time = arrow.utcnow().timestamp
        status = self.check_status(
            threshold=self.max_memory, current_value=current_memory)
        self.memory_stats[current_time] = (current_memory, status)
        message = Message.create(("memory_utilization",
                                  current_time,
                                  self.memory_stats))
        await self.queue.put(message)
                             

    async def check(self):
        """
        """
        memory_task = await curio.spawn(self.check_memory())
        cpu_task = await curio.spawn(self.check_cpu())

    def __repr__(self):
        try:
            return "Trap for {} {}".format(self.process.name(),
                                           self.state)
        except AttributeError:
            return "Unbound Trap"

    def __str__(self):
        try:
            return "Trap for {} {}".format(self.process.name(),
                                           self.state)
        except AttributeError:
            return "Unbound Trap"


class Proc(psutil.Process):
    """
    A subclass of :class:`psutil.Process`
    """

    @classmethod
    def _parent_walk(cls, current_proc):
        """
        recursive function to return the top parential proc
        NOTE: currently we are basing only on name of the process
        as such it may present issues with properly id' the parent
        possible solution - look at os module, or possible systemd
        but could get ugly with various systems. e.g. chrome,
        chrome-sandbox

        :param current_proc :class:`psutil.Process`: Process instance Process instance
        :return Proc.id: Process Id
        :rtype int:
        """
        parent = current_proc.parent()
        try:
            if current_proc.name() != parent.name():
                return current_proc.pid
        except AttributeError:
            # We've traveresed all the way to PID 1,
            # `process.parent()` returns None
            return current_proc.pid
        return cls._parent_walk(current_proc.parent())

    @classmethod
    def _is_match(cls, proc, properties):
        """
        True if all configured process properties match a process.
        we are checking if all fields provided
        match, the current proc.
        access each object's attr, via a 'string'

        :param :class:`psutil.Process` proc: the actual process, `psutil.Process`
        :param dict properties
        :return: boolean if all the property fields match the properties
        :rtype: bool
        """
        property_fields_match = [properties.get(field) == getattr(proc, field)()
                                 for field in properties.keys()]
        return all(property_fields_match)

    @classmethod
    def create_watch(cls, properties):
        """
        finds a process based on properties provided. Creates a Proc for
        the parent process.

        :param namedtuple properties: properies of the process to watch
        :return Proc:
        :rtype Proc:
        """
        for proc in psutil.process_iter():
            if cls._is_match(proc, properties):
                # return the parent of this process
                return cls(pid=cls._parent_walk(proc))

    def __unicode__(self):
        return '{}_{}'.format(self.pid(), self.name())

    def __init__(self, pid=None):
        super().__init__(pid=pid)


class Message(object):
    """
    generates message obj.

    :param dict data: data for message.
    """
    @staticmethod
    def create(data):
        """factory for creating an object"""
        sender = data[0]
        timestamp = data[1]
        result_data = data[2]
        return BaseMessage(result_data, sender, timestamp)


class BaseMessage(object):
    """
    Represents a message.

    :param data:
    :param sender:
    .. py:attribute:: _initial message obj before encode, internal use
    """

    _initial = {}

    def __init__(self, data=None, sender=None, timestamp=None):
        self.is_valid(data=data, sender=sender)
        self.timestamp = timestamp
        self._initial.update({'create_timestamp': self.create_timestamp(),
                              "data": data,
                              "sender": sender})

    def is_valid(self, data=None, sender=None):
        """
        checks for a valid message, sets .initial

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
        """
        creation timestamp, utc

        :return: arrow.utcnow()
        :rtype: object
        """
        return arrow.utcnow().isoformat(sep="T")

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "Message: {}, {}".format(self.timestamp, self.data)
   
    def encode(self):
        """JSON encodes .initial

        :returns: json.dump
        :rtype: bytes
        """
        return json.dumps(self._initial)
