# Generated by Django 2.2.4 on 2019-08-06 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tpot_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='variable',
        ),
    ]
