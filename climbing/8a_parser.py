from bs4 import BeautifulSoup, Comment
import time
from datetime import datetime
import csv
import os
from py_db import db
import argparse
import ast

db = db('personal')


base_path = os.getcwd()

grade_dict = {
    "8C+":"16", "8C":"15", "8B+":"14", "8B":"13", "8A+":"12", "8A":"11",
    "7C+":"10", "7C":"9", "7B+":"8", "7B":"7.5", "7A+":"7", "7A":"6",
    "6C+":"5.5", "6C":"5", "6B+":"4.5", "6B":"4", "6A+":"3.5", "6A":"3",
    "5C":"2", "5B":"1", "5A":"0", 
    "4C":"0", "4B":"0", "4A":"0", "3C":"0", "3B":"0", "3A":"0", "2":"0"}

def initiate():
    process_8a()

    process_completed()
    process_undone()
    process_returnInterest()

def process_8a():
    db.query("Truncate boulders_completed;")
    db.conn.commit()

    f = open("/Users/connordog/Dropbox/__TempFiles/Andy the Eagle God - Boulder Log-book 8a.nu.html","r")
    soup = BeautifulSoup(f.read(), "html.parser")
    f.close()

    ascent_data = []

    for comment in soup.find_all(string=lambda text:isinstance(text, Comment)):
        if comment.strip() == "Ascents":
            next_node = comment.next_sibling

            while next_node and next_node.next_sibling:
                ascent_data.append(next_node)
                next_node = next_node.next_sibling

                if not next_node.name and next_node.strip() == "List Options": break;

    for item in ascent_data:
        if str(item).strip() != "":
            ascents_info = item
            break

    ascents = ascents_info.find_all("tr")

    for i, ascent in enumerate(ascents):
        row = []

        ascent_cells = ascent.findAll("td")

        if len(ascent_cells) == 12:
            entry = {}
            boulder_name = ascent_cells[7]
            areas = ascent_cells[8].getText()
            ascent_date = ascent_cells[4]
            grade = ascent_cells[5]
            flash = ascent_cells[6]
            soft_hard_fa = ascent_cells[9].getText()
            stars = len(ascent_cells[11].getText())
            recommended = ascent_cells[3]
            comment = ascent_cells[10]

            for span_tag in boulder_name.find("span"):
                span_tag.replace_with("")
            boulder_name = boulder_name.getText().strip()
            if boulder_name[0] == "*":
                boulder_name = boulder_name[1:]

            # print str(i-1) + " of " + str(len(ascents)-2) + ": " + boulder_name

            try:
                area = areas.split("/")[0].strip()
                sub_area = areas.split("/")[1].strip()
            except IndexError:
                area = areas.strip()
                sub_area = areas.strip()

            for span_tag in ascent_date.find("span"):
                span_tag.replace_with("")
            ascent_date = ascent_date.getText().strip()
            ascent_date = datetime.strptime(ascent_date, "%y-%m-%d").date()

            for script_tag in grade.find("script"):
                script_tag.replace_with("")
            euro_grade = grade.getText().strip()
            v_grade = float(grade_dict.get(euro_grade))

            if flash.find("img")["src"] == "Andy%20the%20Eagle%20God%20-%20Boulder%20Log-book%208a.nu_files/979607b133a6622a1fc3443e564d9577.gif":
                flash = None
            else:
                flash = "TRUE"

            if "Soft" in soft_hard_fa:
                soft_hard = "soft"
            elif "Hard" in soft_hard_fa:
                soft_hard = "hard"
            else:
                soft_hard = ""

            if "FA" in soft_hard_fa:
                fa = "TRUE"
            else:
                fa = None

            if recommended.find("img")["src"] == "Andy%20the%20Eagle%20God%20-%20Boulder%20Log-book%208a.nu_files/UserRecommended_0.gif":
                recommended = None
            else:
                recommended = "TRUE"

            for span_tag in comment.find("span"):
                span_tag.replace_with("")
            comment = comment.getText().strip().replace("\n", "")

            if "Total_Duration" in comment:
                duration_dict = comment.split("Total_Duration")[1].split("}")[0].replace("=","").strip()+"}"
                duration_dict = ast.literal_eval(duration_dict)
                attempts = duration_dict.get('Attempts')
                minutes = duration_dict.get('Minutes')
                session = duration_dict.get('Sessions')
            else:
                attempts = None
                minutes = None
                session = None

            entry_columns = ["ascent_date", "boulder_name", "area", "sub_area", "v_grade", "euro_grade", "flash", "soft_hard", "stars", "fa", "recommended", "est_attempts", "est_minutes", "est_sessions", "comment"]
            row = [ascent_date, boulder_name, area, sub_area, v_grade, euro_grade, flash, soft_hard, stars, fa, recommended, attempts, minutes, session, comment]

            for j, item in enumerate(row):
                if type(item) in (str, unicode) and item != '':
                    row[j] = "".join([k if ord(k) < 128 else "" for k in item])

            entry = {} 
            for i,j in zip(entry_columns, row):
                entry[i] = j

            db.insertRowDict(entry, 'boulders_completed', insertMany=False, replace=True, rid=0, debug=1)
            db.conn.commit()


def process_completed():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Date", "Boulder Name", "Area", "Sub Area", "V Grade", "Euro Grade", "Flash", "Soft/Hard", "Stars (1-3)", "FA", "Recommended", "Estimated Attempts", "Estimated Minutes", "Estimated Session #", "Comment"]
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
