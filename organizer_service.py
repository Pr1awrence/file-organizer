import logging
import os

from file_entry import FileEntry
from stats import OrganizerStats


logger = logging.getLogger("OrganizerApp")


def create_directory_by_category_path(category_path, stats: OrganizerStats):
    try:
        os.mkdir(category_path)
        logger.info(f"Created a new directory {os.path.basename(category_path)}")
    except Exception as e:
        stats.add_error()
        logger.error(f"An error occurred while creating the folder: {e}")


def move_file(
    file_entry: FileEntry, destination_dir_path, auto_rename, stats: OrganizerStats
):
    try:
        destination_file_path = os.path.join(destination_dir_path, file_entry.name)

        if os.path.exists(destination_file_path):
            if auto_rename:
                destination_file_path = get_unique_filepath(
                    file_entry.name, destination_dir_path, destination_file_path
                )
                logger.info(
                    f"File conflict resolved. Using unique name: {os.path.basename(destination_file_path)}"
                )
            else:
                logger.warning(
                    f"File '{file_entry.name}' already exists in '{destination_dir_path}'. Skipping."
                )
                stats.add_skipped()
                return

        FileEntry.move_to(file_entry, destination_file_path)

        stats.add_moved(file_entry)
        logger.info(
            f"File {os.path.basename(file_entry.path)} moved successfully to {destination_dir_path}"
        )
    except PermissionError:
        stats.add_error()
        logger.error(
            f"Error: Permission denied to move file or access destination folder."
        )
    except Exception as e:
        stats.add_error()
        logger.error(f"An unexpected error occurred: {e}")


def get_unique_filepath(filename, directory, existing_full_path):
    stem, suffix = os.path.splitext(filename)
    counter = 1
    new_full_path = existing_full_path

    while os.path.exists(new_full_path):
        new_filename = f"{stem}_{counter}{suffix}"
        new_full_path = os.path.join(directory, new_filename)

        counter += 1

    return new_full_path
