"""Консольное меню сервиса учёта удобрений. Практическая работа 2."""

from copy import deepcopy

from services import (
    add_fertilizer, add_plant, cancel_application, create_application,
    find_applications, get_item, get_statistics, sort_applications,
)
from storage import DATA_FILE, load_data, save_data
from utils import (
    get_fertilizer_name, get_plant_name, read_date, read_id, read_number,
    read_text,
)

MENU = """
1 — Добавить растение
2 — Добавить удобрение и его запас
3 — Показать растения и удобрения
4 — Записать применение удобрения
5 — Показать журнал применений
6 — Отменить ошибочную запись о применении
7 — Найти применения по названию
8 — Отсортировать журнал
9 — Показать статистику
0 — Выход
"""


def show_catalogs(data: dict) -> None:
    """Показывает номера объектов для дальнейшего выбора."""
    print("\nРастения:")
    for key, plant in data["plants"].items():
        print(f'{key}: {plant["name"]}')
    if not data["plants"]:
        print("Пока нет растений. Добавьте их через пункт 1.")
    print("Удобрения:")
    for key, fertilizer in data["fertilizers"].items():
        print(f'{key}: {fertilizer["name"]}; '
              f'остаток {fertilizer["stock_ml"]:g} мл')
    if not data["fertilizers"]:
        print("Пока нет удобрений. Добавьте их через пункт 2.")


def show_applications(data: dict, records: list[dict]) -> None:
    """Выводит журнал или результат поиска."""
    if not records:
        print("Записей нет.")
    for record in records:
        plant = get_item(data["plants"], record["plant_id"])["name"]
        fertilizer = get_item(data["fertilizers"], record["fertilizer_id"])
        print(f'№ {record["id"]} | {record["date"]} | {plant} | '
              f'{fertilizer["name"]} | {record["dosage_ml"]:g} мл')


def change_data(data: dict, choice: str) -> str:
    """Меняет копию данных; меню сохранит её только при успехе."""
    if choice == "1":
        number = add_plant(data, get_plant_name())
        return f"Добавлено растение № {number}."
    if choice == "2":
        name = get_fertilizer_name()
        stock = read_number("Сколько удобрения в наличии, мл: ")
        number = add_fertilizer(data, name, stock)
        return f"Добавлено удобрение № {number}."
    if choice == "4":
        if not data["plants"] or not data["fertilizers"]:
            raise ValueError("Сначала добавьте растение и удобрение.")
        show_catalogs(data)
        plant_id = read_id("Номер растения: ")
        fertilizer_id = read_id("Номер удобрения: ")
        dosage = read_number("Количество удобрения, мл: ")
        application_date = read_date()
        record = create_application(data, plant_id, fertilizer_id,
                                    dosage, application_date)
        return f'Применение № {record["id"]} записано.'
    if not data["applications"]:
        raise ValueError("Журнал пуст, отменять нечего.")
    show_applications(data, data["applications"])
    number = read_id("Номер ошибочной записи для отмены: ")
    cancel_application(data, number)
    return "Запись отменена; учтённое количество возвращено в запас."


def show_result(data: dict, choice: str) -> None:
    """Выполняет действия меню, которые не меняют данные."""
    if choice == "3":
        show_catalogs(data)
    elif choice == "5":
        show_applications(data, data["applications"])
    elif choice == "7":
        query = read_text("Часть названия растения или удобрения: ")
        show_applications(data, list(find_applications(data, query)))
    elif choice == "8":
        option = input("1 — по дате, 2 — по дозировке: ").strip()
        if option not in ("1", "2"):
            raise ValueError("Выберите 1 или 2.")
        field = "date" if option == "1" else "dosage_ml"
        show_applications(data, sort_applications(data["applications"], field))
    elif choice == "9":
        result = get_statistics(data)
        print(f'Применений: {result["applications"]}')
        print(f'Растений в журнале: {result["plants_used"]}')
        for key, amount in result["usage_ml"].items():
            name = data["fertilizers"][key]["name"]
            print(f"{name}: использовано {amount:g} мл")
    else:
        print("Нет такого пункта. Введите число от 0 до 9.")


def main() -> None:
    """Загружает данные и повторяет меню до команды выхода."""
    print("СЕРВИС УЧЁТА УДОБРЕНИЙ ДЛЯ РАСТЕНИЙ — ПР2")
    print("Учёт жидких удобрений в мл. Дозировку берите из инструкции.")
    print(f"Файл данных: {DATA_FILE}")
    try:
        data = load_data()
    except (OSError, ValueError, UnicodeError) as error:
        print(f"Не удалось прочитать данные: {error}")
        print("Проверьте JSON или восстановите его из резервной копии.")
        print("Программа завершена, исходный файл не изменён.")
        return
    while True:
        print(MENU)
        try:
            choice = input("Выберите пункт: ").strip()
            if choice == "0":
                print("Работа завершена. Успешные изменения уже сохранены.")
                break
            if choice in ("1", "2", "4", "6"):
                candidate = deepcopy(data)
                message = change_data(candidate, choice)
                save_data(candidate)
                data = candidate
                print(message)
            else:
                show_result(data, choice)
        except (ValueError, OSError, UnicodeError) as error:
            print(f"Операция не выполнена: {error}")
        except (KeyboardInterrupt, EOFError):
            print("\nВыход. Незавершённая операция не сохранена.")
            break


if __name__ == "__main__":
    main()
