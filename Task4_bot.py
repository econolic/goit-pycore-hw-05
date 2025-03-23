import logging
from colorama import Fore, Style, init

# Ініціалізація colorama для автоматичного скидання кольорів
init(autoreset=True)

# Налаштування логування помилок
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

# Декоратор для обробки помилок
def input_error(func):
    """
    Перехоплює помилки введення та повертає кольорові повідомлення.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logging.error(f"ValueError in {func.__name__}: {e}")
            return Fore.RED + str(e)
        except KeyError as e:
            logging.error(f"KeyError in {func.__name__}: {e}")
            return Fore.RED + str(e)
        except IndexError as e:
            logging.error(f"IndexError in {func.__name__}: {e}")
            return Fore.RED + str(e)
    return inner

# Парсинг введення користувача
def parse_input(user_input):
    """
    Розбиває введення на команду та аргументи.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, contacts):
    """
    Додає новий контакт. Очікує ім'я та телефон.
    """
    if len(args) != 2:
        raise ValueError("Будь ласка, вкажіть ім'я та телефон.")
    name, phone = args
    contacts[name] = phone
    return Fore.GREEN + "Контакт додано."

@input_error
def change_contact(args, contacts):
    """
    Змінює телефон контакту. Очікує ім'я та новий телефон.
    """
    if len(args) != 2:
        raise ValueError("Будь ласка, вкажіть ім'я та телефон.")
    name, new_phone = args
    if name not in contacts:
        raise KeyError("Контакт не знайдено. Спочатку додайте його.")
    contacts[name] = new_phone
    return Fore.GREEN + "Контакт оновлено."

@input_error
def show_phone(args, contacts):
    """
    Показує телефон за ім'ям. Очікує лише ім'я.
    """
    if len(args) != 1:
        raise IndexError("Вкажіть лише ім'я користувача.")
    name = args[0]
    if name not in contacts:
        raise KeyError("Контакт не знайдено. Спочатку додайте його.")
    return Fore.BLUE + contacts[name]

def show_all(contacts):
    """
    Показує всі контакти.
    """
    if not contacts:
        return Fore.YELLOW + "Контактів не знайдено."
    return Fore.BLUE + "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def show_help():
    """
    Виводить список доступних команд.
    """
    commands = {
        "hello": "Виводить привітання",
        "add [name] [phone]": "Додає новий контакт",
        "change [name] [phone]": "Змінює номер телефону контакту",
        "phone [name]": "Показує номер телефону за ім'ям",
        "all": "Виводить усі контакти",
        "help": "Показує список команд",
        "close або exit": "Завершує програму"
    }
    help_text = "Доступні команди:\n"
    for cmd, desc in commands.items():
        help_text += f"  {cmd}: {desc}\n"
    return Fore.CYAN + help_text

def main():
    contacts = {}
    print(Fore.GREEN + "Ласкаво просимо до бота-асистента!")
    while True:
        user_input = input(Fore.WHITE + "Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(Fore.GREEN + "До побачення!")
            break
        elif command == "hello":
            print(Fore.BLUE + "Як я можу вам допомогти?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "help":
            print(show_help())
        else:
            print(Fore.RED + "Невірна команда.")

if __name__ == "__main__":
    main()