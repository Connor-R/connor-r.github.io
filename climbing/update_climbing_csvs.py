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
    process_undone()
    process_returnInterest()

def process_completed():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Date", "Boulder Name", "Area", "Sub Area", "V Grade", "Euro Grade", "8a.nu Points", "Flash", "Soft/Hard", "Stars (1-3)", "FA", "Recommended", "Estimated Attempts", "Estimated Minutes", "Estimated Session #", "Comment", "Updated"]
    append_csv.writerow(csv_header)

    qry = "SELECT * FROM boulders_completed ORDER BY ascent_date DESC;"

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","").replace("\n","  ") + '"'
        append_csv.writerow(row)
        

def process_undone():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_undone.csv"
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
    WHERE bc.ascent_date IS NULL
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


if __name__ == "__main__":     
    initiate()
