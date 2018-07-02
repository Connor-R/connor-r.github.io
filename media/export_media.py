from py_db import db
import os
import csv
import argparse
from time import time

db = db('personal')



def initiate():
    start_time = time()

    print "\nexporting books to csv"
    export_to_csv('books')

    print "\nexporting movies to csv"
    export_to_csv('movies')

    print "\nupdating podcast grades"
    update_podcast_grades()

    print "\nexporting podcasts to csv"
    export_to_csv('podcasts')

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nexport_media.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)

def update_podcast_grades():
    qry = "SELECT * FROM podcasts;"
    res = db.query(qry)

    for row in res:
        podcast_name, genre, peak, consistency, adj, overall = row

        grade = (float(peak)*3 + float(consistency)*2)/5 + max(adj,0)

        entry = {"podcast_name":podcast_name, "genre":genre, "peak_grade":peak, "consistency_grade":consistency, "adjustment":adj, "overall_grade":grade}

        db.insertRowDict(entry, 'podcasts', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()

def export_to_csv(table_name):


    col_names_qry = """SELECT `COLUMN_NAME` 
    FROM `INFORMATION_SCHEMA`.`COLUMNS` 
    WHERE `TABLE_SCHEMA`='personal' 
    AND `TABLE_NAME`='%s';"""
    col_names_query = col_names_qry % (table_name)

    col_names = db.query(col_names_query)

    columns = []
    for col_name in col_names:
        columns.append(col_name[0])

    csv_title = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/%s.csv" % (table_name)
    csv_file = open(csv_title, "wb")
    append_csv = csv.writer(csv_file)
    append_csv.writerow(columns)

    qry = "SELECT * FROM %s;" % table_name

    res = db.query(qry)

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
