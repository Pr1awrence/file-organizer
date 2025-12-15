from categories import FileCategory
from file_entry import FileEntry


def test_category_identification():
    entry = FileEntry("/some/path/holiday.jpg")
    entry.categorize()

    assert entry.category == FileCategory.IMAGES
    assert entry.extension == ".jpg"