import sqlite3
from datetime import datetime

DB_NAME = "mitra_ai.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # Uploaded documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_time TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, role="user"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )

    conn.commit()
    conn.close()


def validate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def save_document(filename):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO documents (filename, upload_time) VALUES (?, ?)",
        (filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


def get_documents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents")

    docs = cursor.fetchall()
    conn.close()

    return docs