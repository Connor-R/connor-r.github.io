import time
from datetime import datetime
import csv
import os
from py_db import db
import argparse
import ast

db = db('personal')


base_path = os.getcwd()


def initiate():
    print "\tupdating csvs"
    process_completed()
    process_tried()
    process_returnInterest()
    process_breakdown()

def process_completed():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Date", "Boulder Name", "Area", "Sub Area", "V Grade", "Euro Grade", "8a.nu Points", "Flash", "Soft/Hard", "Stars (1-3)", "FA", "Recommended", "Estimated Final Time", "Estimated Attempts", "Estimated Minutes", "Estimated Session #", "Comment", "Updated"]
    append_csv.writerow(csv_header)

    qry = "SELECT * FROM boulders_completed ORDER BY ascent_date DESC;"

    res = db.query(qry)

    for row in res:
        upd = row[-1]
        comm = "".join(row[-2].split("}.")[1:]).replace("*Bounty Extra Soft*.","").strip()
        row = row[:-2]
        row = list(row)
        row.append(comm)
        row.append(upd)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","").replace("\n","  ") + '"'
        append_csv.writerow(row)
        

def process_tried():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_triedLog.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Estimated Date", "Estimated Time", "Boulder Name", "Area", "Sub Area", "V Grade", "Estimated Attempts", "Estimated Minutes", "Return Interest", "Session Number", "Comment"]
    append_csv.writerow(csv_header)
    
    qry = """SELECT 
    bt.est_date, bt.est_time,
    bt.boulder_name, bt.area, bt.sub_area,
    bt.v_grade, bt.est_attempts, bt.est_minutes, bt.return_interest, bt.session_num, bt.comment
    FROM boulders_tried bt
    LEFT JOIN boulders_completed bc USING (boulder_name, area)
    WHERE est_date > '0000-00-00'
    AND bt.completed = 'FALSE'
    ORDER BY est_date DESC, est_time DESC;"""

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","").replace("\n","  ") + '"'
        append_csv.writerow(row)


def process_returnInterest():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_returnInterest.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Estimated Date", "Estimated Time", "Boulder Name", "Area", "Sub Area", "V Grade", "Estimated Attempts", "Estimated Minutes", "Return Interest", "Comment"]
    append_csv.writerow(csv_header)
    
    qry = """SELECT 
    bt.est_date, bt.est_time,
    bt.boulder_name, bt.area, bt.sub_area,
    bt.v_grade, bt.est_attempts, bt.est_minutes, bt.return_interest, bt.comment
    FROM boulders_tried bt
    LEFT JOIN boulders_completed bc USING (boulder_name, area)
    JOIN (SELECT boulder_name, area, max(est_date) AS est_date FROM boulders_tried GROUP BY boulder_name, area) md USING (boulder_name, area, est_date)
    WHERE bc.ascent_date IS NULL
    ORDER BY est_date DESC, est_time DESC;"""

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","").replace("\n","  ") + '"'
        append_csv.writerow(row)


def process_breakdown():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_yearlyBreakdown.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Year", "8a Top 10 Points", "Climbing Days", "Completed Problems", "Tried Problems", "Completed per Day", "Tried per Day", "Success Rate"]
    append_csv.writerow(csv_header)
    
    qry = """SELECT 
    year AS 'Year', pts AS '8a Top 10 Points', 
    days AS 'Climbing Days', 
    completed_cnt AS 'Completed Problems', 
    tried_cnt AS 'Tried Problems', 
    ROUND(completed_cnt/days, 1) AS 'Completed per Day',
    ROUND(tried_cnt/days, 1) AS 'Tried per Day',
    ROUND(completed_cnt/tried_cnt,3) AS 'Success Rate'
    FROM(
        SELECT 'All Time' AS 'Year', SUM(8a_pts) AS 'pts'
        FROM(
            SELECT *
            FROM boulders_completed
            ORDER BY 8a_pts DESC
            LIMIT 10
        ) a
        UNION ALL
        SELECT 'Last Calendar Year' AS 'Year', SUM(8a_pts) AS 'pts'
        FROM(
            SELECT *
            FROM boulders_completed
            WHERE ascent_date > DATE_ADD(curdate(), INTERVAL -1 YEAR)
            ORDER BY 8a_pts DESC
            LIMIT 10
        ) b
        UNION ALL
        SELECT c_year AS 'Year', SUM(8a_pts) AS 'pts'
        FROM(
            SELECT YEAR(ascent_date) AS 'c_year', 8a_pts, @year, @auto,
            IF(@year=(@year:=YEAR(ascent_date)), @auto:=@auto+1, @auto:=1) indx 
            FROM boulders_completed, (SELECT @year:=0, @auto:=1) a
            ORDER BY YEAR(ascent_date), 8a_pts DESC
        ) c
        WHERE indx <= 10
        GROUP BY c_year DESC
    ) pts
    JOIN(
        SELECT 
        'All Time' AS 'Year', COUNT(DISTINCT est_date) AS days
        FROM boulders_tried
        WHERE YEAR (est_date) != 0
        UNION ALL
        SELECT 
        'Last Calendar Year' AS 'Year', COUNT(DISTINCT est_date) AS days
        FROM boulders_tried
        WHERE YEAR (est_date) != 0
        AND est_date > DATE_ADD(curdate(), INTERVAL -1 YEAR)
        UNION ALL
        SELECT 
        YEAR(est_date) AS 'Year', COUNT(DISTINCT est_date) AS days
        FROM boulders_tried
        WHERE YEAR (est_date) != 0
        GROUP BY YEAR(est_date)
        ORDER BY YEAR DESC
    ) days USING (YEAR)
    JOIN(
        SELECT 'All Time' AS 'Year', COUNT(*) AS completed_cnt
        FROM boulders_completed
        UNION ALL
        SELECT 'Last Calendar Year' AS 'Year', COUNT(*) AS completed_cnt
        FROM boulders_completed
        WHERE ascent_date > DATE_ADD(curdate(), INTERVAL -1 YEAR)
        UNION ALL
        SELECT 
        YEAR(ascent_date) AS 'Year', COUNT(*) AS completed_cnt
        FROM boulders_completed
        GROUP BY YEAR(ascent_date)
        ORDER BY YEAR DESC
    ) cnt USING (YEAR)
    JOIN(
        SELECT 'All Time' AS 'Year', COUNT(*) AS tried_cnt
        FROM boulders_tried
        UNION ALL
        SELECT 'Last Calendar Year' AS 'Year', COUNT(*) AS tried_cnt
        FROM boulders_tried
        WHERE est_date > DATE_ADD(curdate(), INTERVAL -1 YEAR)
        UNION ALL
        SELECT 
        YEAR(est_date) AS 'Year', COUNT(*) AS tried_cnt
        FROM boulders_tried
        GROUP BY YEAR(est_date)
        ORDER BY YEAR DESC
    ) tried USING (YEAR)
    ORDER BY YEAR='All Time' DESC, YEAR='current' DESC, YEAR DESC;"""

    res = db.query(qry)

    for row in res:
        row = list(row)
        append_csv.writerow(row)


if __name__ == "__main__":     
    initiate()
