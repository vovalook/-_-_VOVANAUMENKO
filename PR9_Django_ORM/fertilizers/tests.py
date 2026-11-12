from django.test import Client, TestCase

from .models import Fertilizer, FertilizerFlower, Flower
from . import orm_queries as q


class ORMProjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rose = Flower.objects.create(name='Роза', color='Красный')
        cls.lily = Flower.objects.create(name='Лилия', color='Белый')
        cls.food = Fertilizer.objects.create(
            name='Флора Рост', type='Комплексное', season='Весна–лето',
            dosage='10 мл на 1 л воды', effect='рост', price=280,
        )
        cls.other = Fertilizer.objects.create(
            name='Лист Сила', type='Азотное', season='Весна',
            dosage='5 мл на 1 л воды', effect='листья', price=190,
        )
        FertilizerFlower.objects.create(fertilizer=cls.food, flower=cls.rose)
        FertilizerFlower.objects.create(fertilizer=cls.other, flower=cls.lily)

    def test_basic_reads_and_filters(self):
        self.assertEqual(q.all_fertilizers().count(), 2)
        self.assertEqual(q.fertilizer_by_id(self.food.pk), self.food)
        self.assertEqual(q.fertilizers_by_type('Азотное').count(), 1)
        self.assertEqual(q.affordable_type('Комплексное', 300).count(), 1)
        self.assertEqual(q.fertilizers_by_flower_color('Белый').count(), 1)
        self.assertEqual(q.fertilizers_excluding_type('Азотное').count(), 1)

    def test_search_and_sorts(self):
        self.assertEqual(q.search_fertilizer_name('Рост').count(), 1)
        self.assertEqual(q.search_catalog('роза').count(), 1)
        self.assertEqual(q.fertilizers_by_name().count(), 2)
        self.assertEqual(q.fertilizers_by_type_and_price().count(), 2)

    def test_relations_and_aggregation(self):
        self.assertEqual(q.compatibility_pairs().count(), 2)
        self.assertEqual(q.flowers_with_fertilizers().count(), 2)
        self.assertEqual(q.catalog_summary()['quantity'], 2)
        self.assertEqual(q.fertilizers_with_flower_count().count(), 2)
        self.assertEqual(q.catalog_page(1, 1).paginator.num_pages, 2)
        self.assertEqual(q.flowers_with_fertilizer_count().count(), 2)
        self.assertEqual(q.fertilizer_types_summary().count(), 2)

    def test_existing_pages_and_invalid_parameters(self):
        client = Client()
        self.assertEqual(client.get('/').status_code, 200)
        self.assertContains(client.get('/?q=роза'), 'Флора Рост')
        self.assertContains(client.get('/?type=Азотное'), 'Лист Сила')
        self.assertEqual(client.get(f'/fertilizer/{self.food.pk}/').status_code, 200)
        self.assertEqual(client.get('/fertilizer/9999/').status_code, 404)
        self.assertEqual(client.get('/?page=abc&sort=does_not_exist').status_code, 200)

    def test_create_update_delete(self):
        obj = Fertilizer.objects.create(
            name='Учебное', type='Минеральное', season='Лето',
            dosage='по инструкции', effect='учебная запись', price=100,
        )
        obj.price = 120
        obj.save()
        self.assertEqual(Fertilizer.objects.get(pk=obj.pk).price, 120)
        obj.delete()
        self.assertFalse(Fertilizer.objects.filter(name='Учебное').exists())
