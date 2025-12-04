import os
import argparse
import sys

from categories import FileCategory
from utils import get_file_category, create_directory_by_category_path, move_file_to_directory

default_dir = '.'

parser = argparse.ArgumentParser(description="Parse user's directory")
parser.add_argument('--directory', action='store', dest='directory', default=default_dir)

args = parser.parse_args()
target_dir = args.directory

if not os.path.isdir(target_dir):
    print(f"Directory {target_dir} is not found, please restart program with correct path")
    sys.exit(1)
elif target_dir == default_dir:
    print(f"Default directory {target_dir} is used")
else:
    print(f"Directory {target_dir} is found, start working...")

entries = os.listdir(target_dir)

for entry in entries:
    entry_path = os.path.join(target_dir, entry)

    if os.path.isfile(entry_path): # working with files
        entry_category = get_file_category(entry_path)

        if entry_category == FileCategory.PROJECT:
            continue

        dir_path = os.path.join(target_dir, entry_category.value)

        if not os.path.isdir(dir_path):
            create_directory_by_category_path(dir_path)

        move_file_to_directory(file_path=entry_path, dest_dir_path=dir_path)

    elif os.path.isdir(entry_path): # working with folders
        #TODO: create workflow for subfolders - new var arg and recursive file checking if yes
        continue

