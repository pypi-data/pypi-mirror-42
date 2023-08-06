from __future__ import absolute_import
from future.moves.collections import MutableSequence
from lxml import etree
from tempest_zigzag.tempest_testcase_xml import TempestTestcaseXml


class TempestJunitXMLSuite(MutableSequence):
    """maps directly to an XML suite
    Can create an xml string
    """

    def __init__(self, path):
        """Create a new TempestJunitSuite

        Args:
            path: (str) the path to the file to be read
        """
        # read the xml
        junit_xml_doc = etree.parse(path)
        self._initial_junit_xml = junit_xml_doc.getroot()
        # read the testcases from the xml
        self._test_list = [TempestTestcaseXml(element) for element in self._initial_junit_xml.findall('testcase')]
        self._properties = {}

    def remove_tests_without_idempotent_ids(self):
        """Removes any test cases that do not have the idempotent_id property

        Returns:
            a list of the test cases removed
        """
        new_list = []
        tests_to_return = []

        for test in self._test_list:
            if not test.idempotent_id:
                tests_to_return.append(test)
            else:
                new_list.append(test)

        self._test_list = new_list

        return tests_to_return

    def find_tests_by_classname(self, classname):
        """Gets a list of tests that match a classname

        Args:
            classname: (str) the classname of the tests

        Returns:
            list: a list of TempestTestcaseXml
        """
        return [test for test in self._test_list if test.classname == classname]

    @property
    def _xml_error_count(self):
        """The total number of tests with errors

        Returns:
            int: the number of tests with errors in this sequence
        """
        return len([test for test in self._test_list if test.xml_error_elements])

    @property
    def _xml_failure_count(self):
        """The total number of tests with failures

        Returns:
            int: the number of tests with failures in this sequence
        """
        return len([test for test in self._test_list if test.xml_failure_elements])

    @property
    def _xml_total_time(self):
        """The total time of all the tests contained in this sequence

        Returns:
            float: the total execution time
        """
        return sum([float(test.time) for test in self._test_list])

    @property
    def _xml_total_test_count(self):
        """The total number of tests contained in this sequence

        Returns:
            int: the number of tests in this sequence
        """
        return len(self._test_list)

    @property
    def xml(self):
        """Generate the xml based on the contents of this sequence

        Returns:
            str: the xml string based on the state of this object
        """
        # a dict key = name in xml, value = value if there is one
        d = {
            'errors': self._xml_error_count,
            'failures': self._xml_failure_count,
            'name': 'xml suite created by tempest-zigzag',
            'tests': self._xml_total_test_count,
            'time': self._xml_total_time,
        }

        # build an etree element
        xml = etree.Element('testsuite')
        xml.append(self.properties)

        for xml_attrib_name, value in list(d.items()):
            if value is not None:  # only add attribute if there is a value for it
                xml.attrib[xml_attrib_name] = str(value)

        # read all elements from this sequence and add as child elements
        for test in self._test_list:
            xml.append(test.xml_element)

        xml_string = etree.tostring(xml)

        if type(xml_string) is bytes:  # not sure why this is sometime a bytes and sometimes a string
            return xml_string.decode('UTF-8')
        else:
            return xml_string

    @property
    def properties(self):
        """The xml properties element"""
        properties = etree.Element('properties')
        for k, v in list(self._properties.items()):
            prop = etree.Element('property')
            prop.attrib['name'] = k
            prop.attrib['value'] = v if v else ''  # if a value is not truthy set it to emptystring
            properties.append(prop)

        return properties

    @properties.setter
    def properties(self, value):
        """Sets the _properties dict"""
        self._properties = value

    def __getitem__(self, key):
        """MutableSequence ABC override."""

        return self._test_list.__getitem__(key)

    def __setitem__(self, key, value):
        """MutableSequence ABC override."""

        return self._test_list.__setitem__(key, value)

    def insert(self, index, value):
        """MutableSequence ABC override."""

        return self._test_list.insert(index, value)

    def __delitem__(self, index):
        """MutableSequence ABC override."""

        return self._test_list.__delitem__(index)

    def __len__(self):
        """MutableSequence ABC override."""

        return len(self._test_list)
