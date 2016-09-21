import pandas as pd
from datetime import date
from dateutil import parser
from validate_email import validate_email
import re

class Validators():
  '''
    Validators uses a pandas dataframe to apply validation methods to see
    if each order is valid or invalid.

  '''
  def __init__(self, df):
    self.df = df
    # bad_states are the states that cannot accept shipped wine
    self.bad_states = ('NJ', 'CT', 'PA', 'MA', 'IL', 'ID', 'OR')


  def clean_orders(self):
    '''
      Applies validation rules to each order and adds error messages
      and validity columns to the order dataframe.
      Returns the new dataframe
    '''
    self.df['errors'] = self.df.apply(self._validate_errors,axis=1)
    self.df['valid'] = self.df.apply(self._validate,axis=1)

    return self.df

  def _validate_errors(self, row):
    '''
      Takes a dataframe row as the argument and applies validation methods
      to each row. Returns a list of errors if they exist,
      or None if they do not.

      This is where all validation methods are to be run.
    '''
    errors = []

    error1 = self._state_validate(row)
    if error1 is not None:
      errors.append(error1)

    error2 = self._zip_validate(row)
    if error2 is not None:
      errors.append(error2)

    error3 = self._age_validate(row)
    if error3 is not None:
      errors.append(error3)

    error4 = self._email_validate(row)
    if error4 is not None:
      errors.append(error4)

    error6 = self.__ny_net_combo_validate(row)
    if error6 is not None:
      errors.append(error6)

    if not errors:
      errors = None

    return errors

  def _validate(self, row):
    '''
      Takes a dataframe row as the argument and checks to see if there are
      errors. Returns True or False depending on if error exists.
    '''
    if row['errors']:
      return False
    else:
      return True

  def _state_validate(self, row): # validate against state

    if row['state'] not in self.bad_states:
      return None
    else:
      return {"rule": "AllowedStates", "message": "We don't ship to {}".format(row['state'])}

  def _zip_validate(self, row): # validate against zipcode
    '''
      Will return only one error for zip code problems. Checks the proper
      formatting of the zipcode first, and if okay then checks the sum.

      Returns only one error based on zip code
    '''
    zip_matcher = re.match(r"^[0-9]{5}(?:-[0-9]{4})?$", row['zipcode'])
    if zip_matcher:
      summed = sum(int(x) for x in zip_matcher.string[0:5])
      if summed <= 20:
        return None
      else:
        return {"rule": "ZipCodeSum", "message": "Your zipcode sum is too large"}
    else:
      return {"rule": "ZipCodeLength", "message": "Your zipcode must be 5 or 9 digits"}

  def _age_validate(self, row): #validate against age
    birthday = parser.parse(row['birthday'])
    # call __calculate_age to get age
    age = self.__calculate_age(birthday)
    if age > 21:
      return None
    else:
      return {"rule": "Under21", "message": "You must be over 21 to order"}

  def __calculate_age(self, born): #calculates age for __age_validate method
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

  def _email_validate(self, row): #validate against email address
    is_valid = validate_email(row['email'])
    if is_valid == True:
      return None
    else:
      return {"rule": "InvalidEmail", "message": "This email address is invalid"}

  def __ny_net_combo_validate(self, row): #validate against NY email .net address
    if row['state'] == 'NY' and row['email'].endswith('.net'):
      return {"rule": "EmailNYnet", "message": "New York email addresses cannot be .net domains"}
    else:
      return None





