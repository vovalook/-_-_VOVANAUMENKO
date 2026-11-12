"""Только просмотр исходной SQLite-базы из ПР7 (не используется views.py)."""
import sqlite3
from pathlib import Path

source = Path(__file__).resolve().parent.parent / 'fertilizers.sqlite3'
if not source.exists():
    raise SystemExit(f'Нет исходной базы: {source}')
with sqlite3.connect(source) as connection:
    for table in ('flowers', 'fertilizers', 'fertilizer_flowers'):
        number = connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f'{table}: {number}')
