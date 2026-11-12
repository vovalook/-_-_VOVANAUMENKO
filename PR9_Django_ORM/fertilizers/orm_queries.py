"""Различные прикладные ORM-выражения ПР9, сгруппированные по требованиям.

Каждая функция решает отдельную задачу каталога. Примеры вызываются
в db/check_orm_examples.py и проверяются тестами.
"""
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q

from .models import Fertilizer, FertilizerFlower, Flower


# Базовое чтение — 2 выражения.
def all_fertilizers():                    # 01: полный каталог
    return Fertilizer.objects.all()


def fertilizer_by_id(pk):                 # 02: конкретная карточка
    return Fertilizer.objects.get(pk=pk)


# Фильтрация — 4 выражения.
def fertilizers_by_type(type_name):       # 03: один параметр
    return Fertilizer.objects.filter(type=type_name)


def affordable_type(type_name, max_price):  # 04: два условия
    return Fertilizer.objects.filter(type=type_name, price__lte=max_price)


def fertilizers_by_flower_color(color):   # 05: поле связанной модели
    return Fertilizer.objects.filter(flowers__color=color).distinct()


def fertilizers_excluding_type(type_name):  # 06: исключение
    return Fertilizer.objects.exclude(type=type_name)


# Поиск — 2 выражения.
def search_fertilizer_name(text):         # 07: строковое поле
    return Fertilizer.objects.filter(name__icontains=text)


def search_catalog(text):                 # 08: название, тип или цветок
    text = text.strip()
    if not text:
        return all_fertilizers()
    variants = {text, text.capitalize(), text.title()}
    condition = Q()
    for value in variants:
        condition |= (
            Q(name__icontains=value)
            | Q(type__icontains=value)
            | Q(flowers__name__icontains=value)
        )
    return Fertilizer.objects.filter(condition).distinct()


# Сортировка — 2 выражения.
def fertilizers_by_name():              # 09: одно поле
    return Fertilizer.objects.order_by('name')


def fertilizers_by_type_and_price():    # 10: несколько полей
    return Fertilizer.objects.order_by('type', 'price')


# Работа со связями — 2 выражения.
def compatibility_pairs():              # 11: select_related для FK
    return FertilizerFlower.objects.select_related('fertilizer', 'flower')


def flowers_with_fertilizers():         # 12: prefetch_related для M2M
    return Flower.objects.prefetch_related('fertilizers')


# Агрегаты и аннотации.
def catalog_summary():                  # 13: общий показатель
    return Fertilizer.objects.aggregate(
        quantity=Count('id'), average_price=Avg('price'),
        minimum_price=Min('price'), maximum_price=Max('price'),
    )


def fertilizers_with_flower_count():    # 14: число цветов у каждой подкормки
    return Fertilizer.objects.annotate(flowers_count=Count('flowers', distinct=True))


def catalog_page(page=1, page_size=3):  # 15: Paginator
    return Paginator(Fertilizer.objects.order_by('name'), page_size).get_page(page)


def flowers_with_fertilizer_count():    # 16: число подкормок у каждого цветка
    return Flower.objects.annotate(fertilizers_count=Count('fertilizers', distinct=True))


def fertilizer_types_summary():         # 17: группы по типу и средняя цена
    return Fertilizer.objects.values('type').annotate(
        quantity=Count('id'), average_price=Avg('price'),
    ).order_by('type')
