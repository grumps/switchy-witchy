#-*- coding: utf-8 -*- # noqa: E265
__docformat__ = "reStructuredText"
import unittest
import unittest.mock as mock

import curio

from switchywitchy import machines, models


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
        self.state_obj.queue = curio.Queue()

    def test_setup_init_state_sets(self):
        """state attribute is set to starting type"""
        expected_state = machines.StateMachineMixin.STATE_TABLE["STARTING"]
        self.assertIsInstance(self.state_obj.state, expected_state)
    @unittest.skip("wip")
    def test_consumer_calls_next(self):
        """statemachine consumer should call next transition"""
        self.state_obj.next = mock.Mock(return_value=None)
        # TODO this needs to be tuple like obj
        test_message = mock.MagicMock(models.Message, autospec=True)
        async def main():
            try:
                await curio.spawn(self.state_obj.queue.put(test_message)) 
                await curio.timeout_after(.5, self.state_obj.transition())
            except curio.TaskTimeout as e:
                pass
        curio.run(main())
        self.state_obj.next.assert_called_with(results=test_message)
