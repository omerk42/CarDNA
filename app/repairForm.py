import sqlite3
from pprint import pprint
from datetime import datetime

from flask import session


db_path = 'app\carDNA.db'

# insert new form
def insert_new_form(form_inputs):  
      conn = sqlite3.connect(db_path)
      cur = conn.cursor()
      # Person data
      nationID = form_inputs['nationID']
      fname = form_inputs['fname']
      mname = form_inputs['mname']
      lname = form_inputs['lname']
      gender = form_inputs['gender']
      phonenumber = form_inputs['phonenumber']
      dob = form_inputs['dob']

      # Car data
      car_color = form_inputs['car_color']
      car_mark = form_inputs['car_mark']
      car_model = form_inputs['car_model']
      car_plate_letters = form_inputs['car_plate_letters']
      car_plate_nums = form_inputs['car_plate_nums']
      car_plate_type = form_inputs['car_plate_type']
      car_seats = form_inputs['car_seats']
      car_since_date = form_inputs['car_since_date']
      car_vin = form_inputs['car_vin']
      car_year = form_inputs['car_year']

      
      wp_id  = get_wp_id_by_nation_id()
      cur.execute("BEGIN TRANSACTION")
      query = 'insert into Person (per_nation_id, per_fname, per_mname, per_lname, per_gender, per_phonenumber, per_dob) values (?,?,?,?,?,?,?)'
      cur.execute(query, [nationID, fname, mname, lname, gender, phonenumber, dob])
      per_id = cur.lastrowid

      query = "INSERT INTO car (car_color, car_mark, car_model, car_plate_letters, car_plate_nums, car_plate_type, car_num_seats, car_since_date, car_vin, car_year, car_per_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
      cur.execute(query, [car_color, car_mark, car_model, car_plate_letters, car_plate_nums, car_plate_type, car_seats, car_since_date, car_vin, car_year, per_id])
      car_id = cur.lastrowid

      insert_new_repairement(cur, form_inputs, car_id, wp_id)

      conn.commit()

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

# check if rep_date != current date
def rep_date_bigger_current(rep_date):
  current_year = datetime.today().year
  rep_date = rep_date.strftime("%Y")
  if (int(rep_date) != current_year):
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

def get_wp_id_by_nation_id():
  nation_id = session["user"]
  conn = sqlite3.connect(db_path)
  cur = conn.cursor()
  cur.execute("SELECT per_id FROM Person WHERE per_nation_id =?", [str(nation_id)])
  per_id = cur.fetchone()[0]

  cur.execute("SELECT wp_id FROM workshop WHERE wp_per_id = ?", [per_id])
  wp_id = cur.fetchone()[0]
  return wp_id

def get_car_id_by_per_id(per_id):
  conn = sqlite3.connect(db_path)
  cur = conn.cursor()
  cur.execute("SELECT car_id FROM Car WHERE car_per_id =?", [str(per_id)])
  car_id = cur.fetchone()[0]
  return car_id

def get_per_id_by_nation_id(nation_id):
  conn = sqlite3.connect(db_path)
  cur = conn.cursor()
  cur.execute("SELECT per_id FROM Person WHERE per_nation_id =?", [str(nation_id)])
  per_id = cur.fetchone()[0]
  return per_id

def get_car_id_by_car_vin(car_vin):
  conn = sqlite3.connect(db_path)
  cur = conn.cursor()
  cur.execute("SELECT car_id FROM Car WHERE car_vin =?", [car_vin])
  car_id = cur.fetchone()[0]
  return car_id

def get_car_since_date_by_car_vin(car_vin):
  conn = sqlite3.connect(db_path)
  cur = conn.cursor()
  cur.execute("SELECT car_since_date FROM Car WHERE car_vin =?", [car_vin])
  car_since_date = cur.fetchone()[0]
  return car_since_date

def insert_new_repairement(cur, form_inputs, car_id, wp_id):
      # Repairment 
      rep_permission_paper_id = form_inputs['rep_permission_paper_id']
      rep_desc = form_inputs['rep_desc']
      rep_date = form_inputs['rep_date']
      rep_car_part = form_inputs['rep_car_part']

      query = "INSERT INTO Repairment (rep_date, rep_desc, rep_permission_paper_id, rep_car_id) VALUES (?,?,?,?)"
      cur.execute(query, [rep_date, rep_desc, rep_permission_paper_id, car_id])
      rep_id = cur.lastrowid

      for cp in rep_car_part:
        query = "INSERT INTO car_parts (cp_rep_id, cp_car_part) VALUES (?,?)"
        cur.execute(query, [rep_id, cp])
      
      query = "INSERT INTO workshop_repairs_repairment (wrr_wp_id, wrr_rep_id) VALUES (?,?)"
      cur.execute(query, [wp_id, rep_id])

def pre_insert_new_repairement(form_inputs):
  conn = sqlite3.connect(db_path)
  cur = conn.cursor()
  cur.execute("BEGIN TRANSACTION")
  car_id = get_car_id_by_car_vin(form_inputs["car_vin"])
  wp_id = get_wp_id_by_nation_id()
  insert_new_repairement(cur, form_inputs, car_id, wp_id)
  conn.commit()
  return True