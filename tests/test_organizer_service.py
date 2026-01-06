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

    test_file = source_dir / "photo.jpg"
    test_file.write_text("content")

    entry = FileEntry(str(test_file))

    move_file(entry, str(target_dir), auto_rename=False, stats=stats)

    assert not test_file.exists()
    assert (target_dir / "photo.jpg").exists()
    assert stats.moved_count == 1


def test_move_file_conflict_skip(tmp_path, stats):
    source_dir = tmp_path / "source"
    target_dir = tmp_path / "target"
    source_dir.mkdir()
    target_dir.mkdir()

    file_src = source_dir / "doc.txt"
    file_src.write_text("new content")

    file_dest = target_dir / "doc.txt"
    file_dest.write_text("old content")

    entry = FileEntry(str(file_src))

    move_file(entry, str(target_dir), auto_rename=False, stats=stats)

    assert file_src.exists()
    assert file_dest.read_text() == "old content"
    assert stats.skipped_count == 1


def test_move_file_conflict_rename(tmp_path, stats):
    source_dir = tmp_path / "source"
    target_dir = tmp_path / "target"
    source_dir.mkdir()
    target_dir.mkdir()

    file_src = source_dir / "doc.txt"
    file_src.write_text("new content")

    file_dest = target_dir / "doc.txt"
    file_dest.write_text("old content")

    entry = FileEntry(str(file_src))

    move_file(entry, str(target_dir), auto_rename=True, stats=stats)

    assert not file_src.exists()
    assert file_dest.read_text() == "old content"

    renamed_file = target_dir / "doc_1.txt"
    assert renamed_file.exists()
    assert renamed_file.read_text() == "new content"
    assert stats.moved_count == 1
