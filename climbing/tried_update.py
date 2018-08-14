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

    last_qry = "SELECT boulder_name, area, sub_area, v_grade FROM boulders_tried ORDER BY est_date DESC, est_time DESC LIMIT 1;"

    last_entry = db.query(last_qry)[0]
        
    last_name, last_area, last_sub, last_grade = last_entry

    entry['boulder_name'] = last_name
    entry['area'] = last_area
    entry['sub_area'] = last_sub
    entry['v_grade'] = last_grade

    i = 1
    while i < 11:
        if ((i > 0) and (i < 8)):
            i, cats, entry_vals = process_basic(i, entry)
        elif ((i > 7) and (i < 10)):
            i, cats, entry_vals = process_time(i)
        elif ((i > 9) and (i < 11)):
            i, cats, entry_vals = process_complete(i)

        for cat, val in zip(cats, entry_vals):
            entry[cat] = val

    print "\n"

    if entry.get('sub_area') is None:
        sa = ""
    else:
        sa = "\nAND sub_area = '%s'" % (entry.get('sub_area'))

    prev_qry = """SELECT est_date, est_time
    FROM boulders_tried
    WHERE boulder_name = "%s"
    AND area = "%s"%s
    AND (est_date < "%s"
        OR
        (est_date = "%s" AND est_time < "%s")
    );"""

    prev_query = prev_qry % (entry.get('boulder_name'), entry.get('area'), sa, entry.get('est_date'), entry.get('est_date'), entry.get('est_time'))

    prev_cnt = db.query(prev_query)

    sess_num = len(prev_cnt)

    entry["session_num"] = sess_num+1

    db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
    db.conn.commit()

def process_basic(i, entry):
    cat, prompt = prompt_dict.get(i)
    last_val = entry.get(cat)

    user_prompt = "%s %s (last: %s): " % (i, prompt, last_val)

    val = raw_input(user_prompt)

    if val.lower() == "none":
        val = None

    i += 1
    try:
        if val[0] == "-":
            i = -int(val)
            return i, [cat], [None]
    except IndexError:
        return i, [cat], [last_val]
    except TypeError:
        pass

    return i, [cat], [val]

def process_time(i):
    cat, prompt = prompt_dict.get(i)
    user_prompt = "%s %s: " % (i, prompt)
    if i == 8:
        _days = raw_input(user_prompt)
        
        try:
            if _days[0] == "-":
                i = -int(_days)
                return i, [cat], [None]
        except TypeError:
            pass

        if _days == "":
            _days = 0
        cur_date = date.today()
        est_date = cur_date - timedelta(days=int(_days))
        val = est_date

    if i == 9:
        _time = raw_input(user_prompt)
        
        try:
            if _time[0] == "-":
                i = -int(_time)
                return i, [cat], [None]
        except TypeError:
            pass

        try:
            _time = str(int(_time)) + ":00"
        except ValueError:
            _time = _time
        est_time = datetime.strptime(_time,'%H:%M').time()
        val = est_time

    i += 1
    return i, [cat], [val]

def process_complete(i):
    done = False
    while done is False:
        completed_prompt = "%s Completed (y/n): " % (i)
        completed = raw_input(completed_prompt)

        try:
            if completed[0] == "-":
                i = -int(completed)
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
        i += 2
    else:
        return_interest = raw_input("Return Interest (0-5): ")
    
        i += 1
        try:
            if return_interest[0] == "-":
                i = -int(return_interest)
                return i, ['return_interest'], [None]
        except TypeError:
            pass

        return_interest = min(int(return_interest), 5)

    return i, ['completed', 'return_interest'], [completed, return_interest]


if __name__ == "__main__":     
    initiate()
