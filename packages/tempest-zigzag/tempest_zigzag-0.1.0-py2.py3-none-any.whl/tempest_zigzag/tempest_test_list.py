from __future__ import absolute_import
from future.moves.collections import Sequence
from tempest_zigzag.tempest_testcase_list import TempestTestcaseList


class TempestTestList(Sequence):

    def __init__(self, path):
        """Create TempestTestList

        Args:
            path: (str) the path to the file to read
        """

        self._test_list = []

        with open(path) as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    self._test_list.append(TempestTestcaseList(line))

    def find_tests_by_classname(self, classname):
        """Find all the tests that have the same class name

        Args:
            classname: (str) the classname of a test

        Returns:
            list: the tests with the specified classname
        """

        return [test for test in self._test_list if test.classname == classname]

    def __getitem__(self, key):
        """Sequence ABC override."""

        return self._test_list.__getitem__(key)

    def __iter__(self):
        """Sequence ABC override."""

        return iter(self._test_list)

    def __len__(self):
        """Sequence ABC override."""

        return len(self._test_list)
