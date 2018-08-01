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

grade_dict = {
    "A8_f199f5feceae573aceb8547c167a30cd();":["9C","21"],
    "A8_e639e048efc86173b48366d80fd6d19d();":["9B+","20"],
    "A8_fa551bede6c5da30c5d8855695d6dace();":["9B","19"],
    "A8_03bfb95fc9a3fae4443bc09be895dec1();":["9B","19"],
    "A8_df251d57e562a0caff30c838d8669139();":["9A","17"],
    "A8_3c9afcb7e9aeee08d4e0259a9f8cd863();":["8C+","16"],
    "A8_8a2f2ba201c69c72f5fae6d5b490ca31();":["8C","15"],
    "A8_371ada172e6aca6d36030cff991c2110();":["8B+","14"],
    "A8_70ae3987db297649adfa22ec835bbef5();":["8B","13"],
    "A8_f94c1a7c1ade88cfeb2bd73ffa116d9f();":["8A+","12"],
    "A8_59b85d692c593f314ed49d15870ff8d2();":["8A","11"],
    "A8_ea3a0c3e0e84736e61d7b4ae4aa07145();":["7C+","10"],
    "A8_2d8a2dca8da8f8595bfafa25580f88c4();":["7C","9"],
    "A8_ebe1c7b6a0324f26fa1203e423827d73();":["7B+","8"],
    "A8_a3ef9ab41d342fca7c6d3bf3b2e01ca2();":["7B","7.5"],
    "A8_b68c76e55910e67faca8829b4700d2e1();":["7A+","7"],
    "A8_728a1685254b76fb0532dd2bd83fc670();":["7A","6"],
    "A8_323b60c5b47a45c73f666867fd27b319();":["6C+","5.5"],
    "A8_59ed716391fbf46727ad091b93b1b507();":["6C","5"],
    "A8_8e761f5120d8a81b268c721eb940f633();":["6B+","4.5"],
    "A8_4b0680d2e6545260c512c8424e7d0180();":["6B","4"],
    "A8_31d055ac30224e9cb434b74b6f77c9fe();":["6A+","3.5"],
    "A8_3cd6d35aa8f427f02d106c1c40969227();":["6A","3"],
    "A8_b69a020c915c748aba94ed6c86226541();":["5C","2"],
    "A8_10d988d607dfa42c867b638336965a99();":["5B","1"],
    "A8_217b0d256645bca88490d2f8257ffecd();":["5A","0"],
    "A8_027540acd8eb24681172603ebf359a5c();":["4C","0"],
    "A8_5e6e11644ad74bc7fa3554dc12d16d5d();":["4B","0"],
    "A8_f299aa555cd9014afd36ef6483f3aaf3();":["4A","0"],
    "A8_3440bab174d681fb370b859be0dc2f23();":["3C","0"],
    "A8_cc156b58d7e8ba3e3737d1927b74c135();":["3B","0"],
    "A8_d02544d610dbfd7bb34cb85ff612365c();":["3A","0"],
    "A8_56f871c6548ae32aaa78672c1996df7f();":["2","0"],
}


def initiate():
    url = "https://www.8a.nu/scorecard/andy-the-eagle-god/boulders/?AscentClass=0&AscentListTimeInterval=0&AscentListViewType=1&ListByAscDate=1&GID=4e15446b352fd1a7852da8accd84d52c"
    table_name = "boulders_completed"

    print "\tscraping 8a"
    process_8a(url, table_name)

    print "\tupdating csvs"
    process_completed()
    process_undone()
    process_returnInterest()

def process_8a(url, table_name):
    if table_name is not None:
        qry = "Truncate %s;" % table_name
        db.query(qry)
        db.conn.commit()

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, "lxml")

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
            euro_grade, v_grade = grade_dict.get(grade_JS)

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

            if recommended.find("img")["src"] == "/scorecard/images/UserRecommended_1.gif":
                recommended = "RECOMMENDED"
            else:
                recommended = None

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

            if table_name is not None:
                db.insertRowDict(entry, table_name, insertMany=False, replace=True, rid=0, debug=1)
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
