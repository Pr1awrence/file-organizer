from enum import Enum


class FileCategory(Enum):
    IMAGES = "Images"
    VIDEOS = "Videos"
    DOCUMENTS = "Documents"
    TEXT = "Text"
    ARCHIVES = "Archives"
    PROJECT = "Project"
    UNKNOWN = "Unknown"


file_category_values = [file_type.value for file_type in FileCategory]


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
    ".ruff_cache",
    "organizer.py",
    "categories.py",
    "stats.py",
    "organizer_service.py",
    "file_entry.py",
    "README.md",
    ".gitignore",
    "LICENSE",
    "Pipfile",
    "Pipfile.lock",
}
