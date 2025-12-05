import logging
import os
import shutil

from categories import FILE_EXTENSIONS_MAP, PROJECT_ITEMS, FileCategory
from file_entry import FileEntry
from stats import OrganizerStats


logger = logging.getLogger("OrganizerApp")


def categorize_file(file_entry: FileEntry):
    if file_entry.name in PROJECT_ITEMS:
        file_entry.category = FileCategory.PROJECT
    else:
        for category_name, extension_set in FILE_EXTENSIONS_MAP.items():
            if file_entry.extension in extension_set:
                file_entry.category = category_name


def create_directory_by_category_path(category_path, stats: OrganizerStats):
    try:
        os.mkdir(category_path)
        logger.info(f"Created a new directory {os.path.basename(category_path)}")
    except Exception as e:
        stats.add_error()
        logger.error(f"An error occurred while creating the folder: {e}")


def move_file(file_entry: FileEntry, destination_dir_path, stats: OrganizerStats):
    try:
        shutil.move(file_entry.path, destination_dir_path)
        stats.add_moved(file_entry)
        logger.info(f"File {os.path.basename(file_entry.path)} moved successfully to {destination_dir_path}")
    except PermissionError:
        stats.add_error()
        logger.error(f"Error: Permission denied to move file or access destination folder.")
    except Exception as e:
        stats.add_error()
        logger.error(f"An unexpected error occurred: {e}")
