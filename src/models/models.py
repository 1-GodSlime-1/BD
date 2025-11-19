class User:
    def __init__(self, user_id, login, password, email, role_id):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.email = email
        self.role_id = role_id

class Role:
    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name

class Animal:
    def __init__(self, animal_id, name, species_id, gender, age, size, features, status_id, photo, medical_card_id):
        self.animal_id = animal_id
        self.name = name
        self.species_id = species_id
        self.gender = gender
        self.age = age
        self.size = size
        self.features = features
        self.status_id = status_id
        self.photo = photo
        self.medical_card_id = medical_card_id

class Species:
    def __init__(self, species_id, name):
        self.species_id = species_id
        self.name = name

class Status:
    def __init__(self, status_id, name):
        self.status_id = status_id
        self.name = name

class MedicalCard:
    def __init__(self, medical_card_id, title, status, description, date):
        self.medical_card_id = medical_card_id
        self.title = title
        self.status = status
        self.description = description
        self.date = date

class AnimalDetails:
    def __init__(self, animal_id, name, species_name, gender, age, size, features, status_name, medical_info):
        self.animal_id = animal_id
        self.name = name
        self.species_name = species_name
        self.gender = gender
        self.age = age
        self.size = size
        self.features = features
        self.status_name = status_name
        self.medical_info = medical_info