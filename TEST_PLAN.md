# Test Plan for File Organizer Utility

## 1. Introduction
The objective of this test plan is to ensure the reliability, data safety, and functional correctness of the File Organizer Utility. Given that the application modifies the file system (moving and deleting directories), rigorous testing is required to prevent data loss.

## 2. Test Strategy
The testing approach consists of two levels:
1.  **Automated Testing (Pytest):** Focuses on internal logic, class behaviors, and file system operations in a sandboxed environment (`tmp_path`). **Goal: achieves 100% Code Coverage.**
    *   **Unit Tests:** Isolate and verify core business logic (e.g., categorizing files based on extensions).
    *   **Integration Tests:** Verify the interaction between components (CLI, Service layer) and simulate external system behaviors using Mocks.
2.  **Manual Testing (Black Box):** Focuses on User Experience (CLI usage), integration with the real operating system, and edge cases that are difficult to automate.

## 3. Automated Testing Scope
*   **Unit Tests (`test_file_entry.py`):**
    *   Correct categorization based on file extensions.
    *   Identification of Project files (ignoring `.git`, `venv`, etc.).
    *   Handling of uppercase extensions (`.JPG` -> `.jpg`).
    *   **Edge Cases:** Handling files without extensions (e.g., `LICENSE`, binary files).
*   **Service Tests (`test_organizer_service.py`):**
    *   **Mocking File System:** Using `patch` to simulate `os.stat`, `os.chmod`, and `os.rmdir`.
    *   **Conflict Resolution:** Verifying the auto-rename logic (`file.txt` -> `file_1.txt`).
    *   **Folder Deletion Logic:**
        *   Happy path (standard deletion).
        *   **Edge Case:** Handling Windows Read-Only folders (detecting attribute -> `chmod` -> delete).
        *   **Negative Case:** Non-empty folders must be skipped.
*   **CLI & Integration Tests (`test_organizer_main.py`):**
    *   **Entry Point Verification:** Testing `main()` execution with mocked `sys.argv`.
    *   **Argument Parsing:** Verifying flags `-r` (recursive), `-a` (autorename), and default directory behavior.
    *   **Workflow Orchestration:** Ensuring the script correctly invokes service functions based on inputs.
*   **Stats Tests (`test_stats.py`):**
    *   Verification of metrics collection and log output formatting (`caplog`).

**To run automated tests:**
```bash
pipenv run pytest
```

## 4. Manual Test Cases (CLI & End-to-End)

| ID        | Test Case Name                          | Pre-conditions                                                                 | Steps                                                       | Expected Result                                                                                                                        |
|:----------|:----------------------------------------|:-------------------------------------------------------------------------------|:------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
| **TC-01** | **Smoke Test & Help**                   | None                                                                           | Run `python organizer.py --help`                            | The help menu is displayed with descriptions for `-d`, `-r`, and `-a` arguments.                                                       |
| **TC-02** | **Basic Sorting (Happy Path)**          | A folder with mixed files (`.jpg`, `.pdf`, `.txt`) exists.                     | Run `python organizer.py -d "target_folder"`                | Folders `Images`, `Documents`, `Text` are created. Files are moved correctly. Console shows "Moved" stats.                             |
| **TC-03** | **Recursive Sorting**                   | Nested folders containing files exist inside the target directory.             | Run `python organizer.py -d "target_folder" -r`             | Files from subfolders are moved to root category folders. Empty subfolders are deleted.                                                |
| **TC-04** | **Conflict Safety (Skip)**              | A file named `photo.jpg` exists in both source and destination (`Images/`).    | Run `python organizer.py -d "target_folder"` (without `-a`) | The file is **NOT** moved or overwritten. Log shows a warning. Stat "Skipped" increments.                                              |
| **TC-05** | **Conflict Resolution (Rename)**        | Same as TC-04.                                                                 | Run `python organizer.py -d "target_folder" -a`             | The file is moved and renamed using the format: original_filename + _ + rename_count + extension. The original file remains untouched. |
| **TC-06** | **Project Safety (Project folder)**     | Target folder contains `.ruff_cache/` folder.                                  | Run `python organizer.py -d "target_folder" -r`             | Project folder is ignored and left in place. Log confirms "Skipping known/project folder: .ruff_cache".                                |
| **TC-07** | **Project Safety (Project file)**       | Target folder contains `organizer.py` file.                                    | Run `python organizer.py -d "target_folder"`                | Project file is ignored and left in place. Log confirms "Skipping project file: organizer.py".                                         |
| **TC-08** | **Invalid Directory**                   | Directory does not exist.                                                      | Run `python organizer.py -d "non_existent"`                 | Error message "Directory not found". Program exits gracefully with code 1.                                                             |
| **TC-09** | **Read-Only Folder Deletion (Windows)** | Create an empty folder `Test`. Right-click -> Properties -> Check "Read-only". | Run `python organizer.py -d "target_folder" -r`             | The script detects the Read-Only attribute, removes it automatically, and deletes the folder. Log confirms deletion.                   |

## 5. Risk Assessment
*   **Data Loss:** High risk. Mitigated by:
    * `shutil.move` atomic operations.
    * Strict conflict checks (Skip by default, Rename optional).
    * LBYL (Look Before You Leap) logic: `os.listdir` checks before any deletion attempt.
*   **Permission Errors:** Addressed via:
    * `try/except` blocks logging PermissionError without crashing the app.
    * Automatic `os.chmod` injection to handle Windows Read-Only directories.