from py_db import db
import argparse
from time import time

db = db('personal')


def initiate():
    start_time = time()

    print "\ndeleting backfilled tried boulders"
    db.query("DELETE FROM boulders_tried WHERE return_interest IS NULL;")
    db.conn.commit()

    print "\nupdating tried boulders"
    update_boulders()

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\ncompleted_to_tried.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)

def update_boulders():
    qry = """SELECT 
    ascent_date, boulder_name, area, sub_area, v_grade, bc.comment,
    (bc.est_attempts - IFNULL(bt.est_attempts,0)) AS 'update_attempts',
    (bc.est_minutes - IFNULL(bt.est_minutes,0)) AS 'update_minutes',
    (bc.est_sessions - IFNULL(bt.est_sessions,0)) AS 'update_sessions', 
    (1 - IFNULL(bt.sent,0)) AS 'update_completed'
    FROM boulders_completed bc
    LEFT JOIN(
        SELECT 
        boulder_name, area, sub_area, SUM(est_attempts) AS est_attempts, SUM(est_minutes) AS est_minutes, COUNT(*) AS est_sessions,
        SUM(IF(completed="TRUE",1,0)) AS sent
        FROM boulders_tried
        GROUP BY boulder_name, area, sub_area
    ) bt USING (boulder_name, area, sub_area)
    WHERE bc.updated != "FALSE"
    ORDER BY update_sessions DESC;"""

    res = db.query(qry)

    for row in res:
        process_update(row)

def process_update(row):
    _date, boulder_name, area, sub_area, v_grade, final_comment, u_atts, u_mins, u_sessions, u_completed = row

    return_interest = None
    update_sessions = u_sessions - u_completed

    for sess_num in range(1,update_sessions+1):
        entry = {}
        return_interest = None

        if sess_num < 10:
            sess_val = "0"+str(sess_num)
        else:
            sess_val = str(sess_num)
        est_time = '00:00:%s' % (sess_val)

        est_attempts = 1
        est_minutes = 1
        update_comment = "Backfill Comment #%s" % (sess_num)

        entry["est_date"] = _date
        entry["est_time"] = est_time
        entry["boulder_name"] = boulder_name
        entry["area"] = area
        entry["sub_area"] = sub_area
        entry["v_grade"] = v_grade
        entry["est_attempts"] = est_attempts
        entry["est_minutes"] = est_minutes
        entry["return_interest"] = return_interest
        entry["comment"] = update_comment
        entry["completed"] = "FALSE"

        db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()

    if u_completed == 1:
        entry = {}
        return_interest = None
        est_time = '23:59:59'
        est_attempts = u_atts - update_sessions
        est_minutes = u_mins - update_sessions
        update_comment = "".join(final_comment.split("}.")[1:]).strip()

        entry["est_date"] = _date
        entry["est_time"] = est_time
        entry["boulder_name"] = boulder_name
        entry["area"] = area
        entry["sub_area"] = sub_area
        entry["v_grade"] = v_grade
        entry["est_attempts"] = est_attempts
        entry["est_minutes"] = est_minutes
        entry["return_interest"] = return_interest
        entry["comment"] = update_comment
        entry["completed"] = "TRUE"

        db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()




if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()
