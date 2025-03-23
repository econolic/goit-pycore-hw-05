import sys
from collections import Counter

def parse_log_line(line: str) -> dict:
    """
    Парсить один рядок логу в компоненти: дата, час, рівень, повідомлення.
    Очікуваний формат рядка: "<дата> <час> <рівень> <повідомлення>"
    Повертає словник із ключами: date, time, level, message, або None, якщо рядок невалідний.
    """
    line = line.strip()
    if not line:
        return None
    parts = line.split()
    if len(parts) < 3:
        return None
    date = parts[0]
    time = parts[1]
    level = parts[2]
    message = ' '.join(parts[3:]) if len(parts) > 3 else ''
    return {"date": date, "time": time, "level": level, "message": message}

def load_logs(file_path: str) -> list:
    """
    Завантажує та парсить лог-файл за вказаною адресою.
    Повертає список записів логу (словників), отриманих із parse_log_line.
    """
    logs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            entry = parse_log_line(line)
            if entry:
                logs.append(entry)
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Фільтрує список записів логу за вказаним рівнем (нечутливо до регістру).
    Повертає список записів, які відповідають заданому рівню.
    """
    level_upper = level.upper()
    return [log for log in logs if log["level"].upper() == level_upper]

def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів логу для кожного рівня.
    Повертає словник, де ключі — рівні логування, а значення — їхня кількість.
    """
    levels = [log["level"] for log in logs]
    return dict(Counter(levels))

def display_log_counts(counts: dict):
    """
    Виводить підрахунки записів для кожного рівня у табличному форматі.
    """
    print(f"{'Рівень':<8} | Кількість")
    print("-" * 20)
    for level in sorted(counts):
        count = counts[level]
        print(f"{level:<8} | {count}")

def main():
    # Перевірка аргументів командного рядка
    if len(sys.argv) < 2:
        print("Помилка: не вказано файл журналу логів.")
        print("Використання: python task3.py <шлях_до_лог_файлу> [<рівень_логування>]")
        sys.exit(1)
    if len(sys.argv) > 3:
        print("Помилка: надто багато аргументів.")
        print("Використання: python task3.py <шлях_до_лог_файлу> [<рівень_логування>]")
        sys.exit(1)

    log_file_path = sys.argv[1]
    filter_level = sys.argv[2].upper() if len(sys.argv) == 3 else None

    # Завантаження логів із обробкою помилок
    try:
        logs = load_logs(log_file_path)
    except FileNotFoundError:
        print(f"Помилка: файл '{log_file_path}' не знайдено.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Помилка: не вдалося декодувати файл '{log_file_path}'. Перевірте кодування.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка: не вдалося прочитати файл. {e}")
        sys.exit(1)

    # Перевірка, чи є валідні записи
    if not logs:
        print("Попередження: файл журналу порожній або не містить валідних записів.")
        sys.exit(0)

    # Підрахунок і вивід кількості записів за рівнями
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # Фільтрація за рівнем, якщо вказано
    if filter_level:
        known_levels = set(counts.keys())
        if filter_level not in known_levels:
            print(f"\nПопередження: рівень '{filter_level}' не знайдено у логах.")
        else:
            filtered_logs = filter_logs_by_level(logs, filter_level)
            if not filtered_logs:
                print(f"\nНемає записів рівня {filter_level}.")
            else:
                print(f"\nЗаписи рівня {filter_level}:")
                print("-" * 50)
                for entry in filtered_logs:
                    print(f"{entry['date']} {entry['time']} - {entry['message']}")

if __name__ == "__main__":
    main()