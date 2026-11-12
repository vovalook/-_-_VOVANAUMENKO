"""Практическая проверка 17 самостоятельных ORM-выражений."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fertilizer_project.settings')

import django
django.setup()

from fertilizers import orm_queries as q  # noqa: E402

examples = [
    ('01 all', lambda: list(q.all_fertilizers())),
    ('02 get', lambda: q.fertilizer_by_id(1)),
    ('03 filter by type', lambda: list(q.fertilizers_by_type('Комплексное'))),
    ('04 filter multiple', lambda: list(q.affordable_type('Комплексное', 300))),
    ('05 filter related', lambda: list(q.fertilizers_by_flower_color('Белый'))),
    ('06 exclude', lambda: list(q.fertilizers_excluding_type('Азотное'))),
    ('07 name search', lambda: list(q.search_fertilizer_name('Рост'))),
    ('08 multi field search', lambda: list(q.search_catalog('роза'))),
    ('09 sort one field', lambda: list(q.fertilizers_by_name())),
    ('10 sort two fields', lambda: list(q.fertilizers_by_type_and_price())),
    ('11 select_related', lambda: list(q.compatibility_pairs())),
    ('12 prefetch_related', lambda: list(q.flowers_with_fertilizers())),
    ('13 aggregate', q.catalog_summary),
    ('14 annotate', lambda: list(q.fertilizers_with_flower_count())),
    ('15 paginator', lambda: list(q.catalog_page(1))),
    ('16 flower aggregate', lambda: list(q.flowers_with_fertilizer_count())),
    ('17 group values', lambda: list(q.fertilizer_types_summary())),
]
for title, func in examples:
    result = func()
    print(f'{title}: {result}')
print('Проверено 17 самостоятельных ORM-выражений для каталога удобрений.')
