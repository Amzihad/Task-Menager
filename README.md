# SUPERNOVA - Student Academic Task Manager (Desktop Version)

A pure **Python OOP** project with a graphical window made with **Tkinter**. No Flask, no HTML, no pip packages. Tasks are stored in a JSON file.

- **Teachers** can add, view, edit and delete tasks.
- **Students** can view tasks, see deadlines, mark tasks completed, and view pending / completed tasks.

## Folder Structure

```
supernova_gui/
├── main.py             # window classes: App, LoginPage, Dashboard,
│                       #   TeacherDashboard, StudentDashboard, TaskDialog
├── models.py           # data classes: User, Teacher, Student, Task, TaskManager
├── README.md
└── data/
    └── tasks.json      # saved tasks (created automatically if missing)
```

## How to Run

1. Install Python 3.8 or newer.
2. Tkinter must be installed:
   - **Windows / Mac:** already included with the Python installer from python.org.
   - **Ubuntu / Linux Mint / Debian:** run once
     ```
     sudo apt install python3-tk
     ```
3. Run:
   ```
   cd supernova_gui
   python3 main.py          # on Windows: python main.py
   ```

Check Tkinter quickly with: `python3 -m tkinter` (a small test window should open).

## Login Accounts (password for all: `1234`)

The login window does not show these. Type them yourself.

| Role    | Usernames                                                  |
|---------|------------------------------------------------------------|
| Teacher | `teacher`, `teacher2`, `teacher3`, `teacher4`, `teacher5`  |
| Student | `student`, `student2`, `student3`, `student4`, `student5`  |

## How to Use

- **Teacher:** click a row to select a task, then use **Edit** or **Delete**. Use **+ Add Task** to create a new one.
- **Student:** use the sidebar to switch between All, Pending and Completed tasks. Select a row and click **Mark as Completed**.
- Click a row to read the task description below the table.

## OOP Concepts (for the viva)

| Concept | Where it is used |
|---|---|
| **Classes and Objects** | `User`, `Teacher`, `Student`, `Task`, `TaskManager` (`models.py`) and the window classes in `main.py`. The 10 users and every task are objects. |
| **Inheritance** | `Teacher(User)` and `Student(User)`. Also `TeacherDashboard(Dashboard)` and `StudentDashboard(Dashboard)` share one layout from the parent `Dashboard` class. `App`, `LoginPage` and `TaskDialog` inherit from Tkinter classes. |
| **Encapsulation** | Attributes start with two underscores (`self.__password`, `self.__title`). They are read through getters/properties and changed only by methods like `update()` and `mark_completed()`. |
| **Constructors** | Every class has `__init__`. Child classes call `super().__init__(...)`. |
| **Methods / overriding** | `get_role()`, `get_info()`, `can_manage_tasks()` are overridden in `Teacher` and `Student`. `Dashboard` defines empty methods (`get_row`, `get_tasks`, `build_actions`...) that each child class overrides. |

## How It Works

- `App` is the main window. It creates the `TaskManager`, keeps the logged-in user, and switches between pages.
- After login, `App` opens `TeacherDashboard` or `StudentDashboard` depending on the user's role.
- Every teacher action (`add_task`, `edit_task`, `delete_task`) first calls `check_teacher()`, which uses `can_manage_tasks()`. The student dashboard class does not even have these actions.
- `TaskManager` loads `data/tasks.json` at start-up and saves after every change, so tasks stay after closing the program.
- Each task stores the usernames of students who completed it (`completed_by`), so every student has their own Completed / Pending list.

Passwords are plain text because this is a demo project.
