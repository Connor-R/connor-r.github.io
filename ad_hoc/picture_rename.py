import os
import time
import imghdr
import pathlib
import csv
import datetime

base_path = "/Users/connorreed/Desktop/Images/iPhoto"
csv_path = "/Users/connorreed/Desktop/picture_rename.csv"
csv_file = open(csv_path, "w")
append_csv = csv.writer(csv_file)
csv_header = ["parent_dir", "primary_bin", "media_type", "old_name", "created_year", "created_month", "created_day", "created_hour", "created_minute", "created_second", "parsed_year", "parsed_month", "parsed_day", "descriptor", "day_match", "ext", "new_name"]
append_csv.writerow(csv_header)


def initiate():

    process_dir(base_path,0)


def process_dir(path, lvl, parent_dir=''):
    # print(path)
    for i in range (0, len(os.listdir(path))):
        sub_dir = os.listdir(path)[i]

        ext = pathlib.Path(sub_dir).suffix

        if sub_dir in ('MiniHoop', '.DS_Store', 'Icon\r') or ext in ('.txt', '.pdf'):
            continue

        new_path = path+'/'+sub_dir

        if ext == '':
            stt = ''
            for j in range(0,lvl):
                stt += '    '
            stt += sub_dir
            print(f'DIR: {stt}')
            # input(f'DIR: {stt}')
            process_dir(new_path, lvl+1, sub_dir)
        else:
            imghdr.what(new_path)
            process_file(sub_dir, new_path, lvl+1, ext, parent_dir)

            


def process_file(filename, path, lvl, ext, parent_dir=''):
    # pass
    stt = ''
    for j in range(0,lvl):
        stt += '\t'
    stt += parent_dir+'/'+filename
    # print(f'FILE: {stt}')

    if ext.lower() in ('.jpg', '.png', '.jpeg'): #8519 pictures
        media_type = 'Picture'
    elif ext.lower() in ('.mov', '.mp4', '.avi', '.m4v'): #1938 movies
        media_type = 'Video'
    else:
        media_type = 'Unknown'
        print(ext)

    primary_bin = parent_dir.replace('-Pictures','').replace('-Videos','')

    # https://stackoverflow.com/questions/946967/get-file-creation-time-with-python-on-mac
    time_created = datetime.datetime.strptime(time.ctime(os.stat(path).st_birthtime), "%a %b %d %H:%M:%S %Y")
    created_year = time_created.year
    created_month = time_created.month
    created_day = time_created.day
    created_hour = time_created.hour
    created_minute = time_created.minute
    created_second = time_created.second

    parsed_year = 99999 ###
    parsed_month = 0 ###
    parsed_day = 0 ###
    parsed_counter = 0 ###
    parsed_descriptor = 0 ###

    descriptor_string = f"-{parsed_descriptor}" if parsed_descriptor is not None else ""
    new_ext = ext.lower()

    if parsed_year == created_year and parsed_month == created_month and parsed_day == created_day:
        day_match = True
    else:
        day_match = None

    if(0
        or parsed_year < created_year
        or (parsed_year == created_year and parsed_month < created_month) 
        or (parsed_year == created_year and parsed_month == created_month and parsed_day < created_day)
    ):
        decided_year = parsed_year
        decided_month = parsed_month
        decided_day = parsed_day
        decided_hour = 0
        decided_min = 0
        decided_sec = parsed_counter
    else:
        decided_year = created_year
        decided_month = created_month
        decided_day = created_day
        decided_hour = created_hour
        decided_min = created_minute
        decided_sec = created_second

    new_name = f"{primary_bin}-{decided_year:04d}-{decided_month:02d}-{decided_day:02d} {decided_hour:02d}.{decided_min:02d}.{decided_sec:02d}{descriptor_string}{new_ext}"


    csv_row = [parent_dir, primary_bin, media_type, filename, created_year, created_month, created_day, created_hour, created_minute, created_second, parsed_year, parsed_month, parsed_day, parsed_descriptor, day_match, ext, new_name]
    append_csv.writerow(csv_row)


if __name__ == "__main__":     
    initiate()

