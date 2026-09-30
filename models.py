import sqlite3
import hashlib
from datetime import datetime

DB_FILE = "student_tracker.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            monthly_budget REAL DEFAULT 0.0
        )
    ''')
    
    # Expenses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Split Bills Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS split_bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            total_amount REAL NOT NULL,
            per_person REAL NOT NULL,
            roommates_count INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class UserManager:
    @staticmethod
    def register(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        pwd_hash = hash_password(password)
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pwd_hash))
            conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already exists."
        finally:
            conn.close()

    @staticmethod
    def login(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        pwd_hash = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, pwd_hash))
        user = cursor.fetchone()
        conn.close()
        if user:
            return user
        return None

    @staticmethod
    def update_budget(user_id, amount):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET monthly_budget = ? WHERE id = ?", (amount, user_id))
        conn.commit()
        conn.close()

class ExpenseManager:
    @staticmethod
    def add_expense(user_id, amount, category, description):
        conn = get_db_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, description, today)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_expenses(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC", (user_id,))
        expenses = cursor.fetchall()
        conn.close()
        return expenses

    @staticmethod
    def delete_expense(expense_id, user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0