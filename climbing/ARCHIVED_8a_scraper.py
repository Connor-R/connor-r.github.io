from mechanize import Browser
import requests
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

br = Browser()
br.set_handle_robots(False)
br.set_handle_referer(False)
br.set_handle_refresh(False)
br.addheaders = [("User-agent", "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"),
    ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
    ("Keep-Alive","115"),
    ("Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7")
    ]

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

def initiate():
    url = "https://www.8a.nu/scorecard/andy-the-eagle-god/boulders/?AscentClass=0&AscentListTimeInterval=0&AscentListViewType=1&ListByAscDate=1&GID=4e15446b352fd1a7852da8accd84d52c"
    table_name = "boulders_completed"

    check_for_updates()
            
    print "\n\tscraping 8a"
    process_8a(url, table_name)

    check_for_un_updated()

def process_8a(url, table_name):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, "lxml")
    print "\t\tgrabbed html"

    if table_name != None:
        qry = "UPDATE %s SET updated = 'FALSE';" % table_name
        db.query(qry)
        db.conn.commit()

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

        if len(ascent_cells) == 9:
            entry = {}
            ascent_date = ascent_cells[0]
            grade = ascent_cells[1]
            flash = ascent_cells[2]
            boulder_name = ascent_cells[3]
            recommended = ascent_cells[4]
            areas = ascent_cells[5].getText()
            soft_hard_fa = ascent_cells[6].getText()
            comment = ascent_cells[7]
            stars = len(ascent_cells[8].getText())

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

            grade_JS = grade.getText()
            grade_qry = """SELECT font, hueco, 8a_points
            FROM boulders_grades
            WHERE 8a_javascript = "%s";"""
            grade_query = grade_qry % (grade_JS)
            euro_grade, v_grade, pts_base = db.query(grade_query)[0]

            if flash.find("img")["src"] == "/scorecard/images/56f871c6548ae32aaa78672c1996df7f.gif":
                flash = "FLASH"
            elif flash.find("img")["src"] == "/scorecard/images/e37046f07ac72e84f91d7f29f8455b58.gif":
                flash = "ONSIGHT"
            else:
                flash = None

            if "Soft" in soft_hard_fa:
                soft_hard = "SOFT"
            elif "Hard" in soft_hard_fa:
                soft_hard = "HARD"
            else:
                soft_hard = ""

            if "FA" in soft_hard_fa:
                fa = "FA"
            else:
                fa = None

            if flash == "FLASH":
                pts = pts_base+50
            elif flash == "ONSIGHT":
                pts = pts_base+100
            else:
                pts = pts_base

            if fa == "FA":
                pts += 20

            if recommended.find("img")["src"] == "/scorecard/images/UserRecommended_1.gif":
                recommended = "RECOMMENDED"
            else:
                recommended = None

            for span_tag in comment.find("span"):
                span_tag.replace_with("")
            comment = comment.getText().strip().replace("\n", "")

            if "Total_Duration" in comment:
                duration_dict = comment.split("Total_Duration")[1].split("}")[0].replace("=","").strip()+"}"
                try:
                    duration_dict = ast.literal_eval(duration_dict)
                    final_time = duration_dict.get('Final Time')
                    attempts = duration_dict.get('Attempts')
                    minutes = duration_dict.get('Minutes')
                    session = duration_dict.get('Sessions')
                except SyntaxError:
                    print '\nERROR:', boulder_name, '\n', duration_dict, '\n----------------\n'
                    final_time = None
                    attempts = 0
                    minutes = 0
                    session = 0
            else:
                final_time = None
                attempts = None
                minutes = None
                session = None

            if "*Bounty Extra Soft*." in comment:
                soft_hard = "BOUNTY EXTRA SOFT"


            if attempts == 2:
                pts += 2

            updated = "TRUE"

            entry_columns = ["ascent_date", "boulder_name", "area", "sub_area", "v_grade", "euro_grade", "8a_pts", "flash", "soft_hard", "stars", "fa", "recommended", "final_time", "est_attempts", "est_minutes", "est_sessions", "comment", "updated"]
            row = [ascent_date, boulder_name, area, sub_area, v_grade, euro_grade, pts, flash, soft_hard, stars, fa, recommended, final_time, attempts, minutes, session, comment, updated]

            for j, item in enumerate(row):
                if type(item) in (str, unicode) and item != '':
                    row[j] = "".join([k if ord(k) < 128 else "" for k in item])

            entry = {} 
            for i,j in zip(entry_columns, row):
                entry[i] = j

            if table_name is not None:
                db.insertRowDict(entry, table_name, insertMany=False, replace=True, rid=0, debug=1)
                db.conn.commit()


def check_for_updates(): ##### change me
    print "\n\tchecking for boulders to update"
    update_qry = """SELECT 
    euro_grade, soft_hard, flash, boulder_name, area, sub_area, fa, est_attempts, comment, stars, ascent_date, recommended
    FROM boulders_completed
    WHERE updated = "FALSE";"""

    update_res = db.query(update_qry)

    if update_res == ():
        print "\t\tNo boulders to update!"
    else:
        for i, row in enumerate(update_res):
            print "\n\nUpdate %s of %s" % (i+1, len(update_res))

            keys = ["grade", "soft_hard", "style", "name", "area", "sub area", "FA", "2ndGo", "comment", "stars", "date", "recommended"]

            _grade2, soft_hard, _flash, _name, _area, _subarea, _fa, attempts, _comment, _stars, _date, _recommended = row
            
            if _flash is None:
                _flash = "Redpoint"

            if attempts == 2:
                go2 = "Second GO"
            else:
                go2 = "None"

            vals = [_grade2, soft_hard, _flash, _name, _area, _subarea, go2, _fa, _comment, _stars, _date, _recommended]
            for k, v in zip(keys, vals):
                print ("\t"+k+":"), "\n", v

            # if (((i+1)%3 == 0) or ((i+1) == len(update_res))):
            raw_input("\n\nGo to 8a.nu to update!\n\n")

def check_for_un_updated():
    print "\n\tchecking for boulders to delete (or add)"
    qry = """SELECT ascent_date, boulder_name, area, sub_area, v_grade, euro_grade, updated
    FROM boulders_completed
    WHERE updated = 'FALSE';"""

    res = db.query(qry)

    if res == ():
        print "\t\tNo boulders to update!"
    else:
        for i, row in enumerate(res):
            print "\nUpdate %s of %s" % (i+1, len(res))

            keys = ["date", "name", "area", "sub area", "hueco", "euro", "updated"]

            for k, v in zip(keys, row):
                print ("\t"+k+":"), "\n", v
        raw_input("\n\nUpdate these problems in the database!\n\n")

if __name__ == "__main__":     
    initiate()
