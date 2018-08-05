import sys
import os
import argparse
from datetime import datetime, timedelta, date


from py_db import db

db = db('personal')

entry = {}

print "\nUpdate Attempted Boulder\n"

name_prompt = "Boulder Name: "
name = raw_input(name_prompt)
entry["boulder_name"] = str(name)


area_prompt = "Area: "
area = raw_input(area_prompt)
entry["area"] = str(area)


sub_area_prompt = "Sub Area: "
sub_area = raw_input(sub_area_prompt)
entry["sub_area"] = str(sub_area)


_days_prompt = "Days since attempt (0 for today, 1 for yesterday, etc.): "
_days = raw_input(_days_prompt)
cur_date = date.today()
est_date = cur_date - timedelta(days=int(_days))
entry["est_date"] = est_date


_time_prompt = "Attempted Time (24:60 format): "
_time = raw_input(_time_prompt)
est_time = datetime.strptime(_time,'%H:%M').time()
entry["est_time"] = est_time


grade_prompt = "V Grade: "
grade = raw_input(grade_prompt)
entry["v_grade"] = float(grade)


attempts_prompt = "Estimated Number of Attempts: "
attempts = raw_input(attempts_prompt)
entry["est_attempts"] = int(attempts)


minutes_prompt = "Estimated Number of Minutes: "
minutes = raw_input(minutes_prompt)
entry["est_minutes"] = int(minutes)


comment_prompt = "Comment: "
comment = raw_input(comment_prompt)
entry["comment"] = str(comment)


done = False
while done is False:
    completed_prompt = "Completed (y/n): "
    completed = raw_input(completed_prompt)
    if completed.lower() == 'y':
        completed = "TRUE"
        done = True
    elif completed.lower() == 'n':
        completed = "FALSE"
        done = True
entry["completed"] = str(completed)


if completed == "TRUE":
    return_interest = None
else:
    return_interest = raw_input("Return Interest: ")
    return_interest = int(return_interest)
entry["return_interest"] = return_interest

print "\n"

db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
db.conn.commit()