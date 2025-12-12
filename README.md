# Python File Organizer Utility

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## Short Description
A lightweight Python utility for automatically organizing files in a specified directory by type (images, videos, documents, etc.), with support for recursive traversal and automatic renaming of conflicting files.

## Project Description
This project was developed as a practical exercise to hone Python automation skills. It addresses the common problem of cluttered folders (e.g., "Downloads") by categorizing and moving files into appropriate subfolders. The utility is written with an object-oriented approach and module-based logic, making it easily extensible and maintainable.

## Features
*   **Category-based Sorting:** Automatically identifies file types (image, video, document, text, archive, other) and moves them into corresponding subfolders (e.g., `Images/`, `Videos/`, `Documents/`).
*   **Flexible Directory Specification:** Users can specify any target directory for organization via command-line arguments.
*   **Recursive Traversal:** Optional ability to process files within all nested subdirectories.
*   **Automatic Empty Folder Deletion:** In recursive mode, empty subfolders from which all files have been moved are automatically deleted.
*   **Conflict Resolution:** Option to automatically rename files when duplicates are found in the target category (e.g., `report.pdf` becomes `report_1.pdf`).
*   **Project Item Exclusion:** Automatically skips project-related files and folders (`.git/`, `venv/`, `organizer.py`, etc.) to prevent unintended modifications.
*   **Detailed Logging:** Utilizes Python's standard `logging` module for informative output on progress, warnings, and errors.
*   **Summary Report:** Displays a consolidated report at the end of the operation, including statistics on moved files, skipped items, and errors.

## Demo
**1. Folder state before sorting**
![Before Sorting](docs/images/before_sorting.png)

**2. File organization report after sorting**
![File Organization After Sorting](docs/images/file_org_report.png)

**3. Folder state after sorting**
![After Sorting](docs/images/after_sorting.png)

## Getting Started 
### Prerequisites
*   Python 3.13 or higher
*   `pip`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Pr1awrence/file-organizer.git
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
    
## Usage
Run the script from your command line, specifying the target directory and optional arguments.

### Basic Sort
Organize files in the current directory:
```bash
python organizer.py --directory="C:\pathtoyourfolder"
```

### Recursive Sort
Process files in all subdirectories and delete empty ones:
```bash
python organizer.py --directory="C:\pathtoyourfolder" -r
```

### Automatic Renaming
Automatically rename files if duplicates are found in the destination:
```bash
python organizer.py --directory="C:\pathtoyourfolder" -a
```

### Combined Usage
```bash
python organizer.py --directory="C:\pathtoyourfolder" -r -a
```

## Project Structure
*   `organizer.py`: The main executable script, handles command-line arguments and orchestrates the sorting process.
*   `organizer_service.py`: Contains file system interaction functions (directory creation, file movement, unique filename generation).
*   `file_entry.py`: Defines the FileEntry class to encapsulate file information and behavior (categorization, movement).
*   `categories.py`: Defines the FileCategory Enum, file extension mappings, and a list of ignored project-related items.
*   `stats.py`: Defines the OrganizerStats class for collecting and displaying operational statistics.

## Author
[Galina Smirnova / Pr1awrence](https://github.com/Pr1awrence)

## License
This project is licensed under the MIT License - see the `LICENSE.txt` file for details.