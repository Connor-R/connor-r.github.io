from py_db import db
import os
import csv

db = db('personal')


def initiate():
    #TODO UPDAE PATH
    base_path = "/Volumes/Daddy/NOT_ON_LAPTOP/TV_Shows/"

    for i in range (1, len(os.listdir(base_path))):
        entry = {}
        seasons_cnt = 0
        episodes_cnt = 0
        show_name = os.listdir(base_path)[i]
        if show_name[0] == 'z':
            show_name = show_name[1:]
        seasons_path = base_path+os.listdir(base_path)[i]
        seasons_count = len([name for name in os.listdir(seasons_path) if name.startswith(show_name)])
        seasons_cnt += seasons_count

        seasons_indices = []
        for j in range(1, len(os.listdir(seasons_path))):
            if show_name in os.listdir(seasons_path)[j]:
                seasons_indices.append(j)

        for k in seasons_indices:
            episodes_paths = base_path+os.listdir(base_path)[i]+'/'+os.listdir(seasons_path)[k]

            try:
                episodes_count = len([name for name in os.listdir(episodes_paths) if name.startswith(show_name)])
                episodes_cnt += episodes_count
            except OSError:
                seasons_cnt -= 1

        try:
            avg_eps = float(episodes_cnt)/float(seasons_cnt)
        except ZeroDivisionError:
            avg_eps = 0

        if show_name[0] == 'z':
            show_name = show_name[1:]

        entry['show_name'] = show_name.replace("_"," ")
        entry['seasons'] = seasons_cnt
        entry['episodes'] = episodes_cnt
        entry['episodes_per_season'] = avg_eps


        db.insertRowDict(entry, 'tv_show_data', insertMany=False, replace=True, rid=0, debug=1)
        db.conn.commit()


if __name__ == "__main__":     
    initiate()

