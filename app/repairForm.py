import sqlite3
from pprint import pprint
from datetime import datetime


db_path = 'app\carDNA.db'

# insert new form
def insert_new_form(form_inputs):  
    try:
      conn = sqlite3.connect(db_path)
      cur = conn.cursor()
      # TODO: 1) begin transaction -> 2) insert person info -> 3) insert car info (foreign per_id) -> 4) insert repair info (foreign car_id) -> 5) insert 6) car_parts (foreign rep_id) -> 7) insert workshop_repairs_repairment (foreign wp_id, rep_id) -> 8) commit transaction
      # (4) to (7) in another single func. to be used in Add Repairement

    except Exception as ex:
      return ex
    return True

# check if VIN is already registered
# return car_id, else false
def registered_car_vin(car_vin):
      query= "SELECT car_id FROM Car WHERE car_vin = ?"
      try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query, [car_vin])
        result = cur.fetchall()
        if len(result) >= 1:
          return result[0][0]
        else:
          return False
      except Exception as ex:
        return ex

# check if nation id is already registered
# return per_id, else false
def registered_person(nationID):
      query= "SELECT per_id FROM Person WHERE per_nation_id = ?"
      try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query, [nationID])
        result = cur.fetchall()
        if len(result) >= 1:
          return result[0][0]
        else:
          return False
      except Exception as ex:
        return ex


# check if permission id is already registered
def registered_rep_permission_paper_id(rep_permission_paper_id):
      query= "SELECT rep_id FROM Repairment WHERE rep_permission_paper_id = ?"
      return check_registered(query, rep_permission_paper_id)

# check if car_since_date > current date
def car_since_date_bigger_current(car_since_date):
  current_year = datetime.today().year
  if (int(car_since_date) > current_year):
    return True
  else:
    return False

# check if car_since_date < car_year
def car_since_date_older_car_year(car_since_date, car_year):
  if (int(car_since_date) < int(car_year)):
    return True
  else:
    return False

# check if car_year > current date
def car_year_bigger_current(car_year):
  current_year = datetime.today().year
  if (int(car_year) > current_year):
    return True
  else:
    return False

# check if dob > current date
def dob_bigger_current(dob):
  current_year = datetime.today().year
  dob = dob.strftime("%Y")
  if (int(dob) > current_year):
    return True
  else:
    return False

# check if rep_date > current date
def rep_date_bigger_current(rep_date):
  current_year = datetime.today().year
  rep_date = rep_date.strftime("%Y")
  if (int(rep_date) > current_year):
    return True
  else:
    return False

# check if rep_date < car_since_date
def rep_date_older_car_since_date(rep_date, car_since_date):
  rep_date = rep_date.strftime("%Y")
  if (int(rep_date) < int(car_since_date)):
    return True
  else:
    return False

def check_registered(query, param):
    try:
      conn = sqlite3.connect(db_path)
      cur = conn.cursor()
      cur.execute(query, [param])
      result = cur.fetchall()
      if len(result) >= 1:
        return True
      else:
        return False
    except Exception as ex:
      return ex

