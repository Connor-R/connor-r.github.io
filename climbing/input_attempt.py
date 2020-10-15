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
    5:['session_attempts','Estimated Number of Attempts'],
    6:['session_minutes','Estimated Number of Minutes'],
    7:['comment','Comment'],
    8:['session_date','Days since attempt (0 for today, 1 for yesterday, etc.)'],
    9:['session_start','Attempted Time (24:60 format)'],
    10:['completed', 'Completed (y/n)']
}

completed_dict = {
    1:['soft_hard', '\tWas the problem bounty extra soft, soft, or hard (hit RETURN for neither)'],
    2:['stars', '\tStars (20-80)'],
    3:['fa', '\tDid you FA this problem? (y/n)'],
    4:['athletic', '\t\tathletic (y/n)'],
    5:['cruxy', '\t\tcruxy (y/n)'],
    6:['slopey', '\t\tslopey (y/n)'],
    7:['crimpy', '\t\tcrimpy (y/n)'],
    8:['sharp', '\t\tsharp (y/n)'],
    9:['technical', '\t\ttechnical (y/n)'],
    10:['power', '\t\tpower (y/n)'],
    11:['endurance', '\t\tendurance (y/n)'],
    12:['overhang', '\t\toverhang (y/n)'],
    13:['vertical', '\t\tvertical (y/n)'],
    14:['slab', '\t\tslab (y/n)'],
    15:['roof', '\t\troof (y/n)'],
    16:['scary', '\t\tscary (y/n)'],
}

incompleted_dict = {
    1:['return_interest', '\tReturn Interest (0-5)'],
}

def initiate():
    entry = {}
    print "\nUpdate Attempted Boulder\n"

    last_qry = """SELECT boulder_name
    , area
    , sub_area
    , v_grade
    , session_attempts
    , session_minutes
    , session_date
    , session_start
    , completed
    FROM boulder_problems
    ORDER BY session_date DESC, session_start DESC
    LIMIT 1
    ;"""

    last_entry = db.query(last_qry)[0]
        
    last_name, last_area, last_sub, last_grade, last_attempts, last_minutes, last_date, last_time, completed = last_entry

    entry['boulder_name'] = last_name
    entry['area'] = last_area
    entry['sub_area'] = last_sub
    entry['v_grade'] = last_grade
    entry['session_attempts'] = last_attempts
    entry['session_minutes'] = last_minutes
    entry['comment'] = ""
    entry['session_date'] = last_date
    entry['session_start'] = last_time
    entry['completed'] = completed



    i = 1
    while i < 11:
        i, cats, entry_vals = process_basic(i, entry)
        for cat, val in zip(cats, entry_vals):
            if cat is not None:
                entry[cat] = val

    print "\n"

    if entry['completed'] == 'COMPLETED':
        j = 1
        while j < 17:
            j, cats, entry_vals = process_complete(j, entry)
            for cat, val in zip(cats, entry_vals):
                if cat is not None:
                    entry[cat] = val

    else:
        j = 1
        while j < 2:
            j, cats, entry_vals = process_incomplete(j, entry)
            for cat, val in zip(cats, entry_vals):
                if cat is not None:
                    entry[cat] = val


    print "\n"

    raw_input(entry)
    db.insertRowDict(entry, 'boulder_problems', insertMany=False, replace=True, rid=0, debug=1)
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
            return i, [None], [None]
    except IndexError:
        return i, [cat], [last_val]
    except TypeError:
        pass

    if cat == 'session_date' and val != '':
        cur_date = date.today()
        session_date = cur_date - timedelta(days=int(val))
        val = session_date

    if cat == 'session_start':
        try:
            _time = str(int(val)) + ":00"
        except ValueError:
            _time = val
        session_start = datetime.strptime(_time,'%H:%M').time()
        val = session_start

    if cat == 'completed' and val.lower() == 'y':
        val = 'COMPLETED'

    return i, [cat], [val]


def process_complete(j, entry):
    cat, prompt = completed_dict.get(j)

    user_prompt = "%s %s: " % (j, prompt)

    val = raw_input(user_prompt)

    j += 1
    try:
        if val[0] == "-":
            j = -int(val)
            return j, [None], [None]
    except IndexError:
        return j, [cat], [None]
    except TypeError:
        pass

    if (val.lower() == "none" or val[0].lower() == 'n'):
        val = None
    elif (val[0].lower() == 'y' and cat not in ('stars', 'soft_hard')):
        val = cat.upper()
    elif (cat == 'soft_hard' and val.lower() in ('bounty extra soft', 'soft', 'hard')):
        val = val.upper()
    elif (cat == 'stars' and (val > 80 or val < 20)):
        val = val
    else:
        print '\t\t\t~ERROR~ the answer %s is not a valid value for the field %s, please try again' % (val, cat)
        return j-1, [None], [None]

    return j, [cat], [val]


def process_incomplete(j, entry):
    cat, prompt = incompleted_dict.get(j)

    user_prompt = "%s %s: " % (j, prompt)

    val = raw_input(user_prompt)

    j += 1
    try:
        if val[0] == "-":
            j = -int(val)
            return j, [None], [None]
    except IndexError:
        return j, [cat], [None]
    except TypeError:
        pass

    if (cat == 'return_interest' and (val > 5 or val < 1)):
        val = cat
    else:
        print '\t\t\t~ERROR~ the answer %s is not a valid value for the field %s, please try again' % (val, cat)
        return j-1, [None], [None]

    return j, [cat], [val]


if __name__ == "__main__":     
    initiate()
