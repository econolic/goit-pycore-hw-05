from typing import Callable

def generator_numbers(text: str):
    """
    Генератор, який знаходить і повертає всі дійсні числа у тексті.
    
    Аргументи:
        text (str): Текст, що містить числа, відокремлені пробілами.
    
    Повертає:
        generator: Генератор, що видає дійсні числа з тексту.
    """
    words = text.split()  # Розбиваємо текст на слова за пробілами
    for word in words:
        try:
            number = float(word)  # Спроба конвертувати слово у float
            yield number         # Якщо успішно, видаємо число
        except ValueError:
            pass                 # Якщо не число, пропускаємо

def sum_profit(text: str, func: Callable):
    """
    Обчислює загальну суму чисел у тексті, використовуючи заданий генератор.
    
    Аргументи:
        text (str): Текст, що містить числа.
        func (Callable): Функція-генератор, яка повертає числа з тексту.
    
    Повертає:
        float: Загальна сума чисел.
    """
    total = sum(func(text))  # Підсумовуємо всі числа з генератора
    return total

# Приклад використання:
if __name__ == "__main__":
     # Приклад 1: Текст з числами
    text = ("Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, "
            "доповнений додатковими надходженнями 27.45 і 324.00 доларів.")
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")

    # Приклад 2: Текст без чисел
    text_empty = "Цей текст не містить числових значень."
    total_empty = sum_profit(text_empty, generator_numbers)
    print(f"Загальний дохід: {total_empty}") 