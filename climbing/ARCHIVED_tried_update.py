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

completed_dict = {
    1:['soft_hard', 'Was the problem soft or hard (hit RETURN for neither)'],
    2:['stars', 'Stars (1-3)'],
    3:['fa', 'Did you FA this problem? (y/n)'],
    4:['recommended', 'Do you recommend this problem? (y/n)'],
}

def initiate():
    entry = {}
    print "\nUpdate Attempted Boulder\n"

    last_qry = "SELECT boulder_name, area, sub_area, v_grade, est_attempts, est_minutes, est_date FROM boulders_tried ORDER BY est_date DESC, est_time DESC LIMIT 1;"

    last_entry = db.query(last_qry)[0]
        
    last_name, last_area, last_sub, last_grade, last_attempts, last_minutes, last_date = last_entry

    entry['boulder_name'] = last_name
    entry['area'] = last_area
    entry['sub_area'] = last_sub
    entry['v_grade'] = last_grade
    entry['est_attempts'] = last_attempts
    entry['est_minutes'] = last_minutes
    entry['comment'] = ""
    entry['est_date'] = last_date
    entry['est_time'] = datetime.strptime('00:00:00','%H:%M:%S').time()



    i = 1
    while i < 11:
        if ((i > 0) and (i < 8)):
            i, cats, entry_vals = process_basic(i, entry)
        elif ((i > 7) and (i < 10)):
            i, cats, entry_vals = process_time(i)
        elif ((i > 9) and (i < 11)):
            i, cats, entry_vals = process_complete(i, entry)

        for cat, val in zip(cats, entry_vals):
            if cat is not None:
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
            return i, [None], [None]
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
                return i, [None], [None]
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
                return i, [None], [None]
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

def process_complete(i, entry):
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

            entry2 = entry.copy()
            j = 1
            while j < 5:
                if ((j > 0) and (j < 3)):
                    j, cats2, vals2 = update_completed_basic(j, entry2)
                elif ((j > 2) and (j < 5)):
                    j, cats2, vals2 = update_completed_boolean(j, entry2)

                for cat2, val2 in zip(cats2, vals2):
                    if cat2 is not None:
                        entry2[cat2] = val2

            enter_completed(entry2)


        elif completed.lower() == 'n':
            completed = "FALSE"
            done = True

    if completed == "TRUE":
        return_interest = None
        i += 2
    else:
        return_interest = raw_input("\tReturn Interest (0-5): ")
    
        i += 1
        try:
            if return_interest[0] == "-":
                i = -int(return_interest)
                return i, [None], [None]
        except TypeError:
            pass

        return_interest = min(int(return_interest), 5)

    return i, ['completed', 'return_interest'], [completed, return_interest]

def update_completed_basic(j, entry2):
    cat, prompt = completed_dict.get(j)

    user_prompt = "\t%s %s: " % (j, prompt)

    val = raw_input(user_prompt)

    if val.lower() == "none":
        val = None

    j += 1
    try:
        if val[0] == "-":
            j = -int(val)
            return j, [None], [None]
    except IndexError:
        return j, [cat], [None]
    except TypeError:
        pass

    return j, [cat], [val.upper()]

def update_completed_boolean(j, entry2):
    cat, prompt = completed_dict.get(j)

    user_prompt = "\t%s %s: " % (j, prompt)

    val = raw_input(user_prompt)

    try:
        if val[0] == "-":
            j = -int(val)
            return j, [None], [None]
    except IndexError:
        return j+1, [cat], [None]
    except TypeError:
        pass

    j += 1
    if val.lower() == 'y':
        val = cat.upper()
    else:
        val = None

    return j, [cat], [val]

def enter_completed(entry2):

    entry2['ascent_date'] = entry2.get('est_date')

    prev_time = entry2.get("est_time")
    prev_dtime = datetime(100, 1, 1, prev_time.hour, prev_time.minute, prev_time.second)
    final_time = prev_dtime + timedelta(minutes=int(entry2.get("est_minutes")))
    entry2["final_time"] = final_time.time()

    grade_query = "SELECT MAX(font) AS font, 8a_points FROM boulders_grades WHERE hueco = '%s' GROUP BY hueco" % (entry2.get("v_grade"))
    grade_res = db.query(grade_query)
    if len(grade_res) != 1:
        print "\n\n\nERROR", str(entry2.get("v_grade")), "HAS LENGTH", str(len(res))
    else:
        euro_grade, pts_base = grade_res[0]

    entry2['euro_grade'] = euro_grade
    pts = pts_base

    previous_qry = """SELECT 
    SUM(est_attempts) AS attempts,
    SUM(est_minutes) AS minutes,
    COUNT(*) AS sessions
    FROM boulders_tried
    WHERE boulder_name = "%s"
    AND area = "%s"
    AND sub_area = "%s"
    AND completed != "TRUE"
    GROUP BY boulder_name, area;"""
    previous_query = previous_qry % (entry2.get("boulder_name"), entry2.get("area"), entry2.get("sub_area"))

    previous_res = db.query(previous_query)
    if len(previous_res) > 1:
        print "\n\n\nERROR", str(entry2.get("boulder_name")), "HAS LENGTH", str(len(res))
    elif len(previous_res) == 0:
        prev_att, prev_min, prev_sess = [0,0,0]
    else:
        prev_att, prev_min, prev_sess = previous_res[0]

    est_attempts = int(entry2.get("est_attempts")) + prev_att
    entry2["est_attempts"] = est_attempts

    flash = None
    if est_attempts == 1:
        flash = "FLASH"
        pts += 50
    entry2["flash"] = flash

    if est_attempts == 2:
        pts += 2

    if entry2.get("FA") == "FA":
        pts += 20
        

    entry2["8a_pts"] = pts

    est_minutes = int(entry2.get("est_minutes")) + prev_min
    entry2["est_minutes"] = est_minutes

    est_sessions = 1 + int(prev_sess)
    entry2["est_sessions"] = est_sessions

    comment = "Total_Duration={'Final Time':'" + str(final_time.hour).zfill(2) + ":" + str(final_time.minute).zfill(2) + "', 'Attempts':" + str(est_attempts) + ", 'Minutes':" + str(est_minutes) + ", 'Sessions':" + str(est_sessions) + "}. " + str(entry2.get("comment"))
    entry2['comment'] = comment

    updated = "FALSE"

    del entry2['est_time']
    del entry2['est_date']

    db.insertRowDict(entry2, 'boulders_completed', insertMany=False, replace=True, rid=0, debug=1)
    db.conn.commit()

if __name__ == "__main__":     
    initiate()
