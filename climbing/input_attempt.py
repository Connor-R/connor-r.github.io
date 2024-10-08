import sys
import os
import argparse
from datetime import datetime, timedelta, date


from py_db import db

db = db("personal")

prompt_dict = {
    1:["boulder_name","Boulder Name"],
    2:["area","Area"],
    3:["sub_area","Sub Area"],
    4:["v_grade","V Grade"],
    5:["session_attempts","Estimated Number of Attempts"],
    6:["session_minutes","Estimated Number of Minutes"],
    7:["comment","Comment"],
    8:["session_date","Days since attempt (0 for today, 1 for yesterday, etc.)"],
    9:["session_start","Attempted Time (24:60 format)"],
    10:["completed", "Completed (y/n)"]
}

completed_dict = {
    1:["soft_hard", "\tWas the problem bounty extra soft, soft, or hard (hit RETURN for neither)"],
    2:["stars", "\tStars (20-80)"],
    3:["fa", "\tDid you FA this problem? (y/n)"],
}

attributes_dict = {
    1:["athletic", "athletic"],
    2:["cruxy", "cruxy"],
    3:["slopey", "slopey"],
    4:["crimpy", "crimpy"],
    5:["sharp", "sharp"],
    6:["technical", "technical"],
    7:["power", "power"],
    8:["endurance", "endurance"],
    9:["overhang", "overhang"],
    10:["vertical", "vertical"],
    11:["slab", "slab"],
    12:["roof", "roof"],
    13:["scary", "scary"],
}

incompleted_dict = {
    1:["return_interest", "\tReturn Interest (0-5)"],
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

    entry["boulder_name"] = last_name
    entry["area"] = last_area
    entry["sub_area"] = last_sub
    entry["v_grade"] = last_grade
    entry["session_attempts"] = last_attempts
    entry["session_minutes"] = last_minutes
    entry["comment"] = ""
    entry["session_date"] = last_date
    entry["session_start"] = last_time
    entry["completed"] = completed



    i = 1
    while i < 11:
        i, cats, entry_vals = process_basic(i, entry)
        for cat, val in zip(cats, entry_vals):
            if cat is not None:
                entry[cat] = val

    print "\n"

    if entry["completed"] == "COMPLETED":
        j = 1
        while j < 4:
            j, cats, entry_vals = process_complete(j, entry)
            for cat, val in zip(cats, entry_vals):
                if cat is not None:
                    entry[cat] = val

        while j == 4:
            j, cats, entry_vals = process_attributes(j, entry)
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

    # raw_input(entry)
    db.insertRowDict(entry, "boulder_problems", insertMany=False, replace=True, rid=0, debug=1)
    db.conn.commit()

def process_basic(i, entry):
    cat, prompt = prompt_dict.get(i)
    last_val = entry.get(cat)
    last_str = last_val

    if cat == "sub_area":
        sub_areas = {}

        sa_qry = """SELECT bp.sub_area
        FROM boulder_problems bp
        WHERE bp.area = "%s"
        GROUP BY bp.sub_area
        ORDER BY SUM(IF(bp.completed="COMPLETED",1,0)) DESC, COUNT(*) DESC
        ;""" % (entry.get("area"))

        area_lists = db.query(sa_qry)
        if area_lists != ():
            last_str = ""
            # raw_input(area_lists)
            for j, sa in enumerate(area_lists):
                sub_areas[j] = sa[0]
                # raw_input(sub_areas)
            for k, v in sub_areas.items():
                last_str += "\n\t" + str(k) + " " + str(v)
            last_str += "\nCorresponding sub area #: "
        else:
            last_str = "(new area!): "
    elif cat == "comment":
        last_str = ": "
    elif cat == "v_grade":

        v_qry = """SELECT DISTINCT bp.v_grade
        FROM boulder_problems bp
        WHERE 1
            AND bp.boulder_name = "%s"
            AND bp.area = "%s"
            AND bp.sub_area = "%s"
        ;""" % (entry.get("boulder_name"), entry.get("area"), entry.get("sub_area"))

        prev_v = db.query(v_qry)

        if prev_v != () and len(prev_v) == 1:
            last_val = prev_v[0][0]
            last_str = " (has been recorded as %s previously): " % (last_val)
        else:
            last_str = " (last: " + str(last_str) + "): "
    else:
        last_str = " (last: " + str(last_str) + "): "

    user_prompt = "%s %s%s" % (i, prompt, last_str)

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

    if cat == "sub_area" and val.isdigit() and int(val) in sub_areas:
        val = sub_areas.get(int(val))

    if cat == "session_date" and val != "":
        cur_date = date.today()
        session_date = cur_date - timedelta(days=int(val))
        val = session_date

    if cat == "session_start":
        try:
            _time = str(int(val)) + ":00"
        except ValueError:
            _time = val
        session_start = datetime.strptime(_time,"%H:%M").time()
        val = session_start

    if cat == "completed":
        if val.lower() == "y":
            val = "COMPLETED"
        else:
            val = None

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

    if (val.lower() == "none" or val[0].lower() == "n"):
        val = None
    elif (val[0].lower() == "y" and cat not in ("stars", "soft_hard")):
        val = cat.upper()
    elif (cat == "soft_hard" and val.lower() in ("bounty extra soft", "soft", "hard")):
        val = val.upper()
    elif (cat == "stars" and (val > 80 or val < 20)):
        val = val
    else:
        print "\t\t\t~ERROR~ the answer %s is not a valid value for the field %s, please try again" % (val, cat)
        return j-1, [None], [None]

    return j, [cat], [val]


def process_attributes(j, entry):
    cats=[]
    print '\nATTRIBUTES:'
    for att in range(1,14):
        cat, prompt = attributes_dict.get(att)
        print '\t', att, ' ', prompt
    val = raw_input('Enter relevant indices, separated by spaces: ')

    j += 1

    if val == "":
        return j, [None], [None]

    try:
        indices = list(map(int, val.split(' ')))
    except (ValueError, TypeError):
        print "\n\t\t\t~ERROR~ the answer '%s' is not a valid value for this question, please try again\n" % (val)
        return j-1, [None], [None]

    for ind in indices:
        cat, prompt = attributes_dict.get(ind)
        cats.append(cat.upper())

    return j, cats, cats



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

    try:
        val = int(val)
    except ValueError:
        print "\t\t\t~ERROR~ the answer %s is not a valid value for the field %s, please try again" % (val, cat)
        return j-1, [None], [None]

    if (cat == "return_interest" and val <= 5 and val >= 1):
        val = val
    else:
        print "\t\t\t~ERROR~ the answer %s is not a valid value for the field %s, please try again" % (val, cat)
        return j-1, [None], [None]

    return j, [cat], [val]


if __name__ == "__main__":     
    initiate()
