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
