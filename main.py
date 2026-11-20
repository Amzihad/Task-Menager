"""main.py - SUPERNOVA desktop version (pure Python OOP with Tkinter).

No Flask, no HTML. Classes in this file: App, LoginPage, Dashboard,
TeacherDashboard, StudentDashboard, TaskDialog.
Data classes (User, Teacher, Student, Task, TaskManager) are in models.py.
"""
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from models import Student, Teacher, TaskManager

# ----- colors and font (deep indigo + violet theme, amber highlights) -----
DEEP = "#1e1b4b"       # sidebar, login left panel, headings
PRIMARY = "#6d28d9"    # main buttons, login background
LIGHT = "#f5f3ff"      # table heading background
BG = "#f4f4fb"         # page background
GRAY = "#64748b"       # small grey text
ACCENT = "#f59e0b"     # amber highlights (star, card bars)
FONT = "Helvetica"

TASK_TYPES = ["Assignment", "Quiz", "Lab Report", "Project",
              "Presentation", "Exam"]


# ---------------------------------------------------------------
# App: the main window. Holds the data and switches pages.
# ---------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):                      # Constructor
        super().__init__()
        self.title("SUPERNOVA - Student Academic Task Manager")
        self.geometry("1050x640")
        self.minsize(960, 600)

        folder = os.path.dirname(os.path.abspath(__file__))
        self.manager = TaskManager(os.path.join(folder, "data", "tasks.json"))
        self.current_user = None
        self.page = None
        # Ten demo users (objects of Teacher and Student). Password: 1234
        self.users = [
            Teacher("teacher", "1234", "Teacher One", "CSE"),
            Teacher("teacher2", "1234", "Teacher Two", "EEE"),
            Teacher("teacher3", "1234", "Teacher Three", "BBA"),
            Teacher("teacher4", "1234", "Teacher Four", "Math"),
            Teacher("teacher5", "1234", "Teacher Five", "English"),
            Student("student", "1234", "Student One", "S-001"),
            Student("student2", "1234", "Student Two", "S-002"),
            Student("student3", "1234", "Student Three", "S-003"),
            Student("student4", "1234", "Student Four", "S-004"),
            Student("student5", "1234", "Student Five", "S-005"),
        ]
        self.setup_style()
        self.show_login()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=(FONT, 10),
                        background="white", fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", background=LIGHT, foreground=DEEP,
                        font=(FONT, 10, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#ddd6fe")],
                  foreground=[("selected", DEEP)])

    def switch_page(self, page_class):
        """Remove the old page and show a new one."""
        if self.page is not None:
            self.page.destroy()
        self.page = page_class(self, self)
        self.page.pack(fill="both", expand=True)

    def show_login(self):
        self.current_user = None
        self.switch_page(LoginPage)

    def show_dashboard(self):
        if self.current_user.get_role() == "teacher":
            self.switch_page(TeacherDashboard)
        else:
            self.switch_page(StudentDashboard)

    def find_user(self, username):
        for user in self.users:
            if user.get_username() == username:
                return user
        return None

    def login(self, username, password):
        user = self.find_user(username)
        if user is not None and user.check_password(password):
            self.current_user = user
            return True
        return False


# ---------------------------------------------------------------
# LoginPage
# ---------------------------------------------------------------
class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=PRIMARY)
        self.app = app

        card = tk.Frame(self, bg="white")
        card.place(relx=0.5, rely=0.5, anchor="center", width=820, height=430)

        # left: brand panel
        left = tk.Frame(card, bg=DEEP, width=380)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        brand = tk.Frame(left, bg=DEEP)          # expand=True centers it up-down
        brand.pack(expand=True, anchor="w", padx=36)
        tk.Label(brand, text="★", font=(FONT, 34), fg=ACCENT, bg=DEEP
                 ).pack(anchor="w")
        tk.Label(brand, text="SUPERNOVA", font=(FONT, 26, "bold"), fg="white", bg=DEEP
                 ).pack(anchor="w")
        tk.Label(brand, text="Student Academic Task Manager", font=(FONT, 11),
                 fg="#c4b5fd", bg=DEEP).pack(anchor="w", pady=(2, 24))
        for text in ["✓  Teachers assign and manage tasks",
                     "✓  Students track deadlines easily",
                     "✓  Everything in one simple place"]:
            tk.Label(brand, text=text, font=(FONT, 11), fg="#ddd6fe", bg=DEEP
                     ).pack(anchor="w", pady=4)

        # right: login form (also centered up-down)
        right_side = tk.Frame(card, bg="white")
        right_side.pack(side="left", fill="both", expand=True)
        right = tk.Frame(right_side, bg="white")
        right.pack(expand=True, fill="x", padx=36)
        tk.Label(right, text="Welcome back", font=(FONT, 22, "bold"),
                 fg=DEEP, bg="white").pack(anchor="w")
        tk.Label(right, text="Please log in to continue", font=(FONT, 11),
                 fg=GRAY, bg="white").pack(anchor="w", pady=(2, 14))

        tk.Label(right, text="Username", font=(FONT, 10, "bold"), bg="white"
                 ).pack(anchor="w")
        self.username = self.make_entry(right)
        tk.Label(right, text="Password", font=(FONT, 10, "bold"), bg="white"
                 ).pack(anchor="w", pady=(10, 0))
        self.password = self.make_entry(right, show="•")

        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(right, text="Show password", variable=self.show_var,
                       command=self.toggle_password, bg="white", fg=GRAY,
                       activebackground="white", activeforeground=GRAY,
                       selectcolor="white", relief="flat", bd=0,
                       highlightthickness=0, cursor="hand2", font=(FONT, 9)
                       ).pack(anchor="w", pady=(6, 0))

        self.error = tk.Label(right, text="", font=(FONT, 10), fg="#dc2626", bg="white")
        self.error.pack(anchor="w", pady=(4, 0))
        tk.Button(right, text="Login", command=self.do_login, bg=PRIMARY, fg="white",
                  activebackground=DEEP, activeforeground="white", relief="flat",
                  bd=0, font=(FONT, 12, "bold"), pady=9, cursor="hand2"
                  ).pack(fill="x", pady=(6, 0))
        self.username.focus_set()

    def make_entry(self, parent, show=""):
        entry = tk.Entry(parent, font=(FONT, 12), relief="flat", show=show,
                         highlightthickness=1, highlightbackground="#cbd5e1",
                         highlightcolor=PRIMARY)
        entry.pack(fill="x", ipady=6, pady=(4, 0))
        entry.bind("<Return>", lambda event: self.do_login())
        return entry

    def toggle_password(self):
        self.password.config(show="" if self.show_var.get() else "•")

    def do_login(self):
        if self.app.login(self.username.get().strip(), self.password.get()):
            self.app.show_dashboard()
        else:
            self.error.config(text="Wrong username or password.")


# ---------------------------------------------------------------
# Dashboard (parent class): sidebar + cards + task table.
# TeacherDashboard and StudentDashboard inherit from it.
# ---------------------------------------------------------------
class Dashboard(tk.Frame):
    columns = []        # (name, width) for the table - set by child classes
    card_titles = []    # titles of the 3 cards - set by child classes
    start_view = ""

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.user = app.current_user
        self.manager = app.manager
        self.view = self.start_view
        self.nav_buttons = {}
        self.build_sidebar()
        self.build_content()
        self.set_active(self.view)
        self.refresh()

    # ----- methods that child classes override -----
    def nav_items(self):
        return []

    def build_actions(self, frame):
        pass

    def get_tasks(self):
        return self.manager.get_all_tasks()

    def get_row(self, task):
        return ()

    def get_card_values(self):
        return []

    def get_heading(self):
        return ""

    # ----- layout -----
    def build_sidebar(self):
        side = tk.Frame(self, bg=DEEP, width=230)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        tk.Label(side, text="★ SUPERNOVA", font=(FONT, 16, "bold"),
                 fg="white", bg=DEEP).pack(anchor="w", padx=20, pady=(24, 0))
        tk.Label(side, text="Student Academic Task Manager", font=(FONT, 8),
                 fg="#c4b5fd", bg=DEEP).pack(anchor="w", padx=20, pady=(2, 24))

        for key, text, command in self.nav_items():
            button = tk.Button(side, text=text, command=command, anchor="w",
                               font=(FONT, 11), fg="#ddd6fe", bg=DEEP,
                               activebackground=PRIMARY, activeforeground="white",
                               relief="flat", bd=0, padx=16, pady=9, cursor="hand2")
            button.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = button

        box = tk.Frame(side, bg="#312e81")
        box.pack(side="bottom", fill="x", padx=12, pady=16)
        tk.Label(box, text=self.user.get_name(), font=(FONT, 11, "bold"),
                 fg="white", bg="#312e81").pack(anchor="w", padx=12, pady=(10, 0))
        tk.Label(box, text=self.user.get_role().capitalize() + " · " + self.user.get_info(),
                 font=(FONT, 9), fg="#c4b5fd", bg="#312e81").pack(anchor="w", padx=12)
        tk.Button(box, text="Logout", command=self.app.show_login, bg="white", fg=DEEP,
                  activebackground=LIGHT, activeforeground=DEEP, relief="flat", bd=0,
                  font=(FONT, 10, "bold"), pady=5, cursor="hand2"
                  ).pack(fill="x", padx=12, pady=10)

    def build_content(self):
        content = tk.Frame(self, bg=BG)
        content.pack(side="left", fill="both", expand=True, padx=24, pady=20)

        self.heading = tk.Label(content, font=(FONT, 20, "bold"), fg=DEEP, bg=BG)
        self.heading.pack(anchor="w")

        # dashboard cards
        cards = tk.Frame(content, bg=BG)
        cards.pack(fill="x", pady=14)
        self.card_labels = []
        for i, title in enumerate(self.card_titles):
            cards.columnconfigure(i, weight=1, uniform="card")
            card = tk.Frame(cards, bg="white")
            card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0))
            tk.Frame(card, bg=ACCENT, width=5).pack(side="left", fill="y")
            inner = tk.Frame(card, bg="white")
            inner.pack(side="left", padx=14, pady=10)
            tk.Label(inner, text=title, font=(FONT, 10), fg=GRAY, bg="white").pack(anchor="w")
            value = tk.Label(inner, text="0", font=(FONT, 24, "bold"), fg=PRIMARY, bg="white")
            value.pack(anchor="w")
            self.card_labels.append(value)

        # task table
        panel = tk.Frame(content, bg="white")
        panel.pack(fill="both", expand=True)
        wrap = tk.Frame(panel, bg="white")
        wrap.pack(fill="both", expand=True, padx=12, pady=(12, 0))
        names = [name for name, width in self.columns]
        self.table = ttk.Treeview(wrap, columns=names, show="headings", selectmode="browse")
        for name, width in self.columns:
            self.table.heading(name, text=name)
            self.table.column(name, width=width, anchor="w")
        scroll = ttk.Scrollbar(wrap, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.table.bind("<<TreeviewSelect>>", self.show_description)

        self.desc = tk.Label(panel, text="", font=(FONT, 10), fg=GRAY, bg="white",
                             anchor="w", justify="left", wraplength=760)
        self.desc.pack(fill="x", padx=14, pady=8)
        actions = tk.Frame(panel, bg="white")
        actions.pack(fill="x", padx=12, pady=(0, 12))
        self.build_actions(actions)

    def make_button(self, parent, text, command, color=PRIMARY):
        button = tk.Button(parent, text=text, command=command, bg=color, fg="white",
                           activebackground=color, activeforeground="white",
                           relief="flat", bd=0, padx=16, pady=7,
                           font=(FONT, 10, "bold"), cursor="hand2")
        button.pack(side="left", padx=(0, 8))
        return button

    # ----- common behaviour -----
    def set_active(self, key):
        for name, button in self.nav_buttons.items():
            if name == key:
                button.config(bg="white", fg=DEEP, activebackground="white",
                              activeforeground=DEEP)
            else:
                button.config(bg=DEEP, fg="#ddd6fe", activebackground=PRIMARY,
                              activeforeground="white")

    def refresh(self):
        """Reload the table and cards from the TaskManager."""
        for item in self.table.get_children():
            self.table.delete(item)
        tasks = self.get_tasks()
        for task in tasks:
            self.table.insert("", "end", iid=str(task.id), values=self.get_row(task))
        for label, value in zip(self.card_labels, self.get_card_values()):
            label.config(text=str(value))
        self.heading.config(text=self.get_heading())
        self.desc.config(text="Select a task to see its description." if tasks
                         else "No tasks to show.")

    def selected_task(self):
        """Return the Task selected in the table (or None)."""
        selection = self.table.selection()
        if not selection:
            messagebox.showinfo("Select a task", "Please select a task from the table first.")
            return None
        return self.manager.get_task(int(selection[0]))

    def show_description(self, event=None):
        selection = self.table.selection()
        if selection:
            task = self.manager.get_task(int(selection[0]))
            if task is not None:
                self.desc.config(text="Description: " + task.description)


# ---------------------------------------------------------------
# TeacherDashboard: add, view, edit, delete
# ---------------------------------------------------------------
class TeacherDashboard(Dashboard):
    columns = [("ID", 50), ("Task", 220), ("Course", 210), ("Type", 110),
               ("Deadline", 100), ("Completed", 90)]
    card_titles = ["Total Tasks", "Courses", "Students"]
    start_view = "dashboard"

    def nav_items(self):
        return [("dashboard", "Dashboard", self.refresh),
                ("add", "Add Task", self.add_task)]

    def build_actions(self, frame):
        self.make_button(frame, "+ Add Task", self.add_task)
        self.make_button(frame, "Edit", self.edit_task)
        self.make_button(frame, "Delete", self.delete_task, "#dc2626")

    def student_count(self):
        return len([u for u in self.app.users if u.get_role() == "student"])

    def get_row(self, task):
        return (task.id, task.title, task.course, task.task_type, task.deadline,
                str(len(task.completed_by)) + "/" + str(self.student_count()))

    def get_card_values(self):
        tasks = self.manager.get_all_tasks()
        return [len(tasks), len({t.course for t in tasks}), self.student_count()]

    def get_heading(self):
        return "Teacher Dashboard"

    def check_teacher(self):
        """Role check. Every teacher-only action calls this first."""
        if not self.user.can_manage_tasks():
            messagebox.showerror("Access denied", "Only teachers can do this.")
            return False
        return True

    def add_task(self):
        if self.check_teacher():
            TaskDialog(self, "Add New Task", None, self.save_new)

    def save_new(self, values):
        if self.check_teacher():
            self.manager.add_task(*values)
            self.refresh()

    def edit_task(self):
        if not self.check_teacher():
            return
        task = self.selected_task()
        if task is not None:
            TaskDialog(self, "Edit Task", task,
                       lambda values: self.save_edit(task.id, values))

    def save_edit(self, task_id, values):
        if self.check_teacher():
            self.manager.edit_task(task_id, *values)
            self.refresh()

    def delete_task(self):
        if not self.check_teacher():
            return
        task = self.selected_task()
        if task is not None and messagebox.askyesno(
                "Delete task", "Delete '" + task.title + "'?"):
            self.manager.delete_task(task.id)
            self.refresh()


# ---------------------------------------------------------------
# StudentDashboard: view tasks and mark them completed
# ---------------------------------------------------------------
class StudentDashboard(Dashboard):
    columns = [("ID", 50), ("Task", 220), ("Course", 210), ("Type", 110),
               ("Deadline", 100), ("Status", 90)]
    card_titles = ["Total Tasks", "Completed", "Pending"]
    start_view = "all"

    def nav_items(self):
        return [("all", "All Tasks", lambda: self.set_view("all")),
                ("pending", "Pending Tasks", lambda: self.set_view("pending")),
                ("completed", "Completed Tasks", lambda: self.set_view("completed"))]

    def build_actions(self, frame):
        self.make_button(frame, "Mark as Completed", self.mark_completed, "#16a34a")

    def set_view(self, view):
        self.view = view
        self.set_active(view)
        self.refresh()

    def is_done(self, task):
        return task.is_completed_by(self.user.get_username())

    def get_tasks(self):
        tasks = self.manager.get_all_tasks()
        if self.view == "completed":
            return [t for t in tasks if self.is_done(t)]
        if self.view == "pending":
            return [t for t in tasks if not self.is_done(t)]
        return tasks

    def get_row(self, task):
        return (task.id, task.title, task.course, task.task_type, task.deadline,
                "Completed" if self.is_done(task) else "Pending")

    def get_card_values(self):
        tasks = self.manager.get_all_tasks()
        done = len([t for t in tasks if self.is_done(t)])
        return [len(tasks), done, len(tasks) - done]

    def get_heading(self):
        headings = {"all": "Student Dashboard", "pending": "Pending Tasks",
                    "completed": "Completed Tasks"}
        return headings[self.view]

    def mark_completed(self):
        task = self.selected_task()
        if task is None:
            return
        if self.is_done(task):
            messagebox.showinfo("Already done", "You already completed this task.")
            return
        self.manager.mark_completed(task.id, self.user.get_username())
        self.refresh()


# ---------------------------------------------------------------
# TaskDialog: the Add / Edit window (used by the teacher)
# ---------------------------------------------------------------
class TaskDialog(tk.Toplevel):
    def __init__(self, parent, heading, task, on_save):
        super().__init__(parent)
        self.title(heading)
        self.configure(bg="white")
        self.resizable(False, False)
        self.on_save = on_save

        tk.Label(self, text=heading, font=(FONT, 16, "bold"), fg=DEEP, bg="white"
                 ).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 8))

        self.title_entry = self.add_entry(1, "Task Title")
        self.course_entry = self.add_entry(3, "Course Name")

        tk.Label(self, text="Task Type", font=(FONT, 10, "bold"), bg="white"
                 ).grid(row=5, column=0, sticky="w", padx=24)
        self.type_box = ttk.Combobox(self, values=TASK_TYPES, state="readonly", width=44)
        self.type_box.grid(row=6, column=0, sticky="ew", padx=24, pady=(2, 8), ipady=3)

        self.deadline_entry = self.add_entry(7, "Deadline (YYYY-MM-DD)")

        tk.Label(self, text="Description", font=(FONT, 10, "bold"), bg="white"
                 ).grid(row=9, column=0, sticky="w", padx=24)
        self.desc_text = tk.Text(self, width=46, height=4, font=(FONT, 11), relief="flat",
                                 highlightthickness=1, highlightbackground="#cbd5e1",
                                 highlightcolor=PRIMARY)
        self.desc_text.grid(row=10, column=0, padx=24, pady=(2, 4))

        self.error = tk.Label(self, text="", fg="#dc2626", bg="white", font=(FONT, 10))
        self.error.grid(row=11, column=0, sticky="w", padx=24)

        buttons = tk.Frame(self, bg="white")
        buttons.grid(row=12, column=0, sticky="w", padx=24, pady=(4, 20))
        tk.Button(buttons, text="Save Task", command=self.save, bg=PRIMARY, fg="white",
                  activebackground=DEEP, activeforeground="white", relief="flat", bd=0,
                  font=(FONT, 10, "bold"), padx=18, pady=7, cursor="hand2"
                  ).pack(side="left", padx=(0, 8))
        tk.Button(buttons, text="Cancel", command=self.destroy, bg="#94a3b8", fg="white",
                  activebackground="#64748b", activeforeground="white", relief="flat", bd=0,
                  font=(FONT, 10, "bold"), padx=18, pady=7, cursor="hand2"
                  ).pack(side="left")

        if task is not None:                 # Edit: fill the old values
            self.title_entry.insert(0, task.title)
            self.course_entry.insert(0, task.course)
            self.type_box.set(task.task_type)
            self.deadline_entry.insert(0, task.deadline)
            self.desc_text.insert("1.0", task.description)

        self.transient(parent.winfo_toplevel())
        self.wait_visibility()
        self.grab_set()                      # block the main window until closed
        self.title_entry.focus_set()

    def add_entry(self, row, label):
        tk.Label(self, text=label, font=(FONT, 10, "bold"), bg="white"
                 ).grid(row=row, column=0, sticky="w", padx=24)
        entry = tk.Entry(self, width=46, font=(FONT, 11), relief="flat",
                         highlightthickness=1, highlightbackground="#cbd5e1",
                         highlightcolor=PRIMARY)
        entry.grid(row=row + 1, column=0, padx=24, pady=(2, 8), ipady=4)
        return entry

    def save(self):
        values = (self.title_entry.get().strip(), self.course_entry.get().strip(),
                  self.type_box.get().strip(), self.deadline_entry.get().strip(),
                  self.desc_text.get("1.0", "end-1c").strip())
        if not all(values):
            self.error.config(text="Please fill in all fields.")
            return
        try:
            datetime.strptime(values[3], "%Y-%m-%d")
        except ValueError:
            self.error.config(text="Deadline must look like 2026-12-31.")
            return
        self.on_save(values)
        self.destroy()


if __name__ == "__main__":
    App().mainloop()