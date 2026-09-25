"""Чтение и запись JSON с преобразованием объектов."""

import json
from math import isfinite
from pathlib import Path

from models import Application, Fertilizer, Plant
from services import empty_data
from utils import clean_name, parse_date

DATA_FILE = Path(__file__).resolve().parent / "data" / "database.json"


def validate_number(value, positive: bool = False) -> None:
    """Отклоняет отрицательные числа, bool, NaN и бесконечность."""
    if type(value) not in (int, float) or not isfinite(value):
        raise ValueError("В JSON должно быть конечное число.")
    if value < 0 or (positive and value == 0):
        raise ValueError("В JSON недопустимое количество.")


def validate_data(data: dict) -> None:
    """Проверяет коллекции объектов, ссылки и уникальность номеров."""
    try:
        if not isinstance(data, dict):
            raise ValueError("Корень данных должен быть словарём.")
        for section, expected_type in (("plants", Plant),
                                       ("fertilizers", Fertilizer)):
            if not isinstance(data[section], dict):
                raise ValueError("Справочник должен быть словарём объектов.")
            names = set()
            for key, item in data[section].items():
                if type(key) is not int or key <= 0:
                    raise ValueError("Некорректный номер справочника.")
                if not isinstance(item, expected_type):
                    raise ValueError("В справочнике объект неверного класса.")
                name = clean_name(item.name).casefold()
                if name in names:
                    raise ValueError("Повторяющееся название.")
                names.add(name)
                if section == "fertilizers":
                    validate_number(item.stock_ml)
        if not isinstance(data["applications"], list):
            raise ValueError("Журнал должен быть списком.")
        ids = set()
        for record in data["applications"]:
            if not isinstance(record, Application):
                raise ValueError("В журнале объект неверного класса.")
            number = record.record_id
            if type(number) is not int or number <= 0 or number in ids:
                raise ValueError("Неверный или повторяющийся номер записи.")
            ids.add(number)
            if record.plant_id not in data["plants"]:
                raise ValueError("В журнале есть неизвестное растение.")
            if record.fertilizer_id not in data["fertilizers"]:
                raise ValueError("В журнале есть неизвестное удобрение.")
            validate_number(record.dosage_ml, positive=True)
            parse_date(record.date)
        next_id = data["next_application_id"]
        if type(next_id) is not int or next_id <= max(ids, default=0):
            raise ValueError("Неверный счётчик номеров применений.")
    except (KeyError, TypeError, AttributeError, OverflowError) as error:
        message = "В JSON отсутствуют поля или нарушены типы."
        raise ValueError(message) from error


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
