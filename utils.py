import os


def is_dir_exists(user_dir):
    return os.path.isdir(user_dir)


def get_directory_contents(user_dir):
    return os.listdir(user_dir)