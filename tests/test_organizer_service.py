import os
import stat
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from file_entry import FileEntry
from organizer_service import (
    move_file,
    get_unique_filepath,
    create_directory_by_category_path,
    delete_empty_folder,
)
from stats import OrganizerStats


@pytest.fixture
def stats():
    return OrganizerStats()


@pytest.fixture
def setup_folders(tmp_path):
    source = tmp_path / "source"
    target = tmp_path / "target"
    source.mkdir()
    target.mkdir()

    return source, target


@pytest.fixture()
def mock_fs():
    default_stat = MagicMock()
    default_stat.st_mode = stat.S_IWRITE

    with (
        patch("organizer_service.os.listdir", return_value=[]) as mock_listdir,
        patch("organizer_service.os.stat", return_value=default_stat) as mock_stat,
        patch("organizer_service.os.chmod") as mock_chmod,
        patch("organizer_service.os.rmdir") as mock_rmdir,
    ):
        yield SimpleNamespace(
            listdir=mock_listdir,
            stat=mock_stat,
            chmod=mock_chmod,
            rmdir=mock_rmdir,
            stat_obj=default_stat,
        )


def test_create_directory_success(tmp_path, stats):
    new_dir = tmp_path / "Images"

    assert not new_dir.exists()

    create_directory_by_category_path(str(new_dir), stats)

    assert new_dir.exists()
    assert stats.error_count == 0


def test_create_directory_already_exists(tmp_path, stats):
    existing_dir = tmp_path / "Videos"
    existing_dir.mkdir()

    with patch("organizer_service.os.mkdir") as mock_mkdir:
        create_directory_by_category_path(str(existing_dir), stats)

    mock_mkdir.assert_not_called()

    assert stats.error_count == 0


def test_create_directory_generic_error(tmp_path, stats):
    new_dir = tmp_path / "Images"

    with patch("organizer_service.os.mkdir", side_effect=OSError("Disk full")):
        create_directory_by_category_path(str(new_dir), stats)

    assert stats.error_count == 1
    assert not new_dir.exists()


def test_get_unique_filepath(tmp_path):
    conflict_file = tmp_path / "test.txt"
    conflict_file.touch()

    new_path = get_unique_filepath("test.txt", str(tmp_path), str(conflict_file))

    expected_path = os.path.join(str(tmp_path), "test_1.txt")
    assert new_path == expected_path


def test_get_unique_filepath_multi_conflict(tmp_path):
    conflict_file = tmp_path / "test.txt"
    conflict_file.touch()

    (tmp_path / "test_1.txt").touch()

    new_path = get_unique_filepath("test.txt", str(tmp_path), str(conflict_file))

    expected_path = os.path.join(str(tmp_path), "test_2.txt")
    assert new_path == expected_path


def test_move_file_success(setup_folders, stats):
    source_dir, target_dir = setup_folders
    test_file = source_dir / "photo.jpg"
    test_file.write_text("content")

    entry = FileEntry(str(test_file))

    move_file(entry, str(target_dir), auto_rename=False, stats=stats)

    assert not test_file.exists()
    assert (target_dir / "photo.jpg").exists()
    assert stats.moved_count == 1


def test_move_file_conflict_skip(setup_folders, stats):
    source_dir, target_dir = setup_folders

    file_src = source_dir / "doc.txt"
    file_src.write_text("new content")

    file_dest = target_dir / "doc.txt"
    file_dest.write_text("old content")

    entry = FileEntry(str(file_src))

    move_file(entry, str(target_dir), auto_rename=False, stats=stats)

    assert file_src.exists()
    assert file_dest.read_text() == "old content"
    assert stats.skipped_count == 1


def test_move_file_conflict_rename(setup_folders, stats):
    source_dir, target_dir = setup_folders

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


def test_move_file_permission_error(setup_folders, stats):
    source_dir, target_dir = setup_folders

    file_src = source_dir / "locked.txt"
    file_src.write_text("content")

    entry = FileEntry(str(file_src))

    with patch("file_entry.shutil.move", side_effect=PermissionError("Access denied")):
        move_file(entry, str(target_dir), auto_rename=False, stats=stats)

    assert file_src.exists()
    assert stats.error_count == 1
    assert stats.moved_count == 0


def test_delete_empty_and_writable_folder(setup_folders, mock_fs, stats):
    folder, _ = setup_folders

    delete_empty_folder(str(folder), stats)

    mock_fs.listdir.assert_called_once()
    mock_fs.stat.assert_called_once()
    mock_fs.chmod.assert_not_called()
    mock_fs.rmdir.assert_called_once_with(str(folder))
    assert stats.deleted_folder_count == 1


def test_delete_empty_and_readonly_folder(setup_folders, mock_fs, stats):
    folder, _ = setup_folders

    mock_fs.stat_obj.st_mode = stat.S_IREAD

    delete_empty_folder(str(folder), stats)

    mock_fs.chmod.assert_called_once_with(str(folder), stat.S_IWRITE)
    mock_fs.rmdir.assert_called_once_with(str(folder))
    assert stats.deleted_folder_count == 1


def test_delete_not_empty_folder_skip(setup_folders, mock_fs, stats):
    folder, _ = setup_folders

    mock_fs.listdir.return_value = ["image.jpg"]

    delete_empty_folder(str(folder), stats)

    mock_fs.listdir.assert_called_once()
    mock_fs.stat.assert_not_called()
    mock_fs.chmod.assert_not_called()
    mock_fs.rmdir.assert_not_called()
    assert stats.deleted_folder_count == 0
