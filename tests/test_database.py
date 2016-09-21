import unittest
from validators import Validators
import pandas as pd

class TestValidators(unittest.TestCase):
    ''' Tests for "validators.py" '''

    def setUp(self):
        self.df = pd.DataFrame({
            'id' : ["1000", "1001", "Seven"],
            'name' : ["Test Name", "Name Test", "Test Test"],
            'email' : ["matt@gmail.com", "tom@gmail.net", "mike@topdog.co"],
            'state' : ["LA", "NY", "IL"],
            'zipcode' : ["99999", "10128", "71106"],
            'birthday' : ["Mar 12, 1985", "May 12, 1895", "June 19, 1999"],
            'test_extra' : ["test_extra", 7, False]
        })

    def tearDown(self):
        del self.df


    def test_validate_errors(self):
        validator = Validators(self.df)
        result = validator._validate_errors(self.df.loc[2])
        if result:
            self.assertIs(type(result), list)
        else:
            valid = validator_validate(self.df.loc[2])
            self.assertTrue(valid)

    def test_state_validate(self):
        validator = Validators(self.df)
        result = validator._state_validate(self.df.loc[0])
        if result:
            self.assertIs(type(result), dict)
        else:
            self.assertIsNone(result)

    def test_age_validate(self):
        validator = Validators(self.df)
        result = validator._age_validate(self.df.loc[1])
        if result:
            self.assertIs(type(result), dict)
        else:
            self.assertIsNone(result)

    def test_email_validate(self):
        validator = Validators(self.df)
        result = validator._email_validate(self.df.loc[0])
        if result:
            self.assertIs(type(result), dict)
        else:
            self.assertIsNone(result)


