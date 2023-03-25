import sqlite3
from sqlite3 import Error

DB_NAME = "data/reports.db"

def create_connection():
    """Создает подключение к базе данных SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except Error as e:
        print(e)

    return conn

def init_db():
    """Инициализирует базу данных, создает таблицу reports, если она не существует."""
    conn = create_connection()
    if conn is not None:
        try:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    sprint_number INTEGER NOT NULL,
                    report_text TEXT NOT NULL,
                    submission_date TIMESTAMP NOT NULL
                )"""
            )

def add_report(user_id, sprint_number, report_text, submission_date):
    """Добавляет отчет в базу данных."""
    conn = create_connection()
    if conn is not None:
        try:
            conn.execute(
                "INSERT INTO reports (user_id, sprint_number, report_text, submission_date) VALUES (?, ?, ?, ?)",
                (user_id, sprint_number, report_text, submission_date),
            )
            conn.commit()
        except Error as e:
            print(e)

def get_reports_for_sprint(sprint_number):
    """Извлекает все отчеты для указанного спринта."""
    conn = create_connection()
    reports = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reports WHERE sprint_number=?", (sprint_number,))

            reports = cursor.fetchall()
        except Error as e:
            print(e)

    return reports