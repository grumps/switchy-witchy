#-*- coding: utf-8 -*-
"""Traps capture varying events within the system"""
__author__ = "Maxwell J. Resnick"
__docformat__ = "reStructuredText"

import collections
import json

import psutil
import curio
import arrow


class BaseState(object):
    """
    base class for all state objects
    """

    @classmethod
    def next(cls, results=None):
        """Validates right to transition

        :param current_state:if none, we are to transition
        :returns: cls, either `Starting` or its current_state
        :rtype: cls
        """
        # we should start
        if results is cls.NAME: 
            return cls
        return cls.NEXT_STATE

class Running(BaseState):
    pass


class Failing(BaseState):
    """
    failed state
    """
    pass


class Passing(BaseState):
    """
    failed state
    """
    pass


class Starting(BaseState):
    """Starting state"""

    NEXT_STATE = Running
    NAME = "Starting"

    async def action(self):
        """
        Sets up process.
        Sets up transition
        """
        print("running action on start state")
        self.process = Proc.create_watch(self.properties)
        await self.queue.put("RUNNING",)


class StateMachineMixin(object):
    """
    base class for all statemine obj.
    """
    STATES = {
        "STARTING": Starting,
        "FAIL": Failing,
        "RUNNING": Running,
        "PASS": Passing
    }

    def __init__(self):
        self.state = self.STATES["STARTING"]()
    async def next(self, results):
        """shortcut to state's next"""
        return self.state.next(results)

    async def action(self):
        """shortcut to state's action"""
        await self.state.action()

    async def transition(self):
        """
        background task that consumes queue to determine state
        """
        while True:
            sender, time_stamp, results = await self.queue.get()
            result_state = results[time_stamp]
            self.state = self.next(results)
            if self.state:
                await self.action()
                print('Consumer got', )
