import unittest
import unittest.mock as mock
import datetime
from collections import namedtuple
from traps.models import Proc


class ProcTestCase(unittest.TestCase):
    """tests for traps"""

    @mock.patch('psutil.Process', autopect=True)
    @mock.patch('psutil.Process', autopect=True)
    def setUpMocks(self, mock_proc, mock_proc_2):
        base_name = 'mock_proc_%s'
        for index, item in enumerate(self.test_props):
            base_name = "mock_proc_%s" % (index)
            self.base_name = mock.create_autospec("psutil.Process")
            self.base_name.key = mock.MagicMock(return_value=value)
            self.base_name.parent = mock.MagicMock(return_value=item["parent"])
            self.base_name.pid = mock.MagicMock(return_value=index)

    def setUp(self, *args, **kwargs):
        print(self.shortDescription())
        self.test_props = [{"name": "eee",
                            "parent": None},
                           {"name": "eee",
                            "parent": 0},]

    def test_should_find_a_proc_base_case(self):
        """should find a process with a name `xyz` no parent"""
        proc_id = Proc._parent_walk(self.mock_proc)
        self.assertEqual(55, proc_id())

    def test_parent_walk(self):
        """test_base_case"""
        self.mock_proc = mock.MagicMock(return_value=self.mock_proc_2)
        self.mock_proc_2.name = mock.MagicMock(return_value="eee")
        proc = Proc._parent_walk(self.mock_proc)
        self.assertEqual(self.test_prop['name'], proc.name())
