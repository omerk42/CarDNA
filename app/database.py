from contextlib import nullcontext
import sqlite3
import bcrypt

db_path = 'carDNA.db'

def get_db_connection():
    conn = None
    try:
      conn = sqlite3.connect(db_path)

    except Exception:
      return Exception

    return conn

def insert_new_user(form_inputs):  #signup
    try:
        conn = get_db_connection
        cur = conn.cursor()
        username = form_inputs['username']
        password = form_inputs['password']

        password=password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        query = 'insert into login_info (username, password) values (?,?)'
        cur.execute(query, [username, hashed_password])
        conn.commit()
    except Exception as ex:
        return ex
    return 'You can login now !'