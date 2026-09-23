"""Чтение и запись JSON с проверкой структуры данных."""

import json
from math import isfinite
from pathlib import Path

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
    """Проверяет коллекции, ссылки и уникальность номеров в JSON."""
    try:
        if not isinstance(data, dict):
            raise ValueError("Корень JSON должен быть словарём.")
        for section in ("plants", "fertilizers"):
            if not isinstance(data[section], dict):
                raise ValueError("Справочник должен быть словарём.")
            names = set()
            for key, item in data[section].items():
                if int(key) <= 0 or str(int(key)) != key:
                    raise ValueError("Некорректный номер справочника.")
                name = clean_name(item["name"]).casefold()
                if name in names:
                    raise ValueError("Повторяющееся название в JSON.")
                names.add(name)
                if section == "fertilizers":
                    validate_number(item["stock_ml"])
        if not isinstance(data["applications"], list):
            raise ValueError("Журнал должен быть списком.")
        ids = set()
        for record in data["applications"]:
            number = record["id"]
            if type(number) is not int or number <= 0 or number in ids:
                raise ValueError("Неверный или повторяющийся номер записи.")
            ids.add(number)
            for field, section in (("plant_id", "plants"),
                                   ("fertilizer_id", "fertilizers")):
                if type(record[field]) is not int:
                    raise ValueError("Ссылка должна быть целым номером.")
                if str(record[field]) not in data[section]:
                    raise ValueError("В журнале есть неизвестная ссылка.")
            validate_number(record["dosage_ml"], positive=True)
            parse_date(record["date"])
        next_id = data["next_application_id"]
        if type(next_id) is not int or next_id <= max(ids, default=0):
            raise ValueError("Неверный счётчик номеров применений.")
    except (KeyError, TypeError, AttributeError, OverflowError) as error:
        message = "В JSON отсутствуют поля или нарушены типы."
        raise ValueError(message) from error


def load_data(path: Path = DATA_FILE) -> dict:
    """При отсутствии файла возвращает пустой набор данных."""
    if not path.exists():
        return empty_data()
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    validate_data(data)
    return data


def save_data(data: dict, path: Path = DATA_FILE) -> None:
    """Сначала пишет временный файл, затем заменяет основной."""
    validate_data(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False,
                      indent=2, allow_nan=False)
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()
