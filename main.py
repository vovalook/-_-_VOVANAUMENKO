from datetime import date


def get_plant_name():
    """Получение названия растения."""
    plant_name = input("Введите название растения: ")

    if plant_name == "":
        print("Название растения не может быть пустым.")
        return "Не указано"

    return plant_name


def get_fertilizer_name():
    """Получение названия удобрения."""
    fertilizer_name = input("Введите название удобрения: ")

    if fertilizer_name == "":
        print("Название удобрения не может быть пустым.")
        return "Не указано"

    return fertilizer_name


def check_dosage(dosage):
    """Проверка дозировки удобрения."""
    if dosage <= 0:
        return "Дозировка должна быть больше 0 мл."
    elif dosage <= 50:
        return "Дозировка подходит для растения."
    else:
        return "Внимание! Дозировка слишком большая."


print("======================================")
print(" СЕРВИС УЧЕТА УДОБРЕНИЙ ДЛЯ РАСТЕНИЙ")
print("======================================")

plant = get_plant_name()
fertilizer = get_fertilizer_name()

dosage = float(input("Введите дозировку удобрения в мл: "))

application_date = date.today()

print()
print(" Информация о применении ")
print("Растение:", plant)
print("Удобрение:", fertilizer)
print("Дозировка:", dosage, "мл")
print("Дата применения:", application_date)
print("Результат:", check_dosage(dosage))
