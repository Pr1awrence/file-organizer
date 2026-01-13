from file_entry import FileEntry
from stats import OrganizerStats


def test_stats_collection_and_display(caplog):
    stats = OrganizerStats()

    entry = FileEntry("path/image.png")

    stats.add_moved(entry)
    stats.add_skipped()
    stats.add_error()
    stats.add_deleted_folder()

    stats.display_stats()

    assert "Total processed: 4" in caplog.text
    assert "Total moved successfully: 1" in caplog.text
    assert "Images: 1" in caplog.text
