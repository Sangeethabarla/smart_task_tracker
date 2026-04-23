# Smart Task & Productivity Tracker

A clean, modular, and beginner-friendly command-line application built in pure Python to manage tasks and boost your productivity. It functions completely offline with zero external database requirements—storing your tasks directly into a local `.json` file.

## 🚀 Features

- **Add New Tasks:** Create tasks with optional priorities (High, Medium, Low) and due dates (`YYYY-MM-DD`). 
- **View Tasks:** Easily visualize pending and completed tasks, complete with automated counters.
- **Deadline Monitoring:** Overdue tasks are dynamically tagged with an `(OVERDUE)` status modifier.
- **Priority Highlighting:** Important tasks are clearly marked with `!!! High !!!`.
- **Search & Filter:** Search tasks seamlessly by keyword or filter them strictly by their status (Pending/Completed) and priority tier.
- **Sorting Logic:** Arrange tasks sequentially by their assigned priority or chronologically by due date.
- **Data Persistence:** Tasks are automatically saved to `tasks.json` upon exit and safely loaded when the program starts.

## 📋 Prerequisites

- **Python 3.x** installed on your system. 
- *No external libraries or pip installations required.* The project utilizes only Python's built-in standard libraries (`json`, `os`, `datetime`).

## ⚙️ How to Run

1. Open your terminal natively (e.g., PowerShell, Command Prompt, or within VS Code's terminal pane).
2. Navigate to the directory containing the file:
   ```bash
   cd path/to/project
   ```
3. Execute the interactive tracking script:
   ```bash
   python smart_task_tracker.py
   ```

## 🗂 Project Record Logs & Structure

- `smart_task_tracker.py`: Main execution script containing all logic operations and CLI visual interfaces.
- `tasks.json`: An automatically generated data storage file initialized on your first save.
- `README.md`: Main project documentation.

## 👨‍💻 Resume Value
This project functions as a structural template and allows you to showcase beginner-to-intermediate Python Software Development (SDE) skills. Feel free to clone, interact, tweak, and expand this app (e.g., by migrating the storage format to an SQLite Database or building a Flask frontend API) to bolster your resume!
