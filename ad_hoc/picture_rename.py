import os
import time
import imghdr
import pathlib
import csv
import datetime

base_path = "/Users/connorreed/Desktop/Images/iPhoto"
csv_path = os.getcwd()+"/picture_rename.csv"
csv_file = open(csv_path, "w")
append_csv = csv.writer(csv_file)
csv_header = ["parent_dir", "primary_bin", "media_type", "old_name", "created_year", "created_month", "created_day", "created_hour", "created_minute", "created_second", "parsed_year", "parsed_month", "parsed_day", "parsed_counter", "pre_name", "post_name", "descriptor", "day_match", "ext", "new_name", "old_path", "new_path"]
append_csv.writerow(csv_header)


def initiate():

    process_dir(base_path,0)

    # update_names() ###


def process_dir(path, lvl, parent_dir=''):
    # print(path)
    for i in range (0, len(os.listdir(path))):
        sub_dir = os.listdir(path)[i]

        ext = pathlib.Path(sub_dir).suffix

        if sub_dir in ('MiniHoop', '.DS_Store', 'Icon\r') or ext in ('.txt', '.pdf'):
            continue

        new_path = f"{path}/{sub_dir}"

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

    # print(filename)
    try:
        parsed_year = int(filename.split("|")[0].split("-")[-2])
        parsed_month = int(filename.split("|")[0].split("-")[-1])
        parsed_day = int(filename.split("|")[1].split("-")[0])
    except (ValueError, IndexError):
        parsed_year, parsed_month, parsed_day = [0,0,0]

    try:
        parsed_counter = int(filename.split(".")[0].split("-")[-1])
    except ValueError:
        parsed_counter = 0

    pre_name = ''
    if primary_bin != 'Other':
         pre_name += primary_bin
    if parsed_year != 0:
        pre_name += f"-{parsed_year:04d}-{parsed_month:02d}|{parsed_day:02d}"

    post_name = ''
    if parsed_counter != 0:
        post_name += str(parsed_counter)
    post_name += ext

    parsed_descriptor = filename.replace(pre_name,'').replace(post_name,'')
    if parsed_descriptor == '-': parsed_descriptor = ''
    if parsed_descriptor != '':
        if parsed_descriptor[-1] == "-": parsed_descriptor = parsed_descriptor[:-1]
        if parsed_descriptor[0] == "-": parsed_descriptor = parsed_descriptor[1:]

    if (parsed_descriptor != "" and parsed_descriptor is not None):
        descriptor_string = f"-{parsed_descriptor}"
    else:
        descriptor_string = ""
    new_ext = ext.lower()

    if parsed_year == created_year and parsed_month == created_month and parsed_day == created_day:
        day_match = True
    else:
        day_match = None

    if(0
        or (parsed_year < created_year and parsed_year != 0)
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

    new_path = path.replace(filename, "")+new_name


    csv_row = [parent_dir, primary_bin, media_type, filename, created_year, created_month, created_day, created_hour, created_minute, created_second, parsed_year, parsed_month, parsed_day, parsed_counter, pre_name, post_name, parsed_descriptor, descriptor_string , ext, new_name, path, new_path]
    append_csv.writerow(csv_row)


def update_names():
    

if __name__ == "__main__":     
    initiate()

