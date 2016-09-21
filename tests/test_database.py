import unittest
from my_module import MyClass

class TestDatabase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_something(self):
        my_thing = MyClass()
        result = my_thing.my_method("words!")
        self.assertTrue(result, True)

    def test_something_else(self):
        my_thing = MyClass()
        assertNotEqual(my_thing('a'), my_thing('b'))
