from logging import getLogger

from file_entry import FileEntry


logger = getLogger("OrganizerApp")


class OrganizerStats:
    def __init__(self):
        self.processed_count = 0
        self.moved_count = 0
        self.error_count = 0
        self.skipped_count = 0
        self.category_counts = {}


    def add_moved(self, file_entry: FileEntry):
        self.moved_count += 1
        self.processed_count +=1
        self.category_counts[file_entry.category.value] = self.category_counts.get(file_entry.category.value, 0) + 1


    def add_error(self):
        self.error_count += 1
        self.processed_count += 1


    def add_skipped(self):
        self.skipped_count += 1
        self.processed_count += 1


    def display_stats(self):
        logger.info("\n--- File organization report ---")
        logger.info(f"Total processed: {self.processed_count}")
        logger.info(f"Total moved successfully: {self.moved_count}")
        logger.info(f"Total skipped/errors: {self.skipped_count} / {self.error_count}")
        if self.category_counts:
            logger.info("Categories:")
            for category, count in self.category_counts.items():
                logger.info(f"{category}: {count}")