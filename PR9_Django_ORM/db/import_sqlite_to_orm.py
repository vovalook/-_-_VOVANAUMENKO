"""Безопасный перенос базы ПР7 в Django ORM после выполнения migrate."""
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fertilizer_project.settings')

import django
django.setup()

from django.db import transaction  # noqa: E402
from fertilizers.models import Fertilizer, FertilizerFlower, Flower  # noqa: E402

SOURCE = ROOT / 'fertilizers.sqlite3'
if not SOURCE.exists():
    raise SystemExit(f'Нет исходной базы ПР7: {SOURCE}')

with sqlite3.connect(SOURCE) as conn:
    conn.row_factory = sqlite3.Row
    flowers = [dict(row) for row in conn.execute('SELECT id, name, color FROM flowers')]
    fertilizers = [dict(row) for row in conn.execute(
        'SELECT id, name, type, season, dosage, effect, price FROM fertilizers'
    )]
    links = [tuple(row) for row in conn.execute(
        'SELECT fertilizer_id, flower_id FROM fertilizer_flowers'
    )]

with transaction.atomic():
    for row in flowers:
        Flower.objects.update_or_create(
            pk=row['id'], defaults={'name': row['name'], 'color': row['color']}
        )
    for row in fertilizers:
        Fertilizer.objects.update_or_create(
            pk=row['id'], defaults={key: value for key, value in row.items() if key != 'id'}
        )
    for fertilizer_id, flower_id in links:
        FertilizerFlower.objects.get_or_create(
            fertilizer_id=fertilizer_id, flower_id=flower_id
        )

print(f'Исходная БД ПР7: {len(flowers)} цветов, {len(fertilizers)} удобрений, {len(links)} связей')
print('Рабочая ORM БД: '
      f'{Flower.objects.count()} цветов, '
      f'{Fertilizer.objects.count()} удобрений, '
      f'{FertilizerFlower.objects.count()} связей')
