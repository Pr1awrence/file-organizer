import sys
from unittest.mock import patch

import pytest

from organizer import main


@pytest.fixture()
def mock_argv():
    def _set_args(arg_list):
        return patch.object(sys, "argv", arg_list)

    return _set_args


def test_valid_directory(tmp_path, mock_argv):
    (tmp_path / "photo.jpg").touch()

    with mock_argv(["organizer.py", "-d", str(tmp_path)]):
        main()

    assert (tmp_path / "Images" / "photo.jpg").exists()


def test_invalid_directory(caplog):
    test_args = ["organizer.py", "-d", "/non/existent/path"]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1

    assert (
        f"Directory {test_args[2]} is not found, please restart program with correct path"
        in caplog.text
    )


def test_default_directory(tmp_path, mock_argv, caplog):
    with patch("organizer.DEFAULT_DIR", str(tmp_path)):
        with mock_argv(["organizer.py"]):
            main()

    assert f"Default directory {str(tmp_path)} is used" in caplog.text


def test_reading_file_generic_error(tmp_path, mock_argv, caplog):
    error_message = "Disk fail"
    with patch("organizer.os.listdir", side_effect=OSError(error_message)):
        with mock_argv(["organizer.py", "-d", str(tmp_path)]):
            main()

    assert (
        f"An error during reading directory {str(tmp_path)}: {error_message}"
        in caplog.text
    )


def test_skip_project_files(tmp_path, caplog):
    project_file = tmp_path / "organizer.py"
    project_file.touch()

    test_args = ["organizer.py", "-d", str(tmp_path)]

    with patch.object(sys, "argv", test_args):
        main()

    assert project_file.exists()
    assert "Skipping project file: organizer.py" in caplog.text


def test_skip_folders_without_recursive(tmp_path, mock_argv):
    folder = tmp_path / "Folder"
    folder.mkdir()
    file = folder / "file.txt"
    file.touch()

    with mock_argv(["organizer.py", "-d", str(tmp_path)]):
        main()

    assert folder.exists()
    assert file.exists()


def test_recursive_success(tmp_path, mock_argv):
    folder = tmp_path / "Folder"
    folder.mkdir()
    file = folder / "file.txt"
    file.touch()

    with mock_argv(["organizer.py", "-d", str(tmp_path), "-r"]):
        main()

    assert (tmp_path / "Text" / "file.txt").exists()
    assert not folder.exists()


def test_recursive_skip_project_files(tmp_path, mock_argv, caplog):
    venv = tmp_path / "venv"
    venv.mkdir()

    with mock_argv(["organizer.py", "-d", str(tmp_path), "-r"]):
        main()

    assert venv.exists()
    assert "Skipping known/project folder: venv" in caplog.text
