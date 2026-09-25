

def load_data(path: Path = DATA_FILE) -> dict:
    """При отсутствии файла возвращает пустой набор объектов."""
    if not path.exists():
        return empty_data()
    with path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)
    try:
        data = data_from_json(raw_data)
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        message = "В JSON отсутствуют поля или нарушены типы."
        raise ValueError(message) from error
    validate_data(data)
    return data


def save_data(data: dict, path: Path = DATA_FILE) -> None:
    """Сначала пишет временный файл, затем заменяет основной."""
    validate_data(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data_to_json(data), file, ensure_ascii=False,
                      indent=2, allow_nan=False)
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def data_from_json(raw_data: dict) -> dict:
    """Преобразует словари из JSON в объекты классов."""
    data = empty_data()
    for key, item in raw_data["plants"].items():
        data["plants"][int(key)] = Plant.from_data(int(key), item)
    for key, item in raw_data["fertilizers"].items():
        data["fertilizers"][int(key)] = Fertilizer.from_data(int(key), item)
    data["applications"] = [
        Application.from_data(item) for item in raw_data["applications"]]
    data["next_application_id"] = raw_data["next_application_id"]
    return data


def data_to_json(data: dict) -> dict:
    """Преобразует объекты классов в обычные данные для JSON."""
    return {
        "plants": {str(key): plant.to_data()
                   for key, plant in data["plants"].items()},
        "fertilizers": {str(key): fertilizer.to_data()
                        for key, fertilizer in data["fertilizers"].items()},
        "applications": [record.to_data()
                         for record in data["applications"]],
        "next_application_id": data["next_application_id"],
    }
