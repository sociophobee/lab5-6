import json


def save_dict_to_json(data_dict: dict, filename: str) -> bool:
    """
    Зберігає словник Python у JSON-файл з обробкою винятків.
    """
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(data_dict, file, ensure_ascii=False, indent=4)
        print(f"Словник успішно збережено у файл '{filename}'.")
        return True
    except (IOError, OSError, TypeError) as e:
        print(f"Помилка під час збереження файлу '{filename}': {e}")
        return False


def display_json_file(filename: str):
    """
    Зчитує та виводить зміст JSON-файлу на екран.
    """
    print("\n" + "=" * 65)
    print(f"ВМІСТ JSON-ФАЙЛУ: {filename}")
    print("=" * 65)
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Помилка: файл '{filename}' не знайдено.")
    except (IOError, OSError) as e:
        print(f"Помилка під час читання файлу '{filename}': {e}")


def search_by_field(source_filename: str, output_filename: str, field_name: str, search_value):
    """
    Виконує пошук записів у JSON-файлі за вказаним полем словника
    та зберігає результати у новий JSON-файл.
    """
    try:
        with open(source_filename, mode="r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
        print(f"Помилка під час відкриття або читання '{source_filename}': {e}")
        return

    # Виконуємо пошук за заданим полем
    found_records = {}
    for key, info in data.items():
        if isinstance(info, dict) and str(info.get(field_name, "")).lower() == str(search_value).lower():
            found_records[key] = info

    print(f"\nПошук за полем '{field_name}' = '{search_value}': знайдено записів — {len(found_records)}")

    if save_dict_to_json(found_records, output_filename):
        display_json_file(output_filename)


def main():
    # Словник Python (дані з Практичної роботи №3)
    students_dict = {
        "Студент_1": {"Прізвище": "Рєзнік", "Ім'я": "Дмитро", "Курс": 2, "Спеціальність": "Комп'ютерні науки", "Середній_бал": 92.5},
        "Студент_2": {"Прізвище": "Кравченко", "Ім'я": "Денис", "Курс": 1, "Спеціальність": "Комп'ютерні науки", "Середній_бал": 88.0},
        "Студент_3": {"Прізвище": "Антонов", "Ім'я": "Олександр", "Курс": 1, "Спеціальність": "Комп'ютерні науки", "Середній_бал": 90.0},
        "Студент_4": {"Прізвище": "Коваленко", "Ім'я": "Ірина", "Курс": 2, "Спеціальність": "Кібербезпека", "Середній_бал": 85.4},
        "Студент_5": {"Прізвище": "Мельник", "Ім'я": "Максим", "Курс": 2, "Спеціальність": "Програмна інженерія", "Середній_бал": 91.2}
    }

    initial_json = "dictionary_data.json"
    filtered_json = "search_results.json"

    # 1. Збереження словника у JSON-файл та виведення на екран
    if save_dict_to_json(students_dict, initial_json):
        display_json_file(initial_json)

        # 2. Пошук даних за полем 'Спеціальність' та збереження у новий JSON-файл
        search_by_field(
            source_filename=initial_json,
            output_filename=filtered_json,
            field_name="Спеціальність",
            search_value="Комп'ютерні науки"
        )


if __name__ == "__main__":
    main()