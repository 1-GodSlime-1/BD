import sqlite3
from src.models.models import User, Role, Animal, Species, Status, MedicalCard, AnimalDetails


class Repository:
    def __init__(self, db_file: str = "shelter.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def authenticate_user(self, identifier: str, password: str, login_type: str):
        if login_type == "login":
            query = "SELECT user_id, login, password, email, role_id FROM Users WHERE login = ? AND password = ?"
        else:
            query = "SELECT user_id, login, password, email, role_id FROM Users WHERE email = ? AND password = ?"

        self.cursor.execute(query, (identifier, password))
        row = self.cursor.fetchone()
        if row:
            return User(user_id=row["user_id"], login=row["login"], password=row["password"],
                        email=row["email"], role_id=row["role_id"])
        return None

    def check_login_exists(self, login: str):
        self.cursor.execute("SELECT user_id FROM Users WHERE login = ?", (login,))
        return self.cursor.fetchone() is not None

    def check_email_exists(self, email: str):
        self.cursor.execute("SELECT user_id FROM Users WHERE email = ?", (email,))
        return self.cursor.fetchone() is not None

    def register_user(self, login: str, password: str, email: str, role_id: int):
        try:
            self.cursor.execute("""INSERT INTO Users (login, password, email, role_id) 
                                VALUES (?, ?, ?, ?)""",
                                (login, password, email, role_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при регистрации пользователя: {e}")
            return False

    def get_all_users(self):
        self.cursor.execute("SELECT user_id, login, password, email, role_id FROM Users")
        rows = self.cursor.fetchall()
        return [User(user_id=row["user_id"], login=row["login"], password=row["password"],
                     email=row["email"], role_id=row["role_id"]) for row in rows]

    def get_role(self, role_id: int):
        self.cursor.execute("SELECT role_id, name FROM Role WHERE role_id = ?", (role_id,))
        row = self.cursor.fetchone()
        if row:
            return Role(role_id=row["role_id"], name=row["name"])
        return None

    def update_user_role(self, user_id: int, new_role_id: int):
        try:
            self.cursor.execute("UPDATE Users SET role_id = ? WHERE user_id = ?",
                                (new_role_id, user_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при изменении роли: {e}")
            return False

    def delete_user(self, user_id: int):
        try:
            self.cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")
            return False

    def get_all_animals(self):
        self.cursor.execute(
            "SELECT animal_id, name, species_id, gender, age, size, features, status_id, photo, medical_card_id FROM Animals")
        rows = self.cursor.fetchall()
        return [Animal(animal_id=row["animal_id"], name=row["name"], species_id=row["species_id"],
                       gender=row["gender"], age=row["age"], size=row["size"],
                       features=row["features"], status_id=row["status_id"],
                       photo=row["photo"], medical_card_id=row["medical_card_id"]) for row in rows]

    def get_animal(self, animal_id: int):
        self.cursor.execute(
            "SELECT animal_id, name, species_id, gender, age, size, features, status_id, photo, medical_card_id FROM Animals WHERE animal_id = ?",
            (animal_id,))
        row = self.cursor.fetchone()
        if row:
            return Animal(animal_id=row["animal_id"], name=row["name"], species_id=row["species_id"],
                          gender=row["gender"], age=row["age"], size=row["size"],
                          features=row["features"], status_id=row["status_id"],
                          photo=row["photo"], medical_card_id=row["medical_card_id"])
        return None

    def get_all_animals_with_details(self):
        query = """
            SELECT a.animal_id, a.name, s.name as species_name, a.gender, a.age, 
                   a.size, a.features, st.name as status_name, m.description as medical_info
            FROM Animals a
            LEFT JOIN Species s ON a.species_id = s.species_id
            LEFT JOIN Status st ON a.status_id = st.status_id
            LEFT JOIN MedicalCard m ON a.medical_card_id = m.medical_card_id
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [AnimalDetails(animal_id=row["animal_id"], name=row["name"], species_name=row["species_name"],
                              gender=row["gender"], age=row["age"], size=row["size"],
                              features=row["features"], status_name=row["status_name"],
                              medical_info=row["medical_info"]) for row in rows]

    def get_animal_details(self, animal_id: int):
        query = """
            SELECT a.animal_id, a.name, s.name as species_name, a.gender, a.age, 
                   a.size, a.features, st.name as status_name, m.description as medical_info
            FROM Animals a
            LEFT JOIN Species s ON a.species_id = s.species_id
            LEFT JOIN Status st ON a.status_id = st.status_id
            LEFT JOIN MedicalCard m ON a.medical_card_id = m.medical_card_id
            WHERE a.animal_id = ?
        """
        self.cursor.execute(query, (animal_id,))
        row = self.cursor.fetchone()
        if row:
            return AnimalDetails(animal_id=row["animal_id"], name=row["name"], species_name=row["species_name"],
                                 gender=row["gender"], age=row["age"], size=row["size"],
                                 features=row["features"], status_name=row["status_name"],
                                 medical_info=row["medical_info"])
        return None

    def get_available_animals(self):
        self.cursor.execute("""SELECT animal_id, name, species_id, gender, age, size, features, status_id, photo, medical_card_id 
                            FROM Animals WHERE status_id = 1""")
        rows = self.cursor.fetchall()
        return [Animal(animal_id=row["animal_id"], name=row["name"], species_id=row["species_id"],
                       gender=row["gender"], age=row["age"], size=row["size"],
                       features=row["features"], status_id=row["status_id"],
                       photo=row["photo"], medical_card_id=row["medical_card_id"]) for row in rows]

    def get_animals_by_species(self, species_id: int):
        self.cursor.execute("""SELECT animal_id, name, species_id, gender, age, size, features, status_id, photo, medical_card_id 
                            FROM Animals WHERE species_id = ?""", (species_id,))
        rows = self.cursor.fetchall()
        return [Animal(animal_id=row["animal_id"], name=row["name"], species_id=row["species_id"],
                       gender=row["gender"], age=row["age"], size=row["size"],
                       features=row["features"], status_id=row["status_id"],
                       photo=row["photo"], medical_card_id=row["medical_card_id"]) for row in rows]

    def get_species(self, species_id: int):
        self.cursor.execute("SELECT species_id, name FROM Species WHERE species_id = ?", (species_id,))
        row = self.cursor.fetchone()
        if row:
            return Species(species_id=row["species_id"], name=row["name"])
        return None

    def get_all_species(self):
        self.cursor.execute("SELECT species_id, name FROM Species")
        rows = self.cursor.fetchall()
        return [Species(species_id=row["species_id"], name=row["name"]) for row in rows]

    def get_status(self, status_id: int):
        self.cursor.execute("SELECT status_id, name FROM Status WHERE status_id = ?", (status_id,))
        row = self.cursor.fetchone()
        if row:
            return Status(status_id=row["status_id"], name=row["name"])
        return None

    def get_all_statuses(self):
        self.cursor.execute("SELECT status_id, name FROM Status")
        rows = self.cursor.fetchall()
        return [Status(status_id=row["status_id"], name=row["name"]) for row in rows]

    def add_animal(self, name, species_id, gender, age, size, features, status_id, photo):
        try:
            self.cursor.execute("""INSERT INTO Animals (name, species_id, gender, age, size, features, status_id, photo) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                (name, species_id, gender, age, size, features, status_id, photo))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении животного: {e}")
            return False

    def update_animal(self, animal_id, name, age, size, features):
        try:
            self.cursor.execute("""UPDATE Animals SET name = ?, age = ?, size = ?, features = ? 
                                WHERE animal_id = ?""",
                                (name, age, size, features, animal_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении животного: {e}")
            return False

    def update_animal_status(self, animal_id, status_id):
        try:
            self.cursor.execute("UPDATE Animals SET status_id = ? WHERE animal_id = ?",
                                (status_id, animal_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении статуса: {e}")
            return False

    def get_all_medical_records(self):
        self.cursor.execute("SELECT medical_card_id, title, status, description, date FROM MedicalCard")
        rows = self.cursor.fetchall()
        return [MedicalCard(medical_card_id=row["medical_card_id"], title=row["title"], status=row["status"],
                            description=row["description"], date=row["date"]) for row in rows]

    def get_animal_by_medical_id(self, medical_card_id: int):
        self.cursor.execute("SELECT animal_id, name FROM Animals WHERE medical_card_id = ?",
                            (medical_card_id,))
        row = self.cursor.fetchone()
        if row:
            return Animal(animal_id=row["animal_id"], name=row["name"], species_id=None, gender=None,
                          age=None, size=None, features=None, status_id=None, photo=None,
                          medical_card_id=medical_card_id)
        return None

    def add_medical_record(self, animal_id, title, status, description):
        try:
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")

            self.cursor.execute("""INSERT INTO MedicalCard (title, status, description, date) 
                                VALUES (?, ?, ?, ?)""",
                                (title, status, description, current_date))

            medical_card_id = self.cursor.lastrowid

            self.cursor.execute("UPDATE Animals SET medical_card_id = ? WHERE animal_id = ?",
                                (medical_card_id, animal_id))

            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении медицинской записи: {e}")
            return False

    def close(self):
        self.conn.close()