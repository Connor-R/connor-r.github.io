from bs4 import BeautifulSoup, Comment
import time
from datetime import datetime
import csv
import os

base_path = os.getcwd()

f = open("8a.html","r")
soup = BeautifulSoup(f.read(), "html.parser")
f.close()

csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv"
csv_file = open(csv_path, "wb")
append_csv = csv.writer(csv_file)
csv_header = ["Date", "Boulder Name", "Area", "Sub Area", "Grade", "Euro Grade", "Flash", "Soft/Hard", "Stars (1-3)", "FA", "Recommended", "Attempts", "Duration", "Session #", "Comment"]
append_csv.writerow(csv_header)

ascent_data = []

grade_dict = {
    "8C+":"V16", "8C":"V15", "8B+":"V14", "8B":"V13", "8A+":"V12", "8A":"V11",
    "7C+":"V10", "7C":"V9", "7B+":"V8", "7B":"V7/8", "7A+":"V7", "7A":"V6",
    "6C+":"V5/6", "6C":"V5", "6B+":"V4/5", "6B":"V4", "6A+":"V3/4", "6A":"V3",
    "5C":"V2", "5B":"V1", "5A":"V0", 
    "4C":"V0-", "4B":"V0-", "4A":"V0-", "3C":"V0-", "3B":"V0-", "3A":"V0-", "2":"V0-"}

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
        boulder_name = ascent_cells[7]
        areas = ascent_cells[8].getText()
        ascent_date = ascent_cells[4]
        grade = ascent_cells[5]
        flash = ascent_cells[6]
        soft_hard_fa = ascent_cells[9].getText()
        stars = ascent_cells[11].getText()
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
        grade = grade_dict.get(euro_grade)

        if flash.find("img")["src"] == "Andy%20the%20Eagle%20God%20-%20Boulder%20Log-book%208a.nu_files/979607b133a6622a1fc3443e564d9577.gif":
            flash = None
        else:
            flash = True

        if "Soft" in soft_hard_fa:
            soft_hard = "soft"
        elif "Hard" in soft_hard_fa:
            soft_hard = "hard"
        else:
            soft_hard = ""

        if "FA" in soft_hard_fa:
            fa = True
        else:
            fa = None

        if recommended.find("img")["src"] == "Andy%20the%20Eagle%20God%20-%20Boulder%20Log-book%208a.nu_files/UserRecommended_0.gif":
            recommended = None
        else:
            recommended = True

        for span_tag in comment.find("span"):
            span_tag.replace_with("")
        comment = '"' + comment.getText().strip().replace("\n", "") + '"'

        attempts = None
        duration = None
        session = None

        row = [ascent_date, boulder_name, area, sub_area, grade, euro_grade, flash, soft_hard, stars, fa, recommended, attempts, duration, session, comment]

        for j, item in enumerate(row):
            if type(item) in (str, unicode):
                row[j] = "".join([k if ord(k) < 128 else "" for k in item])
        
        append_csv.writerow(row)




