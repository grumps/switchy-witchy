#-*- coding: utf-8 -*- # noqa: E265

"""
Machines are finite state machines and the various states that a machince can
achieve.

The transitions defined by a "transition table" which is dictionary with a
namedtuple as the value

    ```
    {"foo": namedtuple()}
    ```

Each state class takes a reference to the state table on contstruction

"""
__author__ = "Maxwell J. Resnick"
__docformat__ = "reStructuredText"

import collections


class BaseState(object):
    """
    base class for all state objects
    """

    def __init__(self, state_table=None):
        self.sate_table = state_table

    @classmethod
    def next(cls, results=None):
        """
        Validates right to transition

        :param current_state:if none, we are to transition
        :returns: cls, either `Starting` or its current_state
        :rtype: cls

        """
        # we should start
        if results is cls.NAME:
            return cls
        return cls.NEXT_STATE


class Failing(BaseState):
    """
    failed state
    """
    NAME = "FAILING"


class Passing(BaseState):
    """
    failed state
    """
    NAME = "PASSING"


class Running(BaseState):
    """Running state"""
    NAME = "RUNNING"


class Starting(BaseState):
    """Starting state"""

    NEXT_STATE = (Running,)
    NAME = "STARTING"

    async def action(self):
        """
        Sets up process.
        Sets up transition
        """
        print("running action on start state")
        if not self.process:
            # TODO error message fmt
            await self.queue.put("FAILING", )
        await self.queue.put("RUNNING",)


class StateMachineMixin(object):
    """
    base class for all statemachine objects.
    """
    STATE_ENTRY = collections.namedtuple(
        "state", ["output_states", "state_class"])
    STATE_TABLE = {
        "STARTING": STATE_ENTRY((Running,), Starting),
        "FAILING": STATE_ENTRY((Passing,), Failing),
        "RUNNING": STATE_ENTRY((Passing, Failing), Running),
        "PASSING": STATE_ENTRY((Running,), Passing),
    }

    def __getattr__(self, name):
        """
        automatically forwards to the state class.
        """
        attr = getattr(self.state, name)
        if attr:
            return attr
        else:
            raise AttributeError

    def setup_init_state(self):
        """
        sets the initial state.
        """
        start_state_entry = self.STATE_TABLE["STARTING"]
        start = start_state_entry.state_class(
            start_state_entry.output_states)
        self.state = start

    async def transition(self):
        """
        background task that consumes queue to determine state
        """

        while True:
            sender, time_stamp, results = await self.queue.get()
            # result_state = results[time_stamp]
            self.state = self.next(results, )
            if self.state:
                await self.action()
                print('Consumer got', )
