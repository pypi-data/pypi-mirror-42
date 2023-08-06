from unittest import TestCase

from test.test_packages.testerforpolyfactory import TesterForPolyFactory


class TestPolyFactory(TestCase):

    def setUp(self):
        self.pf = TesterForPolyFactory

    def tearDown(self):
        del self.pf
        pass

    def test_find_factories(self):
        """
        Test the ability to find factory methods.
        """

        self.pf.discover_class_factories()
        print(self.pf.create(object_id='test.test_packages.TestMixin.MM').__class__)

    def test_find_python_modules(self):
        """
        Test the ability to identify python modules
        """
        pass

    def test_create(self):
        """
        Test the creation of a class given its identifier.
        """
        pass

    def test_create_DNE(self):
        """
        Test raising an exception when creating a registered method the does not exist (DNE).
        """
        pass

