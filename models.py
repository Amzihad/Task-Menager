"""models.py - All OOP classes for SUPERNOVA.

Classes: User, Teacher, Student, Task, TaskManager
"""
import json
import os


# ---------------------------------------------------------------
# USER CLASSES  (Inheritance: Teacher and Student inherit from User)
# ---------------------------------------------------------------
class User:
    """Parent class. Holds the data every user has."""

    def __init__(self, username, password, name):  # Constructor
        # Two underscores make these attributes private (Encapsulation).
        # Outside code cannot read them directly, only through methods.
        self.__username = username
        self.__password = password
        self.__name = name

    def get_username(self):
        return self.__username

    def get_name(self):
        return self.__name

    def check_password(self, password):
        return self.__password == password

    # These methods are overridden in the child classes.
    def get_role(self):
        return "user"

    def get_info(self):
        return ""

    def can_manage_tasks(self):
        return False


class Teacher(User):
    """Child class. A teacher can add, edit and delete tasks."""

    def __init__(self, username, password, name, department):
        super().__init__(username, password, name)  # call the parent constructor
        self.__department = department

    def get_role(self):  # Method overriding
        return "teacher"

    def get_info(self):
        return "Dept: " + self.__department

    def can_manage_tasks(self):
        return True


class Student(User):
    """Child class. A student can only view tasks and mark them completed."""

    def __init__(self, username, password, name, student_id):
        super().__init__(username, password, name)
        self.__student_id = student_id

    def get_role(self):
        return "student"

    def get_info(self):
        return "ID: " + self.__student_id


# ---------------------------------------------------------------
# TASK CLASS  (one object = one task)
# ---------------------------------------------------------------
class Task:
    """Stores the information of one academic task."""

    def __init__(self, task_id, title, course, task_type, deadline,
                 description, completed_by=None):
        self.__id = task_id
        self.__title = title
        self.__course = course
        self.__task_type = task_type
        self.__deadline = deadline          # text like "2026-12-01"
        self.__description = description
        # usernames of the students who finished this task
        self.__completed_by = completed_by if completed_by else []

    # Read-only getters (properties), so templates can write task.title
    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def course(self):
        return self.__course

    @property
    def task_type(self):
        return self.__task_type

    @property
    def deadline(self):
        return self.__deadline

    @property
    def description(self):
        return self.__description

    @property
    def completed_by(self):
        return list(self.__completed_by)    # return a copy to keep data safe

    def update(self, title, course, task_type, deadline, description):
        """Change the task details (used by the teacher's Edit)."""
        self.__title = title
        self.__course = course
        self.__task_type = task_type
        self.__deadline = deadline
        self.__description = description

    def mark_completed(self, username):
        if username not in self.__completed_by:
            self.__completed_by.append(username)

    def is_completed_by(self, username):
        return username in self.__completed_by

    def to_dict(self):
        """Convert the object to a dictionary so it can be saved as JSON."""
        return {
            "id": self.__id,
            "title": self.__title,
            "course": self.__course,
            "task_type": self.__task_type,
            "deadline": self.__deadline,
            "description": self.__description,
            "completed_by": self.__completed_by,
        }


# ---------------------------------------------------------------
# TASK MANAGER CLASS  (keeps all tasks and saves them to JSON)
# ---------------------------------------------------------------
class TaskManager:
    """Manages the list of Task objects and the JSON file."""

    def __init__(self, filename):
        self.__filename = filename
        self.__tasks = []
        self.load()                          # read saved tasks at start-up

    def load(self):
        """Read tasks from the JSON file and create Task objects."""
        self.__tasks = []
        if not os.path.exists(self.__filename):
            return
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return                           # empty or broken file -> start empty
        for item in data:
            task = Task(item["id"], item["title"], item["course"],
                        item["task_type"], item["deadline"],
                        item["description"], item.get("completed_by", []))
            self.__tasks.append(task)

    def save(self):
        """Write all tasks to the JSON file."""
        folder = os.path.dirname(self.__filename)
        if folder:
            os.makedirs(folder, exist_ok=True)
        data = [task.to_dict() for task in self.__tasks]
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def get_all_tasks(self):
        """Return all tasks, earliest deadline first."""
        return sorted(self.__tasks, key=lambda task: task.deadline)

    def get_task(self, task_id):
        for task in self.__tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(self, title, course, task_type, deadline, description):
        new_id = max([task.id for task in self.__tasks], default=0) + 1
        self.__tasks.append(Task(new_id, title, course, task_type,
                                 deadline, description))
        self.save()

    def edit_task(self, task_id, title, course, task_type, deadline, description):
        task = self.get_task(task_id)
        if task is None:
            return False
        task.update(title, course, task_type, deadline, description)
        self.save()
        return True

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            return False
        self.__tasks.remove(task)
        self.save()
        return True

    def mark_completed(self, task_id, username):
        task = self.get_task(task_id)
        if task is None:
            return False
        task.mark_completed(username)
        self.save()
        return True
