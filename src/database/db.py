import sqlite3
from sqlite3 import Connection
from datetime import datetime

def get_connection(db_name: str = "shelter.db") -> Connection:
    return sqlite3.connect(db_name)

def create_tables(db_name: str = "shelter.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Role (
            role_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            role_id INTEGER,
            FOREIGN KEY (role_id) REFERENCES Role(role_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Species (
            species_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Status (
            status_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MedicalCard (
            medical_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT,
            description TEXT,
            date DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Animals (
            animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species_id INTEGER,
            gender TEXT,
            age INTEGER,
            size TEXT,
            features TEXT,
            status_id INTEGER,
            photo TEXT,
            medical_card_id INTEGER,
            FOREIGN KEY (species_id) REFERENCES Species(species_id),
            FOREIGN KEY (status_id) REFERENCES Status(status_id),
            FOREIGN KEY (medical_card_id) REFERENCES MedicalCard(medical_card_id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_sample_data(db_name: str = "shelter.db"):
    conn = get_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Role")
    if cursor.fetchone()[0] == 0:
        roles = [
            (1, "Гость"),
            (2, "Работник приюта")
        ]
        cursor.executemany("INSERT OR IGNORE INTO Role (role_id, name) VALUES (?, ?)", roles)

    cursor.execute("SELECT COUNT(*) FROM Users")
    if cursor.fetchone()[0] == 0:
        users = [
            ("guest", "123", "guest@shelter.ru", 1),
            ("employee", "123", "employee@shelter.ru", 2),
            ("admin", "admin123", "admin@shelter.ru", 2)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Users (login, password, email, role_id) VALUES (?, ?, ?, ?)", users)

    cursor.execute("SELECT COUNT(*) FROM Species")
    if cursor.fetchone()[0] == 0:
        species = [
            (1, "Собака"),
            (2, "Кошка"),
            (3, "Кролик"),
            (4, "Птица")
        ]
        cursor.executemany("INSERT OR IGNORE INTO Species (species_id, name) VALUES (?, ?)", species)

    cursor.execute("SELECT COUNT(*) FROM Status")
    if cursor.fetchone()[0] == 0:
        statuses = [
            (1, "Доступен в любое время"),
            (2, "Пристроен"),
            (3, "На лечении")
        ]
        cursor.executemany("INSERT OR IGNORE INTO Status (status_id, name) VALUES (?, ?)", statuses)

    cursor.execute("SELECT COUNT(*) FROM MedicalCard")
    if cursor.fetchone()[0] == 0:
        medical_cards = [
            ("Лечение", ""),
            ("Вакцинация", "Завершено", "Плановая вакцинация", "15-01-2024"),
            ("Стерилизация", "Завершено", "Плановая операция", "02-01-2025"),
            ("Осмотр", "В процессе", "Регулярный осмотр", "03-12-2025"),
            ("Лечение", "Завершено", "Лечение от паразитов", "02.06.2023")
        ]
        cursor.executemany("INSERT OR IGNORE INTO MedicalCard (title, status, description, date) VALUES (?, ?, ?, ?)", medical_cards)

    cursor.execute("SELECT COUNT(*) FROM Animals")
    if cursor.fetchone()[0] == 0:
        animals = [
            ("Барсик", 2, "М", 2, "Маленький", "Ласковый, игривый", 1, "https:", 1),
            ("Шарик", 1, "М", 4, "Большой", "Дружелюбный, любит детей", 1, "https:", 2),
            ("Мурка", 2, "Ж", 3, "Средний", "Спокойная", 3, "https:", 3),
            ("Кексик", 3, "М", 1, "Маленький", "Пушистый", 1, "https:", 4),
            ("Рекс", 1, "М", 5, "Большой", "Любит детей, очень спокойный", 2, "https:", 5)
        ]
        cursor.executemany("""INSERT INTO Animals (name, species_id, gender, age, size, features, status_id, photo, medical_card_id) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", animals)

    conn.commit()
    conn.close()