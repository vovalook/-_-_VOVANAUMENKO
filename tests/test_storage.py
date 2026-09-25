"""Проверки JSON и сохранности исходного файла при ошибке."""

import json

import pytest

from services import add_plant, empty_data
from storage import data_to_json, load_data, save_data


def test_json_round_trip(tmp_path):
    path = tmp_path / "data" / "database.json"
    data = empty_data()
    add_plant(data, "Роза")
    save_data(data, path)
    assert data_to_json(load_data(path)) == data_to_json(data)
    assert "Роза" in path.read_text(encoding="utf-8")


def test_missing_file_returns_empty_collections(tmp_path):
    assert load_data(tmp_path / "missing.json") == empty_data()


def test_corrupted_json_remains_unchanged(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{неверный json", encoding="utf-8")
    original = path.read_bytes()
    with pytest.raises(ValueError):
        load_data(path)
    assert path.read_bytes() == original


def test_wrong_structure_is_rejected(tmp_path):
    path = tmp_path / "wrong.json"
    path.write_text(json.dumps({"plants": []}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_data(path)


def test_write_error_does_not_replace_existing_file(tmp_path, monkeypatch):
    path = tmp_path / "database.json"
    data = empty_data()
    save_data(data, path)
    original = path.read_bytes()
    add_plant(data, "Фикус")

    def failed_dump(*args, **kwargs):
        raise OSError("Нет места на диске")

    monkeypatch.setattr(json, "dump", failed_dump)
    with pytest.raises(OSError):
        save_data(data, path)
    assert path.read_bytes() == original
