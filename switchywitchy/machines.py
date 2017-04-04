#-*- coding: utf-8 -*-
"""Traps capture varying events within the system"""
__author__ = "Maxwell J. Resnick"
__docformat__ = "reStructuredText"


class BaseState(object):
    """
    base class for all state objects
    """

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
    pass


class Passing(BaseState):
    """
    failed state
    """
    NAME = "PASSING"
    #NEXT_STATE = ()


class Running(BaseState):

    NAME = "RUNNING"
    NEXT_STATE = (Passing, Failing)


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
        self.process = Proc.create_watch(self.properties)
        await self.queue.put("RUNNING",)

state_entry = NamedTuple("State", ["output_states", "state_class"])


class StateMachineMixin(object):
    """
    base class for all statemine obj.
    """

    STATE_TABLE = {
        "STARTING": state_entry((Running,), Starting),
        "FAILING": state_entry((Passing,), Failing),
        "RUNNING": state_entry((Passing, Failing), Running),
        "PASSING": state_entry((Running,), Passing),
    }

    def __init__(self):
        self.setup_init_state()

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
        self.state = start()

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
