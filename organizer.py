import os
import argparse
import sys

from utils import get_directory_contents, is_dir_exists

default_dir = '.'

parser = argparse.ArgumentParser(description="Parse user's directory")
parser.add_argument('--directory', action='store', dest='directory', default=default_dir)

args = parser.parse_args()
target_directory = args.directory

if not is_dir_exists(target_directory):
    print(f"Directory {target_directory} is not found, please restart program with correct path")
    sys.exit(1)
elif target_directory == default_dir:
    print(f"Default directory {target_directory} is used")
else:
    print(f"Directory {target_directory} is found, start working...")

entries = get_directory_contents(target_directory)

for entry in entries:
    entry_path = os.path.join(target_directory, entry)

    if os.path.isfile(entry_path):
        print(f"File: {entry_path}")
    elif os.path.isdir(entry_path):
        print(f"Folder: {entry_path}")
    else:
        print(f"Unknown type: {entry_path}")
