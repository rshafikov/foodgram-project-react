# Generated by Django 2.2.16 on 2022-10-16 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follow',
            new_name='following',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='user',
        ),
    ]
