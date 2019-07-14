from py_db import db
import os
import csv
import argparse
from time import time

db = db('personal')



def initiate():
    start_time = time()

    for media_type in ('books', 'movies', 'podcasts', 'tv_show_grades'):
        print "\t", media_type
        update_grades(media_type)
        export_to_csv(media_type)

    print "\tquotes"
    export_to_csv('quotes')

    end_time = time()
    elapsed_time = float(end_time - start_time)
    print "\n\nexport_media.py"
    print "time elapsed (in seconds): " + str(elapsed_time)
    print "time elapsed (in minutes): " + str(elapsed_time/60.0)


def update_grades(media_type):
    print("\t\tgrades")
    def ifnull(div_val, ovr_val, weight, val):
        if val is None:
            return div_val, ovr_val, val
        else:
            div_val += weight
            ovr_val += weight*val
            return float(div_val), float(ovr_val), val

    qry = "SELECT * FROM %s;" % (media_type)
    res = db.query(qry)

    for row in res:
        div_val = 0
        ovr_val = 0

        name = row[0]

        adjustment = row[len(row)-2]

        # peak, consistency, premise get 1.0 weight, everything else gets 0.5
        feature_cnt = 3
        attribute_cnt = 6
        for feature in range(0, feature_cnt):
            div_val, ovr_val, feat_val = ifnull(div_val, ovr_val, 1, row[len(row)-2-attribute_cnt-feature_cnt+feature])

        for attribute in range(feature_cnt, feature_cnt+attribute_cnt):
            div_val, ovr_val, att_val = ifnull(div_val, ovr_val, 0.5, row[len(row)-2-attribute_cnt-feature_cnt+attribute])

        grade = float(ovr_val) / float(max(div_val, 1.0))

        if adjustment is not None:
            grade = grade + float(adjustment)

        row = list(row)
        row[-1] = grade
        row = tuple(row)

        col_names_qry = """SELECT `COLUMN_NAME` 
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_SCHEMA`='personal' 
        AND `TABLE_NAME`="%s";""" % (media_type)

        col_names = db.query(col_names_qry)

        keys = []
        for c in col_names:
            keys.append(c[0])

        db.insertRow(keys=keys, values=row, table=media_type, insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()


def export_to_csv(table_name):
    print "\t\texporting", table_name, "to csv"

    if table_name == "tv_show_grades":
        update_tv_show_rankings()
        export_tv_show_csv()

    else:
        col_names_qry = """SELECT `COLUMN_NAME` 
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_SCHEMA`='personal' 
        AND `TABLE_NAME`='%s';"""
        col_names_query = col_names_qry % (table_name)

        col_names = db.query(col_names_query)

        columns = []
        for col_name in col_names:
            columns.append(col_name[0])

        csv_title = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_%s.csv" % (table_name)
        csv_file = open(csv_title, "wb")
        append_csv = csv.writer(csv_file)
        append_csv.writerow(columns)

        qry = "SELECT * FROM %s ORDER BY 1;" % table_name

        res = db.query(qry)

        for row in res:
            row = list(row)
            for i, val in enumerate(row):
                if type(val) in (str,):
                    row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","").replace("\n","  ") + '"'
            append_csv.writerow(row)


def update_tv_show_rankings():
    qry = """SELECT * 
    FROM tv_show_data;"""

    res = db.query(qry)

    for row in res:
        entry = {}
        name, seasons, episodes, eps_per_season = row

        row_qry = """SELECT *
        FROM tv_show_grades
        WHERE name = "%s";"""

        row_query = row_qry % (name)

        try:
            foo, genre, ep_len, runtime_hrs, peak, consistency, premise, plot, information_gain, fx, wit, lng, timelsns, adj, grade = db.query(row_query)[0]
            runtime_hrs = float(episodes*ep_len)/60.0
        except (IndexError, TypeError):
            update_entry = {"name":name}
            db.insertRowDict(update_entry, 'tv_show_grades', insertMany=False, replace=True, rid=0, debug=1)
            db.conn.commit()
            genre, ep_len, runtime_hrs, peak, consistency, premise, plot, information_gain, fx, wit, lng, timelsns, adj, grade = None,None,None,None,None,None,None,None,None,None,None,None,None,None

        entry['name'] = name
        entry['genre'] = genre
        entry['episode_length'] = ep_len
        entry['approx_runtime_hours'] = runtime_hrs
        entry['peak'] = peak
        entry['consistency'] = consistency
        entry['premise'] = premise
        entry['plot'] = plot
        entry['information_gain'] = information_gain
        entry['desired_effects'] = fx
        entry['wit'] = wit
        entry['length'] = lng
        entry['timelessness'] = timelsns
        entry['adjustment'] = adj
        entry['overall_grade'] = grade

        db.insertRowDict(entry, 'tv_show_grades', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()


def export_tv_show_csv():

    qry = """SELECT
    name, genre, seasons, episodes, 
    episode_length, episodes_per_season, approx_runtime_hours,
    peak, consistency, premise, plot, information_gain, desired_effects, wit, length, timelessness, adjustment, overall_grade
    FROM (SELECT name FROM tv_show_grades UNION SELECT name FROM tv_show_data) a
    LEFT JOIN tv_show_grades USING (name)
    LEFT JOIN tv_show_data USING (name)
    ORDER BY overall_grade DESC;"""

    res = db.query(qry)

    csv_title = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_tvShows.csv"
    csv_file = open(csv_title, "wb")
    append_csv = csv.writer(csv_file)
    headers = ['name', 'genre', 'seasons', 'episodes', 'episode_length', 'episodes_per_season', 'approx_runtime_hours', 'peak', 'consistency', 'premise', 'plot', 'information_gain', 'desired_effects', 'wit', 'length', 'timelessness', 'adjustment', 'overall_grade']
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
