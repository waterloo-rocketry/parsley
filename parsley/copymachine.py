import shutil
import os
import sys
import configparser

# can be edited to add files not meant to be copied
# make configuring thingy work idk
config = configparser.ConfigParser()

if os.path.exists("configs.ini"):
    config.read("configs.ini")
    excluded_files = config.get('exclude', 'excluded').split()
else:
    # assumes this list
    excluded_files = ["can_common.c", "can_common.h", "message.types.h"]


def copy_directory(source_dir, destination_dir, excluded_files):
    # check if the destination directory exists
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)

    # go through each file
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)

        # recursive
        if os.path.isdir(source_file):
            copy_directory(source_file, destination_file, excluded_files)

        # check if its excluded or not, copy if it isn't
        elif file not in excluded_files:
            shutil.copy2(source_file, destination_file)


source_dir = sys.argv[1]
destination_dir = sys.argv[2]
copy_directory(source_dir, destination_dir, excluded_files)