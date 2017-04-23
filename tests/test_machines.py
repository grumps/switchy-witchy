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

import unittest
import unittest.mock as mock

from switchywitchy import machines


class TestStateMachine(machines.StateMachineMixin):

    def __init__(self):
        self.setup_init_state()


class TestStateMachineMixin(unittest.TestCase):
    """tests for StateMachineMixin"""

    @classmethod
    def setUpClass(cls):
        cls.state_cls = TestStateMachine

    def setUp(self):
        print(self.shortDescription())
        self.state_obj = self.state_cls()

    def test_setup_init_state_sets(self):
        """state attribute is set to starting type"""
        expected_state = machines.StateMachineMixin.STATE_TABLE["STARTING"]
        self.assertIsInstance(self.state_obj.state, expected_state)
