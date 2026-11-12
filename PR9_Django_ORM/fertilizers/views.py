from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render

from .models import Fertilizer
from .orm_queries import all_fertilizers, fertilizer_by_id, search_catalog, catalog_summary


SORT_FIELDS = {
    'name': 'name',
    'price': 'price',
    'price_desc': '-price',
    'type': 'type',
}


def index(request):
    query = request.GET.get('q', '').strip()
    selected_type = request.GET.get('type', '').strip()
    selected_sort = request.GET.get('sort', 'name')
    if selected_sort not in SORT_FIELDS:
        selected_sort = 'name'

    types = list(Fertilizer.objects.order_by('type').values_list('type', flat=True).distinct())
    if selected_type not in types:
        selected_type = ''

    items = search_catalog(query) if query else all_fertilizers()
    if selected_type:
        items = items.filter(type=selected_type)
    items = items.prefetch_related('flowers').annotate(
        flowers_count=Count('flowers', distinct=True)
    ).order_by(SORT_FIELDS[selected_sort], 'pk')
    page_obj = Paginator(items, 3).get_page(request.GET.get('page'))
    for item in page_obj:
        item.flowers_text = ' • '.join(f.name for f in item.flowers.all())

    summary = catalog_summary()
    return render(request, 'fertilizers/index.html', {
        'items': page_obj,
        'page_obj': page_obj,
        'query': query,
        'types': types,
        'selected_type': selected_type,
        'selected_sort': selected_sort,
        'summary': summary,
    })


def detail(request, fertilizer_id):
    try:
        item = fertilizer_by_id(fertilizer_id)
    except Fertilizer.DoesNotExist as exc:
        raise Http404('Удобрение не найдено') from exc
    item.flowers_text = ' • '.join(
        f.name for f in item.flowers.all().order_by('name')
    )
    return render(request, 'fertilizers/detail.html', {'item': item})
