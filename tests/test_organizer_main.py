import logging
import sys
from unittest.mock import patch

import pytest

from organizer import main


@pytest.fixture()
def mock_argv():
    def _set_args(arg_list):
        return patch.object(sys, 'argv', arg_list)
    return _set_args


def test_main_script_runs_successfully(tmp_path, mock_argv):
    (tmp_path / "photo.jpg").touch()

    with mock_argv(["organizer.py", "-d", str(tmp_path)]):
        main()

    assert (tmp_path / "Images" / "photo.jpg").exists()


def test_main_script_invalid_directory(caplog):
    test_args = ["organizer.py", "-d", "/non/existent/path"]

    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1

    assert f"Directory {test_args[2]} is not found, please restart program with correct path" in caplog.text


def test_main_script_default_directory(tmp_path, mock_argv, caplog):
    caplog.set_level(logging.INFO)

    with patch("organizer.DEFAULT_DIR", str(tmp_path)):
        with mock_argv(["organizer.py"]):
            main()

    assert f"Default directory {str(tmp_path)} is used" in caplog.text


def test_main_script_skips_project_files(tmp_path, caplog):
    caplog.set_level(logging.INFO)

    project_file = tmp_path / "organizer.py"
    project_file.touch()

    test_args = ["organizer.py", "-d", str(tmp_path)]

    with patch.object(sys, 'argv', test_args):
        main()

    assert project_file.exists()
    assert "Skipping project file: organizer.py" in caplog.text

