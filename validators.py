import pandas as pd
from datetime import date
from dateutil import parser
from validate_email import validate_email
import re

class Validators():
  def __init__(self, df):
    self.df = df
    self.bad_states = ('NJ', 'CT', 'PA', 'MA', 'IL', 'ID', 'OR')


  def clean_orders(self):
    self.df['errors'] = self.df.apply(self._validate_errors,axis=1)
    self.df['valid'] = self.df.apply(self._validate,axis=1)

    return self.df

  def _validate_errors(self, row):
    errors = []

    error1 = self.state_validate(row)
    if error1 is not None:
      errors.append(error1)

    error2 = self.zip_validate(row)
    if error2 is not None:
      errors.append(error2)

    error3 = self.age_validate(row)
    if error3 is not None:
      errors.append(error3)

    error4 = self.email_validate(row)
    if error4 is not None:
      errors.append(error4)

    error6 = self.ny_net_combo_validate(row)
    if error6 is not None:
      errors.append(error6)

    if not errors:
      errors = None

    return errors

  def _validate(self, row):
    if row['errors'] == None:
      return True
    else:
      return False


  def state_validate(self, row):
    # validate against state
    if row['state'] not in self.bad_states:
      return None
    else:
      return {"rule": "AllowedStates", "message": "We don't ship to {}".format(row['state'])}

    # validate against zipcode

  def zip_validate(self, row):
    zip_matcher = re.match(r"^[0-9]{5}(?:-[0-9]{4})?$", row['zipcode'])
    if zip_matcher:
      summed = sum(int(x) for x in zip_matcher.string[0:5])
      if summed <= 20:
        return None
      else:
        return {"rule": "ZipCodeSum", "message": "Your zipcode sum is too large"}
    else:
      return {"rule": "ZipCodeLength", "message": "Your zipcode must be 5 or 9 digits"}




    #validate against age
  def age_validate(self, row):
    birthday = parser.parse(row['birthday'])
    age = self._calculate_age(birthday)
    if age > 21:
      return None
    else:
      return {"rule": "Under21", "message": "You must be over 21 to order"}

  def _calculate_age(self, born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


    #validate against email address
  def email_validate(self, row):
    is_valid = validate_email(row['email'])
    if is_valid == True:
      return None
    else:
      return {"rule": "InvalidEmail", "message": "This email address is invalid"}

    #validate against NY email .net address
  def ny_net_combo_validate(self, row):
    if row['state'] == 'NY' and row['email'].endswith('.net'):
      return {"rule": "EmailNYnet", "message": "New York email addresses cannot be .net domains"}
    else:
      return None





