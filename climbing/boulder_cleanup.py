from py_db import db
import argparse
from time import time

db = db('personal')


def initiate():
    start_time = time()

    print "\nupdating session # and final_time on all boulders"
    update_session_details()
    print '\tdone'

    print "\nupdating total attempts/minutes/sessions and flash flag on completed boulders"
    update_completed_boulders()
    print '\tdone'

    print "\nsetting invalid flags to NULL"
    update_flags()
    print '\tdone'

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nboulder_cleanup.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def update_session_details():
    db.query("SET @cnt:=0;")
    db.query("SET @prob:='';")

    query = """SELECT a.session_date
    , a.session_start
    , a.boulder_name
    , a.area
    , a.sub_area
    , IF(a.session_start IS NOT NULL
        , SEC_TO_TIME(TIME_TO_SEC(a.session_start) + a.session_minutes*60)
        , NULL
    ) AS final_time
    , IF(@prob = CONCAT(boulder_name,'_',area), @cnt:=@cnt+1, IF(session_date='0000-00-00', @cnt:=0, @cnt:=1)) AS session_num
    , @prob := CONCAT(boulder_name,'_',area) AS prob_set
    FROM(
        SELECT *
        FROM boulder_problems bp
        ORDER BY area, boulder_name, session_date
    ) a
    ;"""

    res = db.query(query)

    for row in res:
        session_date, session_start, boulder_name, area, sub_area, final_time, session_num, foo = row

        for cat in ('final_time', 'session_num'):
            if cat == 'final_time':
                val = final_time
            elif cat == 'session_num':
                val = session_num

            if (cat != 'final_time' or session_date is not None):
                update_qry = """UPDATE boulder_problems
                SET %s = "%s"
                WHERE 1
                    AND IF("%s" = "None", 1, session_date = "%s")
                    AND session_start = "%s"
                    AND boulder_name = "%s"
                    AND area = "%s"
                    AND sub_area = "%s"
                ;"""

                update_qry = update_qry % (cat, val, session_date, session_date, session_start, boulder_name, area, sub_area)
                db.query(update_qry)
                db.conn.commit()

def update_completed_boulders():
    categories = ['total_attempts', 'total_minutes', 'total_sessions', 'details', 'flash']
    for reset_val in categories:
        db.query("UPDATE boulder_problems SET %s = NULL" % (reset_val))
        db.conn.commit()


    query = """SELECT bp.session_date
    , bp.session_start
    , bp.boulder_name
    , bp.area
    , bp.sub_area
    , bp.completed
    , if(bp.completed='COMPLETED' AND bpc.total_attempts=1, 'FLASH', NULL) AS FLASH
    , bpc.total_attempts
    , bpc.total_minutes
    , bpc.total_sessions
    , CONCAT(
        IF(bp.completed = 'COMPLETED'
            , CONCAT(
                'DESCRIPTORS:'
                , IF(bp.athletic IS NULL, '', CONCAT(' ', bp.athletic, ' |'))
                , IF(bp.cruxy IS NULL, '', CONCAT(' ', bp.cruxy, ' |'))
                , IF(bp.slopey IS NULL, '', CONCAT(' ', bp.slopey, ' |'))
                , IF(bp.crimpy IS NULL, '', CONCAT(' ', bp.crimpy, ' |'))
                , IF(bp.sharp IS NULL, '', CONCAT(' ', bp.sharp, ' |'))
                , IF(bp.technical IS NULL, '', CONCAT(' ', bp.technical, ' |'))
                , IF(bp.power IS NULL, '', CONCAT(' ', bp.power, ' |'))
                , IF(bp.endurance IS NULL, '', CONCAT(' ', bp.endurance, ' |'))
                , IF(bp.overhang IS NULL, '', CONCAT(' ', bp.overhang, ' |'))
                , IF(bp.vertical IS NULL, '', CONCAT(' ', bp.vertical, ' |'))
                , IF(bp.slab IS NULL, '', CONCAT(' ', bp.slab, ' |'))
                , IF(bp.scary IS NULL, '', CONCAT(' ', bp.scary, ' |'))
                , '\n\n'
            )
            , ''
        )
        , bpc.total_attempts
        , ' Attempts | '
        , bpc.total_minutes
        , ' Minutes | '
        , bpc.total_sessions
        , ' Sessions\n\n'
        , bpc.details
    ) AS details
    FROM boulder_problems bp
    JOIN(
        SELECT boulder_name
        , area
        , sub_area
        , MAX(session_num) AS last_session
        , SUM(session_attempts) AS total_attempts
        , SUM(session_minutes) AS total_minutes
        , COUNT(DISTINCT IF(session_num >= 1, CONCAT(session_date,session_start), NULL)) AS total_sessions
        , GROUP_CONCAT(
            CONCAT('Session #'
                , session_num
                , ' on '
                , session_date
                , ' at '
                , session_start
                , '. '
                , session_attempts
                , ' attempts, over '
                , session_minutes
                , ' minutes. \n\t'
                , IFNULL(comment, '')
            )
        ORDER BY session_date, session_start SEPARATOR '\n\n') AS details
        FROM boulder_problems bp
        GROUP BY boulder_name, area, sub_area
    ) bpc USING (boulder_name, area, sub_area)
    WHERE 1
        AND (bp.completed = 'COMPLETED' OR (bp.session_num = bpc.last_session AND bp.session_num > 0))
    ;"""

    res = db.query(query)

    for row in res:
        session_date, session_start, boulder_name, area, sub_area, completed, flash, total_attempts, total_minutes, total_sessions, details = row

        for cat in categories:
            if cat == 'total_attempts':
                val = total_attempts
            elif cat == 'total_minutes':
                val = total_minutes
            elif cat == 'total_sessions':
                val = total_sessions
            elif cat == 'details':
                val = details.replace('"', '\\"')
            elif cat == 'flash':
                val = flash

            update_qry = """UPDATE boulder_problems
            SET %s = IF("%s" = "None", NULL, "%s")
            WHERE 1
                AND IF("%s" = "None", 1, session_date = "%s")
                AND session_start = "%s"
                AND boulder_name = "%s"
                AND area = "%s"
                AND sub_area = "%s"
            ;"""

            update_qry = update_qry % (cat, val, val, session_date, session_date, session_start, boulder_name, area, sub_area)
            db.query(update_qry)
            db.conn.commit()

def update_flags():
    flags = {'completed': []
        , 'return_interest': ['range', 1, 5]
        , 'stars': ['range', 20, 80]
        , 'soft_hard': ['list', 'SOFT', 'HARD', 'BOUNTY EXTRA SOFT']
        , 'flash': []
        , 'athletic': []
        , 'cruxy': []
        , 'slopey': []
        , 'crimpy': []
        , 'sharp': []
        , 'technical': []
        , 'power': []
        , 'endurance': []
        , 'overhang': []
        , 'vertical': []
        , 'slab': []
        , 'roof': []
        , 'scary': []
    }

    for flag, vals in flags.items():
        print '\tchecking', flag
        qry_add = ''
        if vals == []:
            qry_add = "\nAND %s != '%s'" % (flag, flag)
        elif vals[0] == 'range':
            qry_add = "\nAND (%s < %s OR %s > %s)" % (flag, vals[1], flag, vals[2])
        elif vals[0] == 'list':
            for i in vals[1:]:
                qry_add += "\nAND %s != '%s'" % (flag, i)

        qry = """SELECT session_num
        , session_start
        , boulder_name
        , area
        , %s
        FROM boulder_problems
        WHERE 1
            AND %s IS NOT NULL%s
        ;"""

        query = qry % (flag, flag, qry_add)

        res = db.query(query)

        if res != ():
            for row in res:
                session_num, session_start, boulder_name, area, old_val = row

                # print '\t\t\tupdating %s for %s (%s) session #%s starting at %s from %s to NULL' % (flag, boulder_name, area, session_num, session_start, old_val)

                update_qry = """UPDATE boulder_problems
                SET %s = NULL
                WHERE 1
                    AND session_num = '%s'
                    AND session_start = '%s'
                    AND boulder_name = '%s'
                    AND area = '%s'
                ;"""

                update_qry = update_qry % (flag, session_num, session_start, boulder_name, area)
                db.query(update_qry)
                db.conn.commit()

        # print '\t\tdone'


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()
