import os
import argparse
import sys
import logging

from categories import FileCategory, file_category_values, PROJECT_ITEMS
from file_entry import FileEntry
from stats import OrganizerStats
from organizer_service import (
    create_directory_by_category_path,
    move_file,
    delete_empty_folder,
)


DEFAULT_DIR = "."


def main():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    logger = logging.getLogger("OrganizerApp")

    parser = argparse.ArgumentParser(
        prog="OrganizerApp",
        description="Utility for organizing files automatically by type",
    )
    parser.add_argument("--directory", "-d", default=DEFAULT_DIR)
    parser.add_argument(
        "--autorename",
        "-a",
        action="store_true",
        default=False,
        help="Automatically rename files if a conflict occurs.",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        default=False,
        help="Organize files in subdirectories recursively.",
    )

    args = parser.parse_args()
    target_dir = args.directory
    auto_rename = args.autorename
    recursive = args.recursive

    if not os.path.isdir(target_dir):
        logger.error(
            f"Directory {target_dir} is not found, please restart program with correct path"
        )
        sys.exit(1)
    elif target_dir == DEFAULT_DIR:
        logger.info(f"Default directory {target_dir} is used")
    else:
        logger.info(f"Directory {target_dir} is found, start working...")

    stats = OrganizerStats()

    def organize_files(current_dir_path):
        try:
            entries = os.listdir(current_dir_path)
        except OSError as e:
            stats.add_error()
            logger.error(f"An error during reading directory {current_dir_path}: {e}")
            return

        for entry in entries:
            entry_path = os.path.join(current_dir_path, entry)

            if os.path.isfile(entry_path):  # Files
                file_entry = FileEntry(entry_path)

                if file_entry.category == FileCategory.PROJECT:
                    stats.add_skipped()
                    logger.info(f"Skipping project file: {file_entry.name}")
                    continue

                target_dir_path = os.path.join(target_dir, file_entry.category.value)

                create_directory_by_category_path(target_dir_path, stats)

                move_file(file_entry, target_dir_path, auto_rename, stats)

            elif os.path.isdir(entry_path):  # Folders
                if recursive:
                    if entry in file_category_values or entry in PROJECT_ITEMS:
                        logger.info(f"Skipping known/project folder: {entry}")
                        stats.add_skipped()
                        continue

                    organize_files(entry_path)

                    delete_empty_folder(entry_path, stats)

    organize_files(target_dir)
    stats.display_stats()


if __name__ == "__main__":
    main()
