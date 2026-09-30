# Personal Student Expense Tracker (CLI)

## Project Overview
The **Personal Student Expense Tracker** is a lightweight, pure-Python command-line application designed specifically for university students to log daily expenses, monitor monthly budget thresholds, track category spending via ASCII charts, and manage hostel bill splits with roommates.

Built entirely using Python's standard library modules (`sqlite3`, `hashlib`, `csv`, `datetime`, `json`), it provides a zero-dependency, self-contained financial management solution tailored to academic life.

---

## Features
- **User Authentication & Profile Management**: Secure registration and login using SHA-256 password hashing, alongside configurable monthly budget limits.
- **Expense CRUD Operations**: Log, view, filter, and delete expenses categorized across typical student spending areas (Food, Academics, Rent, Travel, Mess, etc.).
- **Visual Budget & Analytics Engine**: Rendered ASCII progress bars showing spending proportion per category alongside dynamic monthly budget warnings (Safe, 80% Threshold Warning, Over-Budget Alert).
- **Hostel Bill Splitter Module**: Share group expenses (e.g., room rent, Wi-Fi) across roommates, auto-calculating individual shares and total money owed back to you.
- **Data Exporting**: Export all personalized expense records directly into a standard `CSV` file for external auditing or portfolio record-keeping.

---

## Technologies & Tools Used
- **Programming Language**: Python 3 (3.8+)
- **Database**: SQLite3 (via built-in `sqlite3` module)
- **Security & Cryptography**: SHA-256 hashing (via built-in `hashlib` module)
- **Data Processing & I/O**: `csv`, `json`, `datetime`, `sys`

---

## System File Architecture
```text
student-expense-tracker/
├── main.py          # Entry point containing CLI menu loops and user dashboard
├── models.py        # SQLite schema initialization, user auth, and expense CRUD
├── analytics.py     # ASCII bar chart generator, budget checker, and CSV exporter
├── splitter.py      # Hostel/roommate bill division logic and history viewer
├── statement.md     # Project problem statement, scope, target audience, and feature list
└── README.md        # Documentation, setup, and usage guide