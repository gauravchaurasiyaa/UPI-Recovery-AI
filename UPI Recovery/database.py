import sqlite3
import os

DATABASE = os.path.join("database", "recovery.db")


def get_connection():
    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT,
            issue_type TEXT NOT NULL,
            description TEXT,
            analysis TEXT,
            guidance TEXT,
            complaint TEXT,
            status TEXT DEFAULT 'Submitted',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def create_case(data):

    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO cases (
            transaction_id,
            amount,
            transaction_date,
            issue_type,
            description,
            analysis,
            guidance,
            complaint
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["transaction_id"],
        data["amount"],
        data["transaction_date"],
        data["issue_type"],
        data["description"],
        data["analysis"],
        data["guidance"],
        data["complaint"]
    ))

    case_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return case_id


def get_all_cases():

    connection = get_connection()

    cases = connection.execute(
        "SELECT * FROM cases ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return cases


def get_case(case_id):

    connection = get_connection()

    case = connection.execute(
        "SELECT * FROM cases WHERE id = ?",
        (case_id,)
    ).fetchone()

    connection.close()

    return case


def update_case_status(case_id, status):

    allowed_statuses = [
        "Submitted",
        "Under Review",
        "Resolved",
        "Rejected"
    ]

    if status not in allowed_statuses:
        return False

    connection = get_connection()

    cursor = connection.execute(
        "UPDATE cases SET status = ? WHERE id = ?",
        (status, case_id)
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated