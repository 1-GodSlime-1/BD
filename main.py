from src.database.db import create_tables, insert_sample_data
from src.repository.repository import Repository

DB_FILE = "shelter.db"

print("Тестовые аккаунты:")
print("Админ: login: admin, password: admin123 (может управлять пользователями)")
print("Работник: login: employee, password: 123")
print("Гость: login: guest, password: 123")

def main_menu():
    print("\n=== Приют животных ===")
    print("1 - Вход в систему")
    print("2 - Регистрация")
    print("0 - Выход")
    return input("Ваш выбор: ")


def login():
    print("\n=== Вход в систему ===")
    print("1 - Вход по логину")
    print("2 - Вход по почте")
    login_choice = input("Выберите способ входа: ")
    if login_choice == "1":
        identifier = input("Логин: ")
        login_type = "login"
    elif login_choice == "2":
        identifier = input("Почта: ")
        login_type = "email"
    else:
        print("Неверный выбор")
        return None, None, None

    password = input("Пароль: ")

    return identifier, password, login_type


def regist(repo):
    while True:
        login = input("Придумайте логин: ")
        if repo.check_login_exists(login):
            print("Этот логин уже занят. Попробуйте другой.")
            continue
        break

    while True:
        email = input("Введите email: ")
        if repo.check_email_exists(email):
            print("Этот email уже занят. Попробуйте другой.")
            continue
        break
    password = input("Придумайте пароль: ")
    print("\nДоступные роли:")
    print("1 - Гость (только просмотр)")
    print("2 - Работник приюта (требует подтверждения администратора)")

    role_choice = input("Выберите роль (1 или 2): ")
    if role_choice == "1":
        role_id = 1
    else:
        role_id = 1
        print("Роль 'Работник приюта' требует подтверждения администратора. Вы зарегистрированы как Гость.")

    if repo.register_user(login, password, email, role_id):
        print("\nРегистрация прошла успешно! Теперь вы можете войти в систему.")
        return True
    else:
        print("\nОшибка при регистрации. Попробуйте снова.")
        return False


def guest_menu(repo):
    while True:
        print("\n=== Меню гостя ===")
        print("1 - Показать всех животных")
        print("2 - Поиск животных по виду")
        print("3 - Показать доступных животных")
        print("4 - Показать информацию о животном")
        print("0 - Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":
            animals = repo.get_all_animals()
            print("\nСписок всех животных:")
            for animal in animals:
                species = repo.get_species(animal.species_id)
                status = repo.get_status(animal.status_id)
                print(f"{animal.animal_id}: {animal.name} ({species.name}) - {status.name}")

        elif choice == "2":
            species_list = repo.get_all_species()
            print("\nДоступные виды:")
            for species in species_list:
                print(f"{species.species_id}: {species.name}")

            try:
                species_id = int(input("Выберите ID вида: "))
                animals = repo.get_animals_by_species(species_id)
                if animals:
                    print(f"\nЖивотные этого вида:")
                    for animal in animals:
                        status = repo.get_status(animal.status_id)
                        print(f"{animal.animal_id}: {animal.name} - {status.name}")
                else:
                    print("Животных этого вида не найдено.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "3":
            animals = repo.get_available_animals()
            print("\nДоступные для пристройства животные:")
            if animals:
                for animal in animals:
                    species = repo.get_species(animal.species_id)
                    print(f"{animal.animal_id}: {animal.name} ({species.name}), {animal.age} лет, {animal.size}")
                    if animal.features:
                        print(f"   Особенности: {animal.features}")
            else:
                print("Нет доступных животных.")

        elif choice == "4":
            animals = repo.get_all_animals_with_details()
            print("\nСписок всех животных:")
            for animal in animals:
                print(f"ID: {animal.animal_id}, Кличка: {animal.name}")
            try:
                animal_id = int(input("Введите ID животного: "))
                animal = repo.get_animal_details(animal_id)
                if animal:
                    print(f"\nПодробная информация:")
                    print(f"Кличка: {animal.name}")
                    print(f"Вид: {animal.species_name}")
                    print(f"Пол: {animal.gender}")
                    print(f"Возраст: {animal.age} лет")
                    print(f"Размер: {animal.size}")
                    print(f"Статус: {animal.status_name}")
                    if animal.features:
                        print(f"Особенности: {animal.features}")
                    if animal.medical_info:
                        print(f"Мед. информация: {animal.medical_info}")
                else:
                    print("Животное не найдено.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "0":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def employee_menu(repo, current_user):
    while True:
        print(f"\n=== Меню работника приюта ===")
        print("1 - Показать всех животных")
        print("2 - Добавить животное")
        print("3 - Редактировать информацию животного")
        print("4 - Изменить статус животного")
        print("5 - Показать медицинские карты")
        if current_user.login == "admin":
            print("6 - Управление пользователями")
        print("0 - Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":
            animals = repo.get_all_animals_with_details()
            print("\nСписок всех животных:")
            for animal in animals:
                print(f"ID: {animal.animal_id}, Кличка: {animal.name}, Вид: {animal.species_name}, "
                      f"Статус: {animal.status_name}, Возраст: {animal.age}")

        elif choice == "2":
            print("\nДобавление нового животного:")
            name = input("Кличка: ")

            species_list = repo.get_all_species()
            print("Доступные виды:")
            for species in species_list:
                print(f"{species.species_id}: {species.name}")
            species_id = int(input("ID вида: "))

            gender = input("Пол: ")
            age = int(input("Возраст: "))
            size = input("Размер: ")
            features = input("Особенности (можно оставить пустым): ")

            status_list = repo.get_all_statuses()
            print("Доступные статусы:")
            for status in status_list:
                print(f"{status.status_id}: {status.name}")
            status_id = int(input("ID статуса: "))

            photo = input("URL фото (можно оставить пустым): ")

            if repo.add_animal(name, species_id, gender, age, size, features, status_id, photo):
                print("Животное успешно добавлено!")
            else:
                print("Ошибка при добавлении животного.")

        elif choice == "3":
            animals = repo.get_all_animals_with_details()
            print("\nСписок всех животных:")
            for animal in animals:
                print(f"ID: {animal.animal_id}, Кличка: {animal.name}, Вид: {animal.species_name}, "
                      f"Статус: {animal.status_name}, Возраст: {animal.age}")
            try:
                animal_id = int(input("Введите ID животного для редактирования: "))
                animal = repo.get_animal(animal_id)
                if animal:
                    print(f"Текущие данные: {animal.name}, возраст: {animal.age}, размер: {animal.size}")

                    new_name = input(f"Новая кличка [{animal.name}]: ") or animal.name
                    new_age = input(f"Новый возраст [{animal.age}]: ") or animal.age
                    new_size = input(f"Новый размер [{animal.size}]: ") or animal.size
                    new_features = input(f"Новые особенности [{animal.features or 'нет'}]: ") or animal.features

                    if repo.update_animal(animal_id, new_name, int(new_age), new_size, new_features):
                        print("Данные животного обновлены!")
                    else:
                        print("Ошибка при обновлении.")
                else:
                    print("Животное не найдено.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "4":
            animals = repo.get_all_animals_with_details()
            print("\nСписок всех животных:")
            for animal in animals:
                print(f"ID: {animal.animal_id}, Кличка: {animal.name}, Вид: {animal.species_name}, "
                      f"Статус: {animal.status_name}, Возраст: {animal.age}")
            try:
                animal_id = int(input("Введите ID животного: "))
                status_list = repo.get_all_statuses()
                print("Доступные статусы:")
                for status in status_list:
                    print(f"{status.status_id}: {status.name}")
                new_status_id = int(input("Новый ID статуса: "))

                if repo.update_animal_status(animal_id, new_status_id):
                    print("Статус животного обновлен!")
                else:
                    print("Ошибка при обновлении статуса.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "5":
            medical_records = repo.get_all_medical_records()
            print("\nМедицинские карты:")
            for record in medical_records:
                animal = repo.get_animal_by_medical_id(record.medical_card_id)
                animal_name = animal.name if animal else "Неизвестно"
                print(f"Карта ID: {record.medical_card_id}, Животное: {animal_name}, "
                      f"Название: {record.title}, Статус: {record.status}")

        elif choice == "6" and current_user.login == "admin":
            admin_user_management(repo)

        elif choice == "0":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def admin_user_management(repo):
    while True:
        print("\n=== Управление пользователями ===")
        print("1 - Показать всех пользователей")
        print("2 - Изменить роль пользователя")
        print("3 - Удалить пользователя")
        print("0 - Назад")
        choice = input("Ваш выбор: ")

        if choice == "1":
            users = repo.get_all_users()
            print("\nСписок пользователей:")
            for user in users:
                role = repo.get_role(user.role_id)
                print(f"ID: {user.user_id}, Логин: {user.login}, Email: {user.email}, Роль: {role.name}")

        elif choice == "2":
            try:
                user_id = int(input("ID пользователя: "))
                new_role_id = int(input("Новая роль (1-Гость, 2-Работник): "))
                if repo.update_user_role(user_id, new_role_id):
                    print("Роль пользователя обновлена!")
                else:
                    print("Ошибка при обновлении роли.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "3":
            try:
                user_id = int(input("ID пользователя для удаления: "))
                if user_id == 1:
                    print("Нельзя удалить администратора!")
                    continue
                if repo.delete_user(user_id):
                    print("Пользователь удален!")
                else:
                    print("Ошибка при удалении пользователя.")
            except ValueError:
                print("Неверный ввод.")

        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def main():
    create_tables(DB_FILE)
    insert_sample_data(DB_FILE)

    repo = Repository(DB_FILE)

    while True:
        choice = main_menu()

        if choice == "1":
            identifier, password, login_type = login()
            if identifier and password and login_type:
                user = repo.authenticate_user(identifier, password, login_type)

                if user:
                    print(f"\nДобро пожаловать, {user.login}!")
                    if user.role_id == 1:
                        guest_menu(repo)
                    elif user.role_id == 2:
                        employee_menu(repo, user)
                else:
                    print("Неверный логин/почта или пароль. Попробуйте снова.")

        elif choice == "2":
            regist(repo)

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

    repo.close()


if __name__ == "__main__":
    main()