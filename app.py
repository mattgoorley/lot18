import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from validators import Validators
import json


UPLOAD_FOLDER = 'files/' #uploads to this directory
ALLOWED_EXTENSIONS = set(['csv']) #only allows csv files to be uploaded
STATIC_FOLDER = 'static/'
# DATABASE = 'files/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/order.db'
db = SQLAlchemy(app)


def allowed_file(filename):
  ''' Checks filename of file import and only takes the allowed extension'''
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/') #index page
def index():
  return render_template('index.html')

@app.route('/import/')
@app.route('/import', methods=['GET','POST'])

def importcsv():
  ''' imports the csv '''
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      data = {
        'message':'No file part',
        'error':'Loading Error'
        }
      return render_template('upload.html', data=data)

    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
      data = {
      'message':'No selected file',
      'error':'Loading Error'
      }
      return render_template('upload.html', data=data)

    if file and not allowed_file(file.filename):
    # if user uploads an incorrect file type,
    # browser notifies incorrect file type
      data = {
      'message':'Incorrect file type',
      'error':'Loading Error'
      }
      return render_template('upload.html', data=data)

    if file and allowed_file(file.filename):
    # if user uploads correctly
      outfile = file_saver(file)
      filename = outfile.name
      return redirect(url_for('all_orders'))
  else:
    data = {'message':'','error':''}
    return render_template('upload.html', data=data)

@app.route('/orders/')
@app.route('/orders', methods=['GET', 'POST'])

def all_orders():
  ''' Returns all orders on the orders page. Allows for filtering '''
  try:
    valid = request.args.get('valid') or None
    state = request.args.get('state') or None
    zipcode = request.args.get('zipcode') or None

    order = Orders.query.all()

    if valid: #filter by validity
      order = Orders.query.filter_by(valid=valid)

    if state: #filter by state
      order = Orders.query.filter_by(state=state)

    if zipcode: #filter by zipcode
      order = Orders.query.filter_by(zipcode=zipcode)


    data = []
    for o in order:
      d = {
        'id': o.order_id,
        'name': o.name,
        'state': o.state,
        'email': o.email,
        'zipcode': o.zipcode,
        'birthday': o.birthday,
        'valid': o.valid,
        'errors': o.errors
      }

      data.append(d)
    return render_template('results.html', data=data)
  except:
    # redirects to import if function cannot run
    return redirect(url_for('importcsv'))

@app.route('/orders/<order_id>', methods=['GET'])
def see_order_id(order_id):
  ''' Sends one order's information '''
  try:
    order = Orders.query.filter_by(order_id=order_id).first()
    data = {
      'id': order.order_id,
      'name': order.name,
      'email': order.email,
      'state': order.state,
      'zipcode': order.zipcode,
      'birthday': order.birthday,
      'valid': order.valid,
      'errors': order.errors
    }
    return render_template('order.html', data=data)

  except:
    # redirects to all orders if try fails
    return redirect(url_for('all_orders'))




def file_exists(filename):
  ''' Renames file if it already exists in directory '''
  if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
    filename = file_exists(filename.rsplit('.', 1)[0] + "1." + filename.rsplit('.', 1)[1])

  return filename

def file_saver(file):
  '''
    Saves uploaded file as a json file, in a SQL database, and creates a
    pandas dataframe to run validation test
  '''
  # check filename uniqueness
  filename = file_exists(file.filename)

  # saves original uploaded file to files directory
  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

  #creates pandas dataframe from the csv file
  df = pd.read_csv('files/' + filename, sep='|')

  # run validation rules
  validate = Validators(df=df)
  data = validate.clean_orders()

  #create a dictionary from pandas dataframe
  d = [
    dict([
        (colname, row[i])
        for i,colname in enumerate(data.columns)
    ])
    for row in data.values
    ]

  # seeds database with order information
  Orders.query.delete()
  for order_row in d:
    order_id = order_row['id']
    name = order_row['name']
    state = order_row['state']
    email = order_row['email']
    zipcode = order_row['zipcode']
    birthday = order_row['birthday']
    valid = str(order_row['valid'])
    errors = str(order_row['errors'])
    save_order = Orders(order_id=order_id, name=name, state=state, email=email, zipcode=zipcode, birthday=birthday, valid=valid, errors=errors)
    db.session.add(save_order)
  db.session.commit()

  # create json file
  with open('files/' + filename.rsplit('.', 1)[0]  + '.json', 'w') as outfile:
    json.dump(d, outfile)
  return outfile


class Orders(db.Model):
  ''' Model for Orders database '''
  __tablename__ = 'orders'
  pk = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, primary_key=False)
  name = db.Column(db.String, nullable=False)
  state = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  zipcode = db.Column(db.String, nullable=False)
  birthday = db.Column(db.String, nullable=False)
  valid = db.Column(db.String, nullable=False)
  errors = db.Column(db.String, nullable=False)



if __name__ == "__main__":
    app.run(debug=True)
