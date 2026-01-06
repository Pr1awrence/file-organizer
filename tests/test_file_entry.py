import pytest

from categories import FileCategory
from file_entry import FileEntry


@pytest.mark.parametrize(
    "filename, expected_category, expected_ext",
    [
        ("vacation.jpg", FileCategory.IMAGES, ".jpg"),
        ("resume.pdf", FileCategory.DOCUMENTS, ".pdf"),
        ("song.mp3", FileCategory.UNKNOWN, ".mp3"),
        ("archive.zip", FileCategory.ARCHIVES, ".zip"),
        ("README.md", FileCategory.PROJECT, ".md"),
    ],
)
def test_categorize_file(filename, expected_category, expected_ext):
    entry = FileEntry(f"/dummy/path/{filename}")

    assert entry.category == expected_category
    assert entry.extension == expected_ext


def test_project_folder_recognition():
    entry = FileEntry("/home/user/project/venv")

    assert entry.category == FileCategory.PROJECT
