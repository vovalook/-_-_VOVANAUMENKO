from django.db import models


class Flower(models.Model):
    """Цветок из справочника ПР5–ПР7."""
    name = models.CharField('Название', max_length=100, unique=True)
    color = models.CharField('Цвет', max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'

    def __str__(self):
        return self.name


class Fertilizer(models.Model):
    """Подкормка, информация о которой отображается в каталоге."""
    name = models.CharField('Название', max_length=120, unique=True)
    type = models.CharField('Тип', max_length=70)
    season = models.CharField('Сезон', max_length=100)
    dosage = models.CharField('Дозировка', max_length=130)
    effect = models.TextField('Эффект')
    price = models.PositiveIntegerField('Цена, руб.')
    flowers = models.ManyToManyField(
        Flower, through='FertilizerFlower', related_name='fertilizers',
        verbose_name='Подходящие цветы',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Удобрение'
        verbose_name_plural = 'Удобрения'

    def __str__(self):
        return self.name


class FertilizerFlower(models.Model):
    """Связь многих удобрений со многими подходящими цветами."""
    fertilizer = models.ForeignKey(
        Fertilizer, on_delete=models.CASCADE, related_name='compatibilities'
    )
    flower = models.ForeignKey(
        Flower, on_delete=models.CASCADE, related_name='fertilizer_links'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['fertilizer', 'flower'], name='unique_fertilizer_flower'
        )]
        verbose_name = 'Совместимость удобрения и цветка'
        verbose_name_plural = 'Совместимости'

    def __str__(self):
        return f'{self.fertilizer} — {self.flower}'
