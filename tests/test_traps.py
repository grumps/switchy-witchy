"""tests for traps package"""

import unittest
import unittest.mock as mock
from switchywitchy.traps.models import Proc, Trap
from switchywitchy import SwitchyWitchy


class ProcTestCase(unittest.TestCase):
    """tests for Proc"""

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
        # janky but used because CI runs onder a different process
        import psutil
        p = psutil.Process()
        expected_name = p.name()
        self.assertIsInstance(Proc.create_watch({"name": expected_name}), Proc)

class TrapTestCase(unittest.TestCase):
    """test for traps"""

    def setUp(self):
        print(self.shortDescription())

    def test_handle_properties_returns_dict(self):
        """tests that handle_properties returns a dict"""
        p = {"process_name":"stuff"}
        s = Trap(p)
        self.assertIsInstance(s.handle_properties(p), dict)

    def test_handle_properties_sets_watch_attr(self):
        """when given a key with a prefix of `watch` attr on `Trap`"""
        p = {"watch_max_cpu_usage":"55",
             "watch_max_memory":"60"}
        s = Trap(p)
        self.assertEqual(s.max_cpu_usage, "55")
        self.assertEqual(s.max_memory, "60")

    def test_handle_properties_returns_proc_props(self):
        """when given a key with a prefix of `process` be in a prop on `Trap`"""
        p = {"process_name":"test_python",
             "watch_max_cpu_usage":"55"}
        s = Trap(p)
        self.assertDictEqual(s.properties, {"name":"test_python"})
        self.assertEqual(s.max_cpu_usage, "55")
