from enum import Enum


class FileCategory(Enum):
    IMAGES = "Images"
    VIDEOS = "Videos"
    DOCUMENTS = "Documents"
    TEXT = "Text"
    ARCHIVES = "Archives"
    PROJECT = "Project"
    UNKNOWN = "Unknown"


FILE_EXTENSIONS_MAP = {
    FileCategory.IMAGES: {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".svg",
    },
    FileCategory.VIDEOS: {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"},
    FileCategory.DOCUMENTS: {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".odt",
        ".ods",
        ".odp",
    },
    FileCategory.TEXT: {".txt", ".rtf", ".md", ".log"},
    FileCategory.ARCHIVES: {".zip", ".rar", ".7z", ".tar", ".gz"},
}


PROJECT_ITEMS = {
    "venv",
    ".git",
    ".idea",
    "__pycache__",
    "organizer.py",
    "categories.py",
    "stats.py",
    "utils.py",
    "README.md",
    ".gitignore",
    "LICENSE",
}
