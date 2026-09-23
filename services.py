"""Действия с растениями, удобрениями и журналом применений."""

from math import isfinite

from utils import clean_name, parse_date


def empty_data() -> dict:
    """Создаёт пустые коллекции и счётчик номеров применений."""
    return {"plants": {}, "fertilizers": {}, "applications": [],
            "next_application_id": 1}


def get_item(items: dict, item_id: int) -> dict:
    """Ищет объект по номеру. В JSON ключи словаря — строки."""
    key = str(item_id)
    if key not in items:
        raise ValueError("Запись с таким номером не найдена.")
    return items[key]


def add_named_item(items: dict, name: str, **fields) -> int:
    """Добавляет объект с уникальным названием и новым номером."""
    name = clean_name(name)
    for item in items.values():
        if item["name"].casefold() == name.casefold():
            raise ValueError("Такое название уже есть в списке.")
    item_id = max((int(key) for key in items), default=0) + 1
    items[str(item_id)] = {"name": name, **fields}
    return item_id


def add_plant(data: dict, name: str) -> int:
    """Добавляет растение в справочник."""
    return add_named_item(data["plants"], name)


def add_fertilizer(data: dict, name: str, stock_ml: float) -> int:
    """Добавляет жидкое удобрение и его исходный запас в мл."""
    if not isfinite(stock_ml) or stock_ml <= 0:
        raise ValueError("Начальный запас должен быть больше нуля.")
    return add_named_item(data["fertilizers"], name, stock_ml=stock_ml)


def check_dosage(dosage: float, available_ml: float) -> None:
    """Проверяет количество и достаточность запаса, а не агронорму."""
    if not isfinite(dosage) or dosage <= 0:
        raise ValueError("Дозировка должна быть больше нуля.")
    if dosage > available_ml:
        raise ValueError(
            f"Недостаточно удобрения: осталось {available_ml:g} мл.")


def create_application(data: dict, plant_id: int, fertilizer_id: int,
                       dosage: float, application_date: str) -> dict:
    """Проверяет данные, добавляет запись и уменьшает остаток."""
    get_item(data["plants"], plant_id)
    fertilizer = get_item(data["fertilizers"], fertilizer_id)
    valid_date = parse_date(application_date)
    check_dosage(dosage, fertilizer["stock_ml"])
    record = {"id": data["next_application_id"], "plant_id": plant_id,
              "fertilizer_id": fertilizer_id, "dosage_ml": dosage,
              "date": valid_date}
    fertilizer["stock_ml"] -= dosage
    data["applications"].append(record)
    data["next_application_id"] += 1
    return record


def cancel_application(data: dict, application_id: int) -> None:
    """Отменяет ошибочную запись и возвращает учтённый расход в запас."""
    for index, record in enumerate(data["applications"]):
        if record["id"] == application_id:
            fertilizer = get_item(data["fertilizers"], record["fertilizer_id"])
            restored = fertilizer["stock_ml"] + record["dosage_ml"]
            if not isfinite(restored):
                raise ValueError("Слишком большое значение запаса.")
            fertilizer["stock_ml"] = restored
            del data["applications"][index]
            return
    raise ValueError("Применение с таким номером не найдено.")


def find_applications(data: dict, query: str):
    """Генератор: ищет записи по части названия растения или удобрения."""
    query = clean_name(query).casefold()
    for record in data["applications"]:
        plant = get_item(data["plants"], record["plant_id"])["name"]
        fertilizer = get_item(data["fertilizers"], record["fertilizer_id"])
        if query in plant.casefold() or query in fertilizer["name"].casefold():
            yield record


def sort_applications(records: list[dict], field: str) -> list[dict]:
    """Возвращает новый список, отсортированный по дате или дозировке."""
    if field not in ("date", "dosage_ml"):
        raise ValueError("Сортировать можно по дате или дозировке.")
    return sorted(records, key=lambda record: record[field])


def get_statistics(data: dict) -> dict:
    """Считает записи и расход отдельно для каждого удобрения."""
    usage = {}
    for record in data["applications"]:
        key = str(record["fertilizer_id"])
        usage[key] = usage.get(key, 0) + record["dosage_ml"]
    used_plants = {record["plant_id"] for record in data["applications"]}
    return {"applications": len(data["applications"]),
            "plants_used": len(used_plants), "usage_ml": usage}
