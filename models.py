"""Классы предметной области для сервиса учёта удобрений."""

from math import isfinite

from utils import clean_name, parse_date


class NamedEntity:
    """Базовый класс для объектов с номером и названием."""

    def __init__(self, item_id: int, name: str) -> None:
        if item_id <= 0:
            raise ValueError("Номер объекта должен быть положительным.")
        self.item_id = item_id
        self.name = clean_name(name)

    def __str__(self) -> str:
        return f"{self.item_id}: {self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.to_data() == other.to_data()

    def to_data(self) -> dict:
        """Преобразует объект в словарь для JSON."""
        return {"name": self.name}


class Plant(NamedEntity):
    """Растение, для которого учитывается применение удобрений."""

    @classmethod
    def from_data(cls, item_id: int, data: dict) -> "Plant":
        """Создаёт растение из словаря JSON."""
        return cls(item_id, data["name"])


class Fertilizer(NamedEntity):
    """Жидкое удобрение с учётом остатка в миллилитрах."""

    def __init__(self, item_id: int, name: str, stock_ml: float) -> None:
        super().__init__(item_id, name)
        self.stock_ml = self._check_stock(stock_ml)

    def __str__(self) -> str:
        return f"{self.item_id}: {self.name}; остаток {self.stock_ml:g} мл"

    @staticmethod
    def _check_stock(value: float) -> float:
        """Проверяет, что запас удобрения неотрицательный."""
        if not isfinite(value) or value < 0:
            raise ValueError("Запас удобрения должен быть неотрицательным.")
        return float(value)

    @classmethod
    def from_data(cls, item_id: int, data: dict) -> "Fertilizer":
        """Создаёт удобрение из словаря JSON."""
        return cls(item_id, data["name"], data["stock_ml"])

    def can_spend(self, dosage_ml: float) -> bool:
        """Показывает, достаточно ли удобрения для указанной дозировки."""
        return isfinite(dosage_ml) and 0 < dosage_ml <= self.stock_ml

    def spend(self, dosage_ml: float) -> None:
        """Уменьшает остаток после применения удобрения."""
        if not self.can_spend(dosage_ml):
            raise ValueError(
                f"Недостаточно удобрения: осталось {self.stock_ml:g} мл.")
        self.stock_ml -= dosage_ml

    def restore(self, dosage_ml: float) -> None:
        """Возвращает удобрение в запас при отмене ошибочной записи."""
        if not isfinite(dosage_ml) or dosage_ml <= 0:
            raise ValueError("Дозировка должна быть больше нуля.")
        self.stock_ml = self._check_stock(self.stock_ml + dosage_ml)

    def to_data(self) -> dict:
        """Преобразует удобрение в словарь для JSON."""
        data = super().to_data()
        data["stock_ml"] = self.stock_ml
        return data


class Application:
    """Запись о применении удобрения для растения."""

    def __init__(self, record_id: int, plant_id: int, fertilizer_id: int,
                 dosage_ml: float, application_date: str) -> None:
        if record_id <= 0 or plant_id <= 0 or fertilizer_id <= 0:
            raise ValueError("Номера записи, растения и удобрения должны быть "
                             "положительными.")
        if not isfinite(dosage_ml) or dosage_ml <= 0:
            raise ValueError("Дозировка должна быть больше нуля.")
        self.record_id = record_id
        self.plant_id = plant_id
        self.fertilizer_id = fertilizer_id
        self.dosage_ml = float(dosage_ml)
        self.date = parse_date(application_date)

    def __str__(self) -> str:
        return (f"№ {self.record_id} | {self.date} | растение "
                f"{self.plant_id} | удобрение {self.fertilizer_id} | "
                f"{self.dosage_ml:g} мл")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Application):
            return False
        return self.to_data() == other.to_data()

    @classmethod
    def from_data(cls, data: dict) -> "Application":
        """Создаёт запись из словаря JSON."""
        return cls(data["id"], data["plant_id"], data["fertilizer_id"],
                   data["dosage_ml"], data["date"])

    def to_data(self) -> dict:
        """Преобразует запись в словарь для JSON."""
        return {"id": self.record_id, "plant_id": self.plant_id,
                "fertilizer_id": self.fertilizer_id,
                "dosage_ml": self.dosage_ml, "date": self.date}
