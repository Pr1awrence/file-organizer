import os
import shutil

from categories import FILE_CATEGORIES, DEFAULT_CATEGORY


def get_file_category(file_path):
    file_extension = get_file_extension(file_path)

    for category_name, extension_set in FILE_CATEGORIES.items():
        if file_extension in extension_set:
            return category_name

    return DEFAULT_CATEGORY


def create_directory_by_category_path(category_path):
    try:
        os.mkdir(category_path)
        print(f"Created a new directory {get_file_name(category_path)}")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")


def move_file_to_directory(file_path, dest_dir_path):
    try:
        shutil.move(file_path, dest_dir_path)
        print(f"File {get_file_name(file_path)} moved successfully to {dest_dir_path}")
    except PermissionError:
        print(f"Error: Permission denied to move file or access destination folder.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()


def get_file_name(file_path):
    _, file_name = os.path.split(file_path)
    return file_name