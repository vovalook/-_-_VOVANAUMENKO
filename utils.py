"""Проверка данных и ввод значений в консоли."""

from datetime import date
from math import isfinite


def clean_name(value: str) -> str:
    """Убирает лишние пробелы и запрещает пустое название."""
    name = value.strip()
    if not name:
        raise ValueError("Название не может быть пустым.")
    return name


def positive_number(value: str) -> float:
    """Принимает положительное число с точкой или запятой."""
    number = float(value.strip().replace(",", "."))
    if not isfinite(number) or number <= 0:
        raise ValueError("Введите конечное число больше нуля.")
    return number


def parse_date(value: str) -> str:
    """Проверяет дату и возвращает её в формате ГГГГ-ММ-ДД."""
    return date.fromisoformat(value.strip()).isoformat()


def read_text(prompt: str) -> str:
    """Повторяет запрос, если введена пустая строка."""
    while True:
        try:
            return clean_name(input(prompt))
        except ValueError as error:
            print(error)


def get_plant_name() -> str:
    """Функция из ПР1: ввод названия растения."""
    return read_text("Название растения: ")


def get_fertilizer_name() -> str:
    """Функция из ПР1: ввод названия удобрения."""
    return read_text("Название удобрения: ")


def read_number(prompt: str) -> float:
    """Повторяет запрос при ошибочном вводе числа."""
    while True:
        try:
            return positive_number(input(prompt))
        except ValueError:
            print("Нужно число больше нуля, например 20 или 2,5.")


def read_id(prompt: str) -> int:
    """Читает положительный целый номер записи."""
    while True:
        text = input(prompt).strip()
        if text.isascii() and text.isdecimal() and int(text) > 0:
            return int(text)
        print("Введите целый номер из списка, например 1.")


def read_date() -> str:
    """При пустом вводе использует сегодняшнюю дату."""
    while True:
        text = input("Дата ГГГГ-ММ-ДД (Enter — сегодня): ").strip()
        try:
            return parse_date(text) if text else date.today().isoformat()
        except ValueError:
            print("Такой даты нет. Пример правильной записи: 2026-09-23.")
