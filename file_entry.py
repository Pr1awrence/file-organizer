import os
import shutil

from categories import FileCategory, PROJECT_ITEMS, FILE_EXTENSIONS_MAP


class FileEntry:
    def __init__(self, full_path):
        self.path = full_path
        self.name = os.path.basename(full_path)
        self.category = FileCategory.UNKNOWN
        self.extension = self._get_file_extension(full_path)

    def categorize(self):
        if self.name in PROJECT_ITEMS:
            self.category = FileCategory.PROJECT
        else:
            for category_name, extension_set in FILE_EXTENSIONS_MAP.items():
                if self.extension in extension_set:
                    self.category = category_name
                    break

    def move_to(self, destination_file_path):
        shutil.move(self.path, destination_file_path)

        self.path = destination_file_path
        self.name = os.path.basename(destination_file_path)

    @staticmethod
    def _get_file_extension(file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower()
