import os

from categories import FileCategory


class FileEntry:
    def __init__(self, full_path):
        self.path = full_path
        self.name = os.path.basename(full_path)
        self.category = FileCategory.UNKNOWN
        self.extension = _get_file_extension(full_path)


def _get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()