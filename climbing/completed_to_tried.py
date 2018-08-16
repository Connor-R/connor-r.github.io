from py_db import db
import argparse
from time import time

db = db('personal')


def initiate():
    start_time = time()

    print "\ndeleting backfilled tried boulders"
    db.query("DELETE FROM boulders_tried WHERE return_interest IS NULL AND completed = 'FALSE';")
    db.conn.commit()

    print "\nupdating tried boulders"
    update_boulders()

    print "\nupdating session numbers on tried boulders"
    update_sessions()

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\ncompleted_to_tried.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)

def update_boulders():
    qry = """SELECT 
    ascent_date, boulder_name, area, sub_area, v_grade, bc.comment,
    TIMEDIFF(bc.final_time, SEC_TO_TIME(fin.final_min*60)) AS 'final_time', 
    fin.final_min,
    fin.final_att,
    bc.est_sessions,
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
    LEFT JOIN(
        SELECT boulder_name, area, sub_area, 
        bc2.est_minutes-IFNULL(bt2.fail_minutes,0) AS 'final_min', 
        bc2.est_attempts-IFNULL(bt2.fail_attempts,0) AS 'final_att'
        FROM boulders_completed bc2
        LEFT JOIN (
            SELECT boulder_name, area, sub_area, SUM(est_attempts) AS fail_attempts, SUM(est_minutes) AS fail_minutes FROM boulders_tried WHERE completed = 'FALSE' GROUP BY boulder_name, area, sub_area
        ) bt2 USING (boulder_name, area, sub_area)
    ) fin USING (boulder_name, area, sub_area)
    WHERE bc.updated != "FALSE"
    ORDER BY ascent_date DESC, update_sessions DESC;"""

    res = db.query(qry)

    for row in res:
        process_update(row)

def process_update(row):
    _date, boulder_name, area, sub_area, v_grade, final_comment, final_time, final_minutes, final_attempts, final_sessions, u_atts, u_mins, u_sessions, u_completed = row

    return_interest = None
    update_sessions = u_sessions - u_completed
    update_comment = "".join(final_comment.split("}.")[1:]).replace("*Bounty Extra Soft*.","").strip()

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
        backfill_comment = "Backfill Comment #%s" % (sess_num)

        entry["est_date"] = _date
        entry["est_time"] = est_time
        entry["boulder_name"] = boulder_name
        entry["area"] = area
        entry["sub_area"] = sub_area
        entry["v_grade"] = v_grade
        entry["est_attempts"] = est_attempts
        entry["est_minutes"] = est_minutes
        entry["return_interest"] = return_interest
        entry["session_num"] = sess_num        
        entry["completed"] = "FALSE"
        entry["comment"] = backfill_comment

        db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()

    if (u_completed == 1):
        entry = {}
        return_interest = None
        est_time = final_time
        est_attempts = final_attempts - update_sessions
        est_minutes = final_minutes - update_sessions

        entry["est_date"] = _date
        entry["est_time"] = est_time
        entry["boulder_name"] = boulder_name
        entry["area"] = area
        entry["sub_area"] = sub_area
        entry["v_grade"] = v_grade
        entry["est_attempts"] = est_attempts
        entry["est_minutes"] = est_minutes
        entry["return_interest"] = return_interest
        entry["session_num"] = final_sessions
        entry["completed"] = "TRUE"
        entry["comment"] = update_comment

        db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()

    comment_updater(boulder_name, area, sub_area, update_comment)


def comment_updater(boulder_name, area, sub_area, update_comment):
    qry = """SELECT *
    FROM boulders_tried
    WHERE boulder_name = "%s"
    AND area = "%s"
    AND sub_area = "%s"
    AND completed = "TRUE";"""

    query = qry % (boulder_name, area, sub_area)

    res = db.query(query)

    if len(res) != 1:
        print "\n\n\nERROR", boulder_name, "HAS LENGTH", str(len(res))
    else:
        entry = {}
        _date, est_time, boulder_name, area, sub_area, v_grade, est_attempts, est_minutes, return_interest, session_num, completed, first_comment = res[0]

        entry["est_date"] = _date
        entry["est_time"] = est_time
        entry["boulder_name"] = boulder_name
        entry["area"] = area
        entry["sub_area"] = sub_area
        entry["v_grade"] = v_grade
        entry["est_attempts"] = est_attempts
        entry["est_minutes"] = est_minutes
        entry["return_interest"] = return_interest
        entry["session_num"] = session_num
        entry["completed"] = "TRUE"
        entry["comment"] = update_comment

        db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()


def update_sessions():
    qry = """SELECT boulder_name, area, sub_area
    FROM boulders_tried
    WHERE est_date > '0000-00-00'
    GROUP BY boulder_name, area, sub_area;"""

    res = db.query(qry)

    for row in res:
        boulder_name, area, sub_area = row

        ind_qry = """SELECT *
        FROM boulders_tried
        WHERE boulder_name = "%s"
        AND area = "%s"
        AND sub_area = "%s"
        ORDER BY est_date, est_time;"""

        ind_query = ind_qry % (boulder_name, area, sub_area)

        ind_res = db.query(ind_query)

        for cnt, ind_row in enumerate(ind_res):
            entry = {}
            _date, est_time, boulder_name, area, sub_area, v_grade, est_attempts, est_minutes, return_interest, session_num, completed, first_comment = ind_row

            entry["est_date"] = _date
            entry["est_time"] = est_time
            entry["boulder_name"] = boulder_name
            entry["area"] = area
            entry["sub_area"] = sub_area
            entry["v_grade"] = v_grade
            entry["est_attempts"] = est_attempts
            entry["est_minutes"] = est_minutes
            entry["return_interest"] = return_interest
            entry["session_num"] = cnt+1
            entry["completed"] = completed
            entry["comment"] = first_comment

            db.insertRowDict(entry, 'boulders_tried', insertMany=False, replace=True, rid=0, debug=1)
            db.conn.commit()



if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()
