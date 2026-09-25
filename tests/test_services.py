"""Проверки правил учёта, поиска и статистики."""

from copy import deepcopy

import pytest

from services import (
    add_fertilizer, add_plant, cancel_application, create_application,
    empty_data, find_applications, get_statistics, sort_applications,
)
from utils import positive_number


def sample_data() -> dict:
    """Независимые данные для каждого теста."""
    data = empty_data()
    add_plant(data, "Роза")
    add_fertilizer(data, "Универсальное", 100)
    return data


def test_application_reduces_stock():
    data = sample_data()
    record = create_application(data, 1, 1, 20, "2026-09-23")
    assert record.record_id == 1
    assert data["fertilizers"][1].stock_ml == 80
    assert data["applications"] == [record]


def test_insufficient_stock_does_not_change_data():
    data = sample_data()
    original = deepcopy(data)
    with pytest.raises(ValueError, match="Недостаточно"):
        create_application(data, 1, 1, 101, "2026-09-23")
    assert data == original


def test_cancel_restores_stock_and_keeps_unique_ids():
    data = sample_data()
    create_application(data, 1, 1, 20, "2026-09-23")
    cancel_application(data, 1)
    assert data["applications"] == []
    assert data["fertilizers"][1].stock_ml == 100
    with pytest.raises(ValueError):
        cancel_application(data, 1)
    assert data["fertilizers"][1].stock_ml == 100
    record = create_application(data, 1, 1, 5, "2026-09-24")
    assert record.record_id == 2


def test_search_sort_and_statistics():
    data = sample_data()
    add_plant(data, "Фикус")
    create_application(data, 1, 1, 20, "2026-09-24")
    create_application(data, 2, 1, 10, "2026-09-23")
    assert [r.record_id for r in find_applications(data, "РОЗ")] == [1]
    assert len(list(find_applications(data, "универс"))) == 2
    records = sort_applications(data["applications"], "dosage_ml")
    assert [r.dosage_ml for r in records] == [10, 20]
    assert data["applications"][0].record_id == 1
    assert get_statistics(data) == {
        "applications": 2, "plants_used": 2, "usage_ml": {1: 30}}


@pytest.mark.parametrize("dose", [0, -1, float("nan"), float("inf")])
def test_invalid_dose_is_rejected(dose):
    data = sample_data()
    with pytest.raises(ValueError):
        create_application(data, 1, 1, dose, "2026-09-23")
    assert data["fertilizers"][1].stock_ml == 100
    assert data["applications"] == []


def test_unknown_id_and_invalid_date_do_not_change_stock():
    data = sample_data()
    for plant_id, date_value in [(99, "2026-09-23"), (1, "2026-02-30")]:
        with pytest.raises(ValueError):
            create_application(data, plant_id, 1, 20, date_value)
    assert data["fertilizers"][1].stock_ml == 100


def test_names_are_checked_and_comma_is_accepted():
    data = sample_data()
    with pytest.raises(ValueError):
        add_plant(data, " роза ")
    with pytest.raises(ValueError):
        add_plant(data, "   ")
    assert positive_number("2,5") == 2.5
    for value in ["abc", "-0", "0", "NaN", "inf"]:
        with pytest.raises(ValueError):
            positive_number(value)


def test_objects_have_string_representation_and_methods():
    data = sample_data()
    plant = data["plants"][1]
    fertilizer = data["fertilizers"][1]
    assert "Роза" in str(plant)
    assert "остаток" in str(fertilizer)
    assert fertilizer.can_spend(50)
    assert not fertilizer.can_spend(150)
