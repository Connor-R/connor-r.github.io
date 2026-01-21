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
    'Climbing', 'Multi-Sport Articles', 'Multi-Sport Sites', 'Soccer', 
    'Bash', 'General Programming', 'Git', 'LaTeX', 'Python', 'SQL', 'Ubuntu',
    'Bayesian Articles', 'Data Science Articles', 'Data Science Documentation', 
    'Decision Making and Psychology', 'Individual Profiles', 'Lifestyle and Self-Improvement',
    '2021','2022','BEST_OF'
    ]

for sport in ('MLB', 'NHL', 'NBA', 'NFL'):
    for desc in ('Coaching and Player Development', 'Draft and Prospects', 'Gameplay and Analysis', 'General Articles', 'General Sites', 'Metric Descriptions', 'Profiles', 'Sport Science'):
        cat_label = sport + ' ' + desc
        categories.append(cat_label)

for yr in range(2022, datetime.date.today().year+1):
    for mth in range(1,13):
        cat_label = str(yr)+'_'+str(mth).rjust(2, '0')
        categories.append(cat_label)
        print(cat_label)


csv_path = '/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_relevant_bookmarks.csv'
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

