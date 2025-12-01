import os
import argparse

default_dir = '.'

parser = argparse.ArgumentParser(description="Parse user's directory")
parser.add_argument('--directory', action='store', dest='directory', default=default_dir)

args = parser.parse_args()

contents = os.listdir(args.directory)

for item in contents:
    item_path = os.path.join(args.directory, item)

    if os.path.isfile(item_path):
        print(f"File: {item_path}")
    elif os.path.isdir(item_path):
        print(f"Folder: {item_path}")
    else:
        print(f"Unknown type: {item_path}")
