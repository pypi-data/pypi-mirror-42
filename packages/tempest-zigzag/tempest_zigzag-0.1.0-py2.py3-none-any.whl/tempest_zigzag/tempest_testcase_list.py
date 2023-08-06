from __future__ import absolute_import
import re
from lxml import etree
from datetime import datetime
from datetime import timedelta


class TempestTestcaseList(object):

    _FULL_CLASSNAME = re.compile(r'^(\w|\.)*')
    _TEST_PARAMETERS = re.compile(r'\[(.*)\]')
    _TEMPEST_UUID_RGX = re.compile(r'(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)')
    _date_time_format = '%Y-%m-%dT%H:%M:%SZ'  # the highest degree of accuracy that qtest will accept (no micro seconds)

    def __init__(self, test_entry_string):
        """Creates a new Tempest Test Execution

        Args:
            test_entry_string: (str) A single line from 'tempest run --list-tests'
        """
        self._test_entry_string = test_entry_string.strip()
        self._xml_element = None
        self._time = '0.00'
        self._date_time_now = datetime.utcnow()  # use same time for all operations

    @property
    def xml_element(self):
        """Produces xml in the format produced by tempest
        property is a caching property

        Returns:
            etree.Element : an xml testcase element
        """

        if self._xml_element is None:
            # a dict key = name in xml, value = value if there is one
            d = {
                'name': self._xml_name,
                'classname': self.classname,
                'time': self.time
            }

            # build an etree element
            xml = etree.Element('testcase')
            for xml_attrib_name, value in list(d.items()):
                if value:  # only add attribute if there is a value for it
                    xml.attrib[xml_attrib_name] = value

            properties = etree.Element('properties')
            properties.append(etree.Element('property', {'name': 'start_time', 'value': self.start_time}))
            properties.append(etree.Element('property', {'name': 'end_time', 'value': self.end_time}))
            properties.append(etree.Element('property', {'name': 'test_id', 'value': self.idempotent_id}))
            properties.append(etree.Element('property', {'name': 'test_step', 'value': 'false'}))

            xml.append(properties)
            self._xml_element = xml

        return self._xml_element

    @property
    def start_time(self):
        """Gets the start time

        Returns:
            str: the end date of this test execution
        """
        return self._date_time_now.strftime(self._date_time_format)

    @property
    def end_time(self):
        """Gets the end time

        Returns:
            str: the end date of this test execution
        """

        start = datetime.strptime(self.start_time, self._date_time_format)
        # if time is a fraction of a second round up to one second
        time = 1 if float(self.time) < 1 else self.time
        duration = timedelta(seconds=float(time))
        end = start + duration
        return end.strftime(self._date_time_format)

    @property
    def _xml_name(self):
        """The name as it appears in the XML
        not to be confused with name which is the name of the test

        Returns:
            str: the value for name as it would appear in tempest xml
        """
        params = list(self.test_tags)
        params.insert(0, "id-{}".format(self.idempotent_id))
        params = ','.join(params)

        return "{name}[{params}]".format(name=self.name, params=params)

    @property
    def name(self):
        """The name

        Returns:
            str: The name of the test
            None
        """
        try:
            return self._FULL_CLASSNAME.match(self._test_entry_string).group(0).split('.')[-1]
        except AttributeError:
            return None

    @property
    def classname(self):
        """The classname

        Returns:
            str: The classname of the test
            None
        """

        try:
            return '.'.join(self._FULL_CLASSNAME.match(self._test_entry_string).group(0).split('.')[:-1])
        except AttributeError:
            return None

    @property
    def idempotent_id(self):
        """The idempotent ID

        Returns:
            str: The UUID of the test
            None
        """

        try:
            return self._TEMPEST_UUID_RGX.search(self._test_entry_string).group(0)
        except AttributeError:
            return None

    @property
    def time(self):
        """The elapsed time of the test case

        Returns:
            str: the time in string format
        """
        return self._time

    @time.setter
    def time(self, value):
        """Sets the time property

        Args:
            value: (str) the time in a string
        """
        self._time = value

    @property
    def test_tags(self):
        """The tags associated with this test

        Returns:
            list: A list of strings
            None
        """

        try:
            params = self._TEST_PARAMETERS.search(self._test_entry_string).group(1).split(',')
            return [param for param in params if self._TEMPEST_UUID_RGX.search(param) is None]
        except AttributeError:
            return None

    @property
    def xml_failure_elements(self):
        """The xml child elements with the tag failure

        Returns:
            list: list of failure elements
        """
        return self.xml_element.findall('failure')

    @property
    def xml_error_elements(self):
        """The xml child elements with the tag error

        Returns:
            list: list of error elements
        """
        return self.xml_element.findall('error')
