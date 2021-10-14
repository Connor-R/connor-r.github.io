import os
import time
import imghdr

base_path = "/Users/connorreed/Desktop/Images/iPhoto"

def initiate():

    process_dir(base_path)


def process_dir(path):
    # print(path)
    for i in range (0, len(os.listdir(path))):
        ext = os.listdir(path)[i]

        if ext in ('MiniHoop', '.DS_Store', 'Icon\r', 'Inherited') or ext[-4:] == '.pdf':
            continue

        new_path = path+'/'+ext

        # try:
        #     imghdr.what(new_path)
        #     process_file(ext, new_path)
        # except(IsADirectoryError):
        #     process_dir(new_path)


def process_file(ext, path):
    print("\t", ext)
    f = open(path)
    # print("\t\t\tcreated:",  time.ctime(os.path.getctime(path)) )


if __name__ == "__main__":     
    initiate()

