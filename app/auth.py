import sqlite3
import bcrypt
from pprint import pprint


db_path = 'app\carDNA.db'

#signup
def insert_new_user(form_inputs):  
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # person data
        nationID = form_inputs['nationID']
        fname = form_inputs['fname']
        mname = form_inputs['mname']
        lname = form_inputs['lname']
        gender = form_inputs['gender']
        phonenumber = form_inputs['phonenumber']
        dob = form_inputs['dob']

        # workshop data
        city = form_inputs['city']
        location = form_inputs['location']
        comm_act_num = form_inputs['comm_act_num']

        # user data
        email = form_inputs['email']
        password = form_inputs['password']
        password=password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur.execute("BEGIN TRANSACTION")
        query = 'insert into Person (per_nation_id, per_fname, per_mname, per_lname, per_gender, per_phonenumber, per_dob) values (?,?,?,?,?,?,?)'
        cur.execute(query, [nationID, fname, mname, lname, gender, phonenumber, dob])
        per_id = cur.lastrowid

        query = "insert into User (usr_email, usr_password) VALUES (?,?)"
        cur.execute(query, [email, hashed_password])
        usr_id = cur.lastrowid


        query = "insert into Workshop (wp_city, wp_comm_act_num, wp_location, wp_per_id, wp_usr_id) values (?,?,?,?,?)"
        cur.execute(query, [city, comm_act_num, location, per_id, usr_id])

        conn.commit()
    except Exception as ex:
        return ex
    return True

# check if nationID is already registered
def registered_nationID(nationID):
      query= "SELECT per_id FROM Person WHERE per_nation_id = ?"
      return check_registered(query, nationID)

# check if phonenumber is already registered
def registered_phonenumber(phonenumber):
      query= "SELECT per_id FROM Person WHERE per_phonenumber = ?"
      return check_registered(query, phonenumber)

# check if email is already registered
def registered_email(email):
      query= "SELECT usr_id FROM User WHERE usr_email = ?"
      return check_registered(query, email)

# check if comm_act_num is already registered
def registered_comm_act_num(comm_act_num):
    query= "SELECT wp_id FROM Workshop WHERE wp_comm_act_num = ?"
    return check_registered(query, comm_act_num)

def check_registered(query, param):
    try:
      conn = sqlite3.connect(db_path)
      cur = conn.cursor()
      cur.execute(query, [param])
      result = cur.fetchall()
      if len(result) >= 1:
        pprint(result)
        quit()
        return True
      else:
        return False
    except Exception as ex:
      return ex

def check_login(nationID, password):

    password = password.encode('utf-8')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT per_id FROM Person WHERE per_nation_id = ?"
    cur.execute(query, [nationID])
    per_id = cur.fetchone()
    if (per_id is not None):
      per_id = per_id[0]
      query = "SELECT wp_usr_id FROM Workshop WHERE wp_per_id = ?"
      cur.execute(query, [per_id])
      usr_id = cur.fetchone()[0]

      query = "SELECT usr_password FROM User WHERE usr_id = ?"
      cur.execute(query, [usr_id])
      hashed_password = cur.fetchone()[0]
      if bcrypt.checkpw(password, hashed_password):
        return True
      else:
        return False
    else:
      return False
      

def get_fname_by_per_nation_id(nationID):
  try:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = "SELECT per_fname FROM Person WHERE per_nation_id = ?"
    cur.execute(query, [nationID])
    fname = cur.fetchone()[0]
    if fname:
      return fname
  except Exception as ex:
      return ex