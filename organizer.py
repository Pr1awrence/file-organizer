import os
import argparse
import sys
import logging

from categories import FileCategory
from file_entry import FileEntry
from stats import OrganizerStats
from utils import categorize_file, create_directory_by_category_path, move_file

default_dir = "."

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("OrganizerApp")

parser = argparse.ArgumentParser(
    prog="OrganizerApp",
    description="Utility for organizing files automatically by type",
)
parser.add_argument("--directory", "-d", default=default_dir)
parser.add_argument("--autorename", "-a", action="store_true", default=False)
parser.add_argument("--recursive", "-r", action="store_true", default=False)

args = parser.parse_args()
target_dir = args.directory
auto_rename = args.autorename
recursive = args.recursive

if not os.path.isdir(target_dir):
    logger.error(
        f"Directory {target_dir} is not found, please restart program with correct path"
    )
    sys.exit(1)
elif target_dir == default_dir:
    logger.info(f"Default directory {target_dir} is used")
else:
    logger.info(f"Directory {target_dir} is found, start working...")

entries = os.listdir(target_dir)
stats = OrganizerStats()

for entry in entries:
    entry_path = os.path.join(target_dir, entry)

    if os.path.isfile(entry_path):  # working with files
        file_entry = FileEntry(entry_path)
        categorize_file(file_entry)

        if file_entry.category == FileCategory.PROJECT:
            stats.add_skipped()
            logger.info(f"Skipping project file: {file_entry.name}")
            continue

        target_dir_path = os.path.join(target_dir, file_entry.category.value)

        if not os.path.isdir(target_dir_path):
            create_directory_by_category_path(target_dir_path, stats)

        move_file(file_entry, target_dir_path, auto_rename, stats)

    elif os.path.isdir(entry_path):  # working with folders
        # TODO: create workflow for subfolders - new var arg and recursive file checking if yes
        continue

stats.display_stats()
