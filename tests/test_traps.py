"""tests for traps package"""

import unittest
import unittest.mock as mock
from switchywitchy.traps.models import Proc


class ProcTestCase(unittest.TestCase):
    """tests for traps"""

    @mock.patch("psutil.Process", autospec=True)
    def create_mock(self, properties, mocked):
        """sets up mocks for tests"""
        for key, value in properties.items():
            setattr(mocked,
                    key,
                    mock.MagicMock(return_value=value))
        return mocked

    def setUp(self):
        print(self.shortDescription())
        self.mocks = []
        self.test_props = [{"name": "e2ee",
                            "parent": None,
                            "pid": 44},
                           {"name": "eee",
                            "parent": 0,
                            "pid": 55},]

    def test_returns_a_proc_without_parent(self):
        """If there's no parent, it should return the initial proc"""
        self.test_props[1]["parent"] = self.create_mock(self.test_props[0])
        mock_proc = self.create_mock(self.test_props[1])
        proc_id = Proc._parent_walk(mock_proc)
        self.assertEqual(55, proc_id())

    def test_returns_a_procs_parent(self):
        """if the process has a parent, it should return the parent"""
        self.test_props.append(dict(self.test_props[1]))
        self.test_props[2]["pid"] = 54
        self.test_props[1]["parent"] = self.create_mock(self.test_props[0])
        self.test_props[2]["parent"] = self.create_mock(self.test_props[1])
        mock_proc = self.create_mock(self.test_props[2])
        proc = Proc._parent_walk(mock_proc)
        self.assertEqual(55, proc())
    
    def test_create_watch_returns_a_proc_class(self):
        """create_watch returns an instance of a process"""
        self.assertIsInstance(Proc.create_watch({"name": "python"}), Proc)
