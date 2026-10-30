import csv


def compare_countries_data(input_csv: str, output_csv: str):
    """
    Зчитує дані з CSV-файлу, зіставляє показники США та України за роками,
    виконує їхнє порівняння та записує результат у новий CSV-файл.
    """
    # 1. Читання вихідного CSV-файлу з обробкою помилок (try-except)
    try:
        with open(input_csv, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            data = list(reader)
        print(f"Файл '{input_csv}' успішно прочитано.")
    except FileNotFoundError:
        print(f"Помилка: файл '{input_csv}' не знайдено. Спершу запустіть parser_data.py.")
        return
    except (IOError, OSError, csv.Error) as e:
        print(f"Помилка під час читання файлу '{input_csv}': {e}")
        return

    # 2. Групуємо дані за роками для зручного порівняння
    yearly_data = {}

    for row in data:
        country_code = row.get("Country Code", "").strip().upper()
        year = row.get("Year", "").strip()
        value_str = row.get("Value", "").strip()

        if year not in yearly_data:
            yearly_data[year] = {}

        try:
            val_float = float(value_str)
        except ValueError:
            val_float = None

        if country_code == "USA":
            yearly_data[year]["USA"] = value_str
            yearly_data[year]["USA_val"] = val_float
        elif country_code in ("UKR", "UA"):
            yearly_data[year]["UKR"] = value_str
            yearly_data[year]["UKR_val"] = val_float

    # 3. Виконуємо порівняння показників
    comparison_results = []
    
    for year in sorted(yearly_data.keys()):
        usa_val_str = yearly_data[year].get("USA", "..")
        ukr_val_str = yearly_data[year].get("UKR", "..")
        
        usa_val = yearly_data[year].get("USA_val")
        ukr_val = yearly_data[year].get("UKR_val")

        if usa_val is not None and ukr_val is not None:
            diff = usa_val - ukr_val
            if diff > 0:
                comparison = f"США вище на {diff:.3f} років"
            elif diff < 0:
                comparison = f"Україна вище на {abs(diff):.3f} років"
            else:
                comparison = "Показники рівні"
        else:
            comparison = "Недостатньо даних для порівняння"

        comparison_results.append({
            "Year": year,
            "USA Life Expectancy": usa_val_str,
            "Ukraine Life Expectancy": ukr_val_str,
            "Comparison Result": comparison
        })

    # 4. Запис результатів у новий CSV-файл з обробкою помилок
    headers = ["Year", "USA Life Expectancy", "Ukraine Life Expectancy", "Comparison Result"]
    
    try:
        with open(output_csv, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")
            writer.writeheader()
            writer.writerows(comparison_results)
        print(f"Результати порівняння успішно записано у новий файл '{output_csv}'.")
    except (IOError, OSError, csv.Error) as e:
        print(f"Помилка під час запису у файл '{output_csv}': {e}")
        return

    # 5. Виведення результатів порівняння на екран у вигляді таблиці
    print("\n" + "=" * 95)
    print(f"{'Рік':<6} | {'США (років)':<18} | {'Україна (років)':<18} | {'Результат порівняння':<38}")
    print("=" * 95)
    for row in comparison_results:
        print(
            f"{row['Year']:<6} | "
            f"{row['USA Life Expectancy']:<18} | "
            f"{row['Ukraine Life Expectancy']:<18} | "
            f"{row['Comparison Result']:<38}"
        )
    print("=" * 95)


if __name__ == "__main__":
    input_file = "world_bank_le_us_ua.csv"
    output_file = "world_bank_comparison_us_ua.csv"
    
    compare_countries_data(input_file, output_file)