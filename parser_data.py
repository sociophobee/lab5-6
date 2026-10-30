import requests
import json
import csv


def fetch_world_bank_data(countries: str, indicator: str, start_year: int, end_year: int):
    """
    Формує URL-адресу та надсилає HTTP-запит до API Світового банку.
    """
    url = (
        f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
        f"?date={start_year}:{end_year}&format=json&per_page=500"
    )
    print(f"Надсилаю запит за адресою:\n{url}\n")

    try:
        response = requests.get(url, timeout=15)
        # Перевірка успішності виконання запиту за кодом відповіді сервера
        if response.status_code == 200:
            print(f"Запит виконано успішно (status_code: {response.status_code}).")
            data = response.json()
            # API Світового банку повертає список: [метадані, сам список записів]
            if isinstance(data, list) and len(data) > 1 and data[1] is not None:
                return data[1]
            else:
                print("Дані за заданими параметрами відсутні у відповіді API.")
                return None
        else:
            print(f"Помилка сервера! Код відповіді: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Помилка під час виконання HTTP-запиту: {e}")
        return None


def save_to_json(data, filename: str) -> bool:
    """
    Зберігає отримані дані у файл формату JSON.
    """
    try:
        with open(filename, mode="w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Дані успішно збережено у JSON-файл '{filename}'.")
        return True
    except (IOError, OSError, TypeError) as e:
        print(f"Помилка під час збереження JSON-файлу '{filename}': {e}")
        return False


def convert_json_to_csv(json_filename: str, csv_filename: str) -> bool:
    """
    Зчитує JSON-файл, виділяє потрібні поля та зберігає їх у CSV-файл.
    """
    try:
        with open(json_filename, mode="r", encoding="utf-8") as json_file:
            raw_data = json.load(json_file)
    except FileNotFoundError:
        print(f"Помилка: файл '{json_filename}' не знайдено.")
        return False
    except json.JSONDecodeError as e:
        print(f"Помилка декодування JSON із файлу '{json_filename}': {e}")
        return False
    except (IOError, OSError) as e:
        print(f"Помилка читання файлу '{json_filename}': {e}")
        return False

    extracted_rows = []
    for entry in raw_data:
        country_name = entry.get("country", {}).get("value", "")
        country_code = entry.get("countryiso3code", "")
        series_name = entry.get("indicator", {}).get("value", "")
        series_code = entry.get("indicator", {}).get("id", "")
        year = entry.get("date", "")
        value = entry.get("value", "")

        if value is None:
            value_str = ".."
        else:
            value_str = f"{value:.3f}"

        extracted_rows.append([
            country_name,
            country_code,
            series_name,
            series_code,
            year,
            value_str
        ])

    # Сортуємо за кодом країни та роком
    extracted_rows.sort(key=lambda x: (x[1], x[4]))

    headers = [
        "Country Name",
        "Country Code",
        "Series Name",
        "Series Code",
        "Year",
        "Value"
    ]

    try:
        with open(csv_filename, mode="w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(headers)
            writer.writerows(extracted_rows)
        print(f"Дані успішно перетворено та збережено у CSV-файл '{csv_filename}'.")
        return True
    except (IOError, OSError, csv.Error) as e:
        print(f"Помилка під час запису у CSV-файл '{csv_filename}': {e}")
        return False


def display_file_content(filename: str):
    """
    Виводить вміст файлу на екран.
    """
    print("\n" + "=" * 70)
    print(f"ВМІСТ ФАЙЛУ: {filename}")
    print("=" * 70)
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            print(file.read())
    except Exception as e:
        print(f"Не вдалося прочитати файл: {e}")


def main():
    # Параметри для Варіанту 13: США та Україна, 2010–2019 рр.
    countries = "us;ua"
    indicator = "SP.DYN.LE00.IN"
    start_year = 2010
    end_year = 2019

    json_file = "world_bank_le_us_ua.json"
    csv_file = "world_bank_le_us_ua.csv"

    # Крок 1: Завантаження даних через API
    records = fetch_world_bank_data(countries, indicator, start_year, end_year)

    if records:
        # Крок 2: Збереження у JSON
        if save_to_json(records, json_file):
            # Крок 3: Конвертація у CSV
            if convert_json_to_csv(json_file, csv_file):
                # Крок 4: Виведення результатів на екран
                display_file_content(json_file)
                display_file_content(csv_file)


if __name__ == "__main__":
    main()