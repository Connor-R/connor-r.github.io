from py_db import db
import bs4
import time
import datetime
import csv
import os

db = db('personal')

base_path = os.getcwd()

f = open('/Users/connordog/Dropbox/__TempFiles/bookmarks.html','r')
soup = bs4.BeautifulSoup(f.read(), 'html.parser')
f.close()

db.query("Truncate bookmarks;")
db.conn.commit()

categories = [
    'MLB Gameplay and Analysis', 'MLB General Articles', 
    'MLB Metric Descriptions', 'MLB Profiles', 'MLB General Sites', 
    'NHL Gameplay and Analysis', 'NHL General Articles', 
    'NHL Metric Descriptions', 'NHL Profiles','NBA General Sites',
    'NBA Gameplay and Analysis', 'NBA General Articles', 
    'NBA Metric Descriptions', 'NBA Profiles',
    'NFL Gameplay and Analysis', 'NFL General Articles', 'NFL General Sites', 
    'NFL Metric Descriptions', 'NFL Profiles',
    'NHL Rest', 'NHL Shot Quality', 'NHL General Sites', 
    'Multi-Sport Articles', 'Multi-Sport Sites', 'Soccer', 'Climbing',
    'Decision Making and Psychology', 'Lifestyle and Self-Improvement',
    'Bash', 'General Programming', 'Git', 'Python', 'SQL', 'Ubuntu',
    'Data Science Articles', 'Data Science Documentation', 'Bayesian Articles', 
    ]

csv_path = '/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/relevant_bookmarks.csv'
csv_file = open(csv_path, 'wb')
append_csv = csv.writer(csv_file)
csv_header = ['category', 'name', 'tags', 'link']
append_csv.writerow(csv_header)

for header in soup.findAll('h3'):
    if header.text not in (categories):
        # print 'nope', header.text
        pass
    else:
        print(header.text)
        category = header.text
        sib = header.find_next_sibling('dl')
        # raw_input(sib)

        for a in sib.find_all('a'):
            entry = {}
            # raw_input(a)
            _name = a.text.encode('utf-8')
            # add_date = a['add_date']
            # add_date = datetime.date.fromtimestamp(float(add_date))
            href = a['href']
            try:
                tags = a['tags']
            except KeyError:
                tags = ''

            append_csv.writerow(['"' + str(category) + '"', '"' + str(_name) + '"', '"' + str(tags) + '"', '"' + str(href) + '"'])

            entry['category_name'] = category
            entry['name'] = _name
            entry['tags'] = tags
            entry['link'] = href

            db.insertRowDict(entry, 'bookmarks', insertMany=False, replace=True, rid=0, debug=1)
            db.conn.commit()

