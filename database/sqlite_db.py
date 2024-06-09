# <---------- Импорт функций ---------->
import sqlite3
import json
from datetime import datetime


# <---------- Функции работы с базой данных---------->
class Database:
    def __init__(self, db_name='tasks.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER UNIQUE,
                    username TEXT UNIQUE,
                    registered TEXT,
                    tasks TEXT
                )
            """)

    def add_user(self, user_id, username):
        with self.connection:
            self.cursor.execute(
                "INSERT OR IGNORE INTO users (id, username, registered, tasks) VALUES (?, ?, ?, ?)",
                (user_id, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), json.dumps([]))
            )
            self.connection.commit()

    def get_user(self, user_id):
        self.cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()

    def add_task(self, user_id, task):
        user = self.get_user(user_id)
        if user:
            tasks = json.loads(user[3])
            tasks.append(task)
            with self.connection:
                self.cursor.execute(
                    "UPDATE users SET tasks = ? WHERE id = ?",
                    (json.dumps(tasks), user_id)
                )
                self.connection.commit()

    def remove_task(self, user_id, task_index):
        user = self.get_user(user_id)
        if user:
            tasks = json.loads(user[3])
            if 0 <= task_index < len(tasks):
                tasks.pop(task_index)
                with self.connection:
                    self.cursor.execute(
                        "UPDATE users SET tasks = ? WHERE id = ?",
                        (json.dumps(tasks), user_id)
                    )
                    self.connection.commit()

    def get_tasks(self, user_id):
        user = self.get_user(user_id)
        if user:
            return json.loads(user[3])
        return []
