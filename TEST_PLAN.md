# Test Plan for File Organizer Utility

## 1. Introduction
The objective of this test plan is to ensure the reliability, data safety, and functional correctness of the File Organizer Utility. Given that the application modifies the file system (moving and deleting directories), rigorous testing is required to prevent data loss.

## 2. Test Strategy
The testing approach consists of two levels:
1.  **Automated Testing (Pytest):** Focuses on internal logic, class behaviors, and file system operations in a sandboxed environment (`tmp_path`).
2.  **Manual Testing (Black Box):** Focuses on User Experience (CLI usage), integration with the real operating system, and edge cases that are difficult to automate.

## 3. Automated Testing Scope
*   **Unit Tests:**
    *   Verification of file extension mapping to categories.
    *   Project file identification (ignoring `.git`, `venv`, etc.).
*   **Integration Tests:**
    *   File movement logic.
    *   Conflict resolution (generating unique paths like `file_1.txt`).
    *   Directory creation and empty folder deletion.

**To run automated tests:**
```bash
pipenv run pytest
```

## 4. Manual Test Cases (CLI & End-to-End)

| ID        | Test Case Name                      | Pre-conditions                                                              | Steps                                                       | Expected Result                                                                                                  |
|:----------|:------------------------------------|:----------------------------------------------------------------------------|:------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| **TC-01** | **Smoke Test & Help**               | None                                                                        | Run `python organizer.py --help`                            | The help menu is displayed with descriptions for `-d`, `-r`, and `-a` arguments.                                 |
| **TC-02** | **Basic Sorting (Happy Path)**      | A folder with mixed files (`.jpg`, `.pdf`, `.txt`) exists.                  | Run `python organizer.py -d "target_folder"`                | Folders `Images`, `Documents`, `Text` are created. Files are moved correctly. Console shows "Moved" stats.       |
| **TC-03** | **Recursive Sorting**               | Nested folders containing files exist inside the target directory.          | Run `python organizer.py -d "target_folder" -r`             | Files from subfolders are moved to root category folders. Empty subfolders are deleted.                          |
| **TC-04** | **Conflict Safety (Skip)**          | A file named `photo.jpg` exists in both source and destination (`Images/`). | Run `python organizer.py -d "target_folder"` (without `-a`) | The file is **NOT** moved or overwritten. Log shows a warning. Stat "Skipped" increments.                        |
| **TC-05** | **Conflict Resolution (Rename)**    | Same as TC-04.                                                              | Run `python organizer.py -d "target_folder" -a`             | The file is moved and renamed to `photo_1.jpg`. Original file remains untouched.                                 |
| **TC-06** | **Project Safety (Project folder)** | Target folder contains `.ruff_cache/` folder.                               | Run `python organizer.py -d "target_folder" -r`             | Project folder is ignored and left in place. Log confirms "Skipping known/project folder: .ruff_cache".          |
| **TC-07** | **Project Safety (Project file)**   | Target folder contains `organizer.py` file.                                 | Run `python organizer.py -d "target_folder"`                | Project file is ignored and left in place. Log confirms "Skipping project file: organizer.py".                   |
| **TC-08** | **Invalid Directory**               | Directory does not exist.                                                   | Run `python organizer.py -d "non_existent"`                 | Error message "Directory not found". Program exits gracefully with code 1.                                       |

## 5. Risk Assessment
*   **Data Loss:** High risk. Mitigated by `shutil.move` atomic operations and strict conflict checks.
*   **Permission Errors:** Addressed via try/except blocks logging `PermissionError` without crashing the app.