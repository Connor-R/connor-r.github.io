from py_db import db
import os
import csv
import argparse
from time import time

db = db('personal')



def initiate():
    start_time = time()

    print "\nupdating tv show grades"
    update_grades()

    print "\nupdating tv show rankings"
    update_rankings()

    print "\nexporting tv shows to csv"
    export_to_csv()


    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nprocessing_tv_shows.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)

def update_grades():
    qry = "SELECT * FROM tv_show_grades;"
    res = db.query(qry)

    for row in res:
        show_name, genre, episode_length, peak, consistency, adj, runtime, grade = row

        grade = (float(peak)*3 + float(consistency)*2)/5 + max(adj,0)

        entry = {"show_name":show_name, "genre":genre, "episode_length":episode_length, "peak_grade":peak, "consistency_grade":consistency, "adjustment":adj, "approx_runtime_hours":runtime, "overall_grade":grade}

        db.insertRowDict(entry, 'tv_show_grades', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()



def update_rankings():
    qry = """SELECT * 
    FROM tv_show_data;"""

    res = db.query(qry)

    for row in res:
        entry = {}
        show_name, seasons, episodes, eps_per_season = row

        row_qry = """SELECT 
        show_name, genre, episode_length, peak_grade, consistency_grade, adjustment, overall_grade
        FROM tv_show_grades
        WHERE show_name = "%s";"""

        row_query = row_qry % (show_name)

        try:
            foo, genre, ep_len, peak, consistency, adj, grade = db.query(row_query)[0]
            runtime_hrs = float(episodes*ep_len)/60.0
        except (IndexError, TypeError):
            update_entry = {"show_name":show_name}
            db.insertRowDict(update_entry, 'tv_show_grades', insertMany=False, replace=True, rid=0, debug=1)
            db.conn.commit()
            ep_len, genre, peak, consistency, adj, runtime_hrs, grade = 0,0,0,0,0,0,0

        entry['show_name'] = show_name
        entry['genre'] = genre
        entry['episode_length'] = ep_len
        entry['peak_grade'] = peak
        entry['consistency_grade'] = consistency
        entry['adjustment'] = adj
        entry['approx_runtime_hours'] = runtime_hrs
        entry['overall_grade'] = grade

        db.insertRowDict(entry, 'tv_show_grades', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()



def export_to_csv():


    qry = """SELECT
    show_name, genre, seasons, episodes, 
    episode_length, episodes_per_season, approx_runtime_hours,
    peak_grade, consistency_grade, adjustment, overall_grade
    FROM (SELECT SHOW_name FROM tv_show_grades UNION SELECT show_name FROM tv_show_data) a
    LEFT JOIN tv_show_grades USING (show_name)
    LEFT JOIN tv_show_data USING (show_name)
    ORDER BY overall_grade DESC;"""

    res = db.query(qry)

    csv_title = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_tvShows.csv"
    csv_file = open(csv_title, "wb")
    append_csv = csv.writer(csv_file)
    headers = ['show_name', 'genre', 'estimated_seasons', 'estimated_episodes', 'episode_length', 'episodes_per_season', 'approx_runtime_hours', 'peak_grade', 'consistency_grade', 'adjustment', 'overall_grade']
    append_csv.writerow(headers)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","").replace("\n","  ") + '"'
        append_csv.writerow(row)


if __name__ == "__main__":     
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    
    initiate()
