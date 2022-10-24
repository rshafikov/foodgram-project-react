# Generated by Django 2.2.16 on 2022-10-24 20:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20221017_2119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'Ингредиент'},
        ),
        migrations.RenameField(
            model_name='ingredientamount',
            old_name='quantity',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Значение не может быть меньше 1')], verbose_name='Время готовки в минутах'),
        ),
    ]