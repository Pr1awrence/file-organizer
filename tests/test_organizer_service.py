import os

import pytest

from file_entry import FileEntry
from organizer_service import move_file, get_unique_filepath
from stats import OrganizerStats


@pytest.fixture
def stats():
    return OrganizerStats()


def test_get_unique_filepath(tmp_path, stats):
    conflict_file = tmp_path / "test.txt"
    conflict_file.write_text("content")

    new_path = get_unique_filepath("test.txt", str(tmp_path), str(conflict_file))

    expected_path = os.path.join(str(tmp_path), "test_1.txt")
    assert new_path == expected_path


def test_move_file_success(tmp_path, stats):
    source_dir = tmp_path / "source"
    target_dir = tmp_path / "target"
    source_dir.mkdir()
    target_dir.mkdir()

    test_file = tmp_path / "photo.jpg"
    test_file.write_text("content")

    entry = FileEntry(str(test_file))
    entry.categorize()

    move_file(entry, str(target_dir), auto_rename=False, stats=stats)

    assert not test_file.exists()
    assert (target_dir / "photo.jpg").exists()
    assert stats.moved_count == 1
