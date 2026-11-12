# Generated for PR9, based on the existing PR7 SQLite tables.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Flower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
            ],
            options={'ordering': ['name'], 'verbose_name': 'Цветок', 'verbose_name_plural': 'Цветы'},
        ),
        migrations.CreateModel(
            name='Fertilizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Название')),
                ('type', models.CharField(max_length=70, verbose_name='Тип')),
                ('season', models.CharField(max_length=100, verbose_name='Сезон')),
                ('dosage', models.CharField(max_length=130, verbose_name='Дозировка')),
                ('effect', models.TextField(verbose_name='Эффект')),
                ('price', models.PositiveIntegerField(verbose_name='Цена, руб.')),
            ],
            options={'ordering': ['name'], 'verbose_name': 'Удобрение', 'verbose_name_plural': 'Удобрения'},
        ),
        migrations.CreateModel(
            name='FertilizerFlower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fertilizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compatibilities', to='fertilizers.fertilizer')),
                ('flower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fertilizer_links', to='fertilizers.flower')),
            ],
            options={'verbose_name': 'Совместимость удобрения и цветка', 'verbose_name_plural': 'Совместимости'},
        ),
        migrations.AddField(
            model_name='fertilizer',
            name='flowers',
            field=models.ManyToManyField(related_name='fertilizers', through='fertilizers.FertilizerFlower', to='fertilizers.flower', verbose_name='Подходящие цветы'),
        ),
        migrations.AddConstraint(
            model_name='fertilizerflower',
            constraint=models.UniqueConstraint(fields=('fertilizer', 'flower'), name='unique_fertilizer_flower'),
        ),
    ]
