import sys
import os
import argparse
from datetime import datetime, timedelta, date


from py_db import db

db = db('personal')

prompt_dict = {
    1:['boulder_name','Boulder Name'],
    2:['area','Area'],
    3:['sub_area','Sub Area'],
    4:['v_grade','V Grade'],
    5:['est_attempts','Estimated Number of Attempts'],
    6:['est_minutes','Estimated Number of Minutes'],
    7:['comment','Comment'],
    8:['est_date','Days since attempt (0 for today, 1 for yesterday, etc.)'],
    9:['est_time','Attempted Time (24:60 format)'],
}


def initiate():
    entry = {}
    print "\nUpdate Attempted Boulder\n"

    i = 1
    while i < 11:
        if ((i > 0) and (i < 8)):
            i, cats, entry_vals = process_basic(i)
        elif ((i > 7) and (i < 10)):
            i, cats, entry_vals = process_time(i)
        elif ((i > 9) and (i < 11)):
            i, cats, entry_vals = process_complete(i)

        for cat, val in zip(cats, entry_vals):
            entry[cat] = val

    print "\n"

    db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
    db.conn.commit()

def process_basic(i):
    cat, prompt = prompt_dict.get(i)

    user_prompt = "%s %s: " % (i, prompt)

    val = raw_input(user_prompt)

    i += 1
    try:
        if val[0] == "-":
            i = -int(val)
            return i, [cat], [None]
    except TypeError:
        pass

    return i, [cat], [val]

def process_time(i):
    cat, prompt = prompt_dict.get(i)
    user_prompt = "%s %s: " % (i, prompt)
    if i == 8:
        _days = raw_input(user_prompt)
        cur_date = date.today()
        est_date = cur_date - timedelta(days=int(_days))
        val = est_date

    if i == 9:
        _time = raw_input(user_prompt)
        est_time = datetime.strptime(_time,'%H:%M').time()
        val = est_time

    i += 1
    try:
        if val[0] == "-":
            i = -int(val)
            return i, [cat], [None]
    except TypeError:
        pass

    return i, [cat], [val]

def process_complete(i):
    done = False
    while done is False:
        completed_prompt = "%s Completed (y/n): " % (i)
        completed = raw_input(completed_prompt)

        try:
            if completed[0] == "-":
                i = -int(val)
                return i, ['completed'], [None]
        except TypeError:
            pass

        if completed.lower() == 'y':
            completed = "TRUE"
            done = True
        elif completed.lower() == 'n':
            completed = "FALSE"
            done = True

    if completed == "TRUE":
        return_interest = None
    else:
        return_interest = raw_input("Return Interest (1-5): ")
        return_interest = int(return_interest)

    i += 1
    try:
        if return_interest[0] == "-":
            i = -int(val)
            return i, ['return_interest'], [None]
    except TypeError:
        pass

    return i, ['completed', 'return_interest'], [completed, return_interest]


if __name__ == "__main__":     
    initiate()
