# Generated by Django 4.1.2 on 2022-10-16 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_delete_tag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
