# Generated by Django 3.1 on 2020-09-18 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_order'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='OrderPlaced',
        ),
    ]
