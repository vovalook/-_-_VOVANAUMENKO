"""Действия с объектами растений, удобрений и применений."""

from models import Application, Fertilizer, Plant
from utils import clean_name


def empty_data() -> dict:
    """Создаёт пустые коллекции объектов и счётчик применений."""
    return {"plants": {}, "fertilizers": {}, "applications": [],
            "next_application_id": 1}


def get_item(items: dict[int, object], item_id: int) -> object:
    """Ищет объект по номеру."""
    if item_id not in items:
        raise ValueError("Запись с таким номером не найдена.")
    return items[item_id]


def next_catalog_id(items: dict[int, object]) -> int:
    """Возвращает следующий номер для справочника."""
    return max(items, default=0) + 1


def check_unique_name(items: dict[int, object], name: str) -> str:
    """Проверяет, что название не повторяется."""
    name = clean_name(name)
    for item in items.values():
        if item.name.casefold() == name.casefold():
            raise ValueError("Такое название уже есть в списке.")
    return name


def add_plant(data: dict, name: str) -> int:
    """Создаёт объект Plant и добавляет его в справочник."""
    name = check_unique_name(data["plants"], name)
    item_id = next_catalog_id(data["plants"])
    data["plants"][item_id] = Plant(item_id, name)
    return item_id


def add_fertilizer(data: dict, name: str, stock_ml: float) -> int:
    """Создаёт объект Fertilizer и добавляет его в справочник."""
    if stock_ml <= 0:
        raise ValueError("Начальный запас должен быть больше нуля.")
    name = check_unique_name(data["fertilizers"], name)
    item_id = next_catalog_id(data["fertilizers"])
    data["fertilizers"][item_id] = Fertilizer(item_id, name, stock_ml)
    return item_id


def check_dosage(dosage: float, available_ml: float) -> None:
    """Проверяет дозировку через объект Fertilizer."""
    temporary = Fertilizer(1, "Проверка", available_ml)
    temporary.spend(dosage)


def create_application(data: dict, plant_id: int, fertilizer_id: int,
                       dosage: float, application_date: str) -> Application:
    """Создаёт объект Application и уменьшает остаток удобрения."""
    get_item(data["plants"], plant_id)
    fertilizer = get_item(data["fertilizers"], fertilizer_id)
    record = Application(data["next_application_id"], plant_id, fertilizer_id,
                         dosage, application_date)
    fertilizer.spend(record.dosage_ml)
    data["applications"].append(record)
    data["next_application_id"] += 1
    return record


def cancel_application(data: dict, application_id: int) -> None:
    """Отменяет ошибочную запись и возвращает учтённый расход в запас."""
    for index, record in enumerate(data["applications"]):
        if record.record_id == application_id:
            fertilizer = get_item(data["fertilizers"], record.fertilizer_id)
            fertilizer.restore(record.dosage_ml)
            del data["applications"][index]
            return
    raise ValueError("Применение с таким номером не найдено.")


def find_applications(data: dict, query: str):
    """Генератор: ищет записи по части названия растения или удобрения."""
    query = clean_name(query).casefold()
    for record in data["applications"]:
        plant = get_item(data["plants"], record.plant_id)
        fertilizer = get_item(data["fertilizers"], record.fertilizer_id)
        plant_match = query in plant.name.casefold()
        fertilizer_match = query in fertilizer.name.casefold()
        if plant_match or fertilizer_match:
            yield record


def sort_applications(records: list[Application],
                      field: str) -> list[Application]:
    """Возвращает новый список, отсортированный по дате или дозировке."""
    if field not in ("date", "dosage_ml"):
        raise ValueError("Сортировать можно по дате или дозировке.")
    return sorted(records, key=lambda record: getattr(record, field))


def get_statistics(data: dict) -> dict:
    """Считает записи и расход отдельно для каждого удобрения."""
    usage = {}
    for record in data["applications"]:
        key = record.fertilizer_id
        usage[key] = usage.get(key, 0) + record.dosage_ml
    used_plants = {record.plant_id for record in data["applications"]}
    return {"applications": len(data["applications"]),
            "plants_used": len(used_plants), "usage_ml": usage}
