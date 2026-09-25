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
