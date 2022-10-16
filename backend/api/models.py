from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name = 'Имя тега',
        max_length = 200,
    )
    color = models.CharField(
        verbose_name = 'Цвет',
        max_length = 7, 
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
    )


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name = 'Имя ингредиента',
        max_length = 200,
    )
    measurement_unit = models.CharField(
        verbose_name = 'Единица измерения',
        max_length = 200,
    )