# Generated by Django 3.2 on 2021-05-24 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='favorites',
        ),
    ]
