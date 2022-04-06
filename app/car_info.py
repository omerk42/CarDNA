import sqlite3
from pprint import pprint
from db import db_path
from repairForm import get_car_id_by_car_vin

def get_car_repairments(car_id):
  
  conn = sqlite3.connect(db_path)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  cur.execute("SELECT car_vin,car_num_seats,car_mark,car_model,car_year,car_color,car_plate_letters,car_plate_nums,car_plate_type,car_since_date FROM Car WHERE car_id =?", [car_id])
  car = [dict(r) for r in cur.fetchall()]

  cur.execute("SELECT rep_id,rep_date,rep_desc,rep_permission_paper_id FROM Repairment WHERE rep_car_id=?", [car_id])
  repairments = [dict(r) for r in cur.fetchall()]
  rep_ids = []
  for rep in repairments:
    rep_ids.append(rep['rep_id'])

  conn = sqlite3.connect(db_path)
  cur = conn.cursor()
  car_parts = dict()
  for rep_id in rep_ids:
    cur.execute("SELECT cp_car_part FROM car_parts WHERE cp_rep_id=?", [rep_id])
    car_parts[rep_id] = cur.fetchall()

  '''
    car[0] holds car object information
    repairments holds list of repairments for the car
    rep_ids holds the repairments ids
    car_parts holds car_parts for each rep_id
  '''
  return car[0], repairments, rep_ids, car_parts


