# Generated by Django 5.2.4 on 2025-07-23 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"), #if we rename to something intitial5 we have to update refernces as well
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="price",
            new_name="unit_price",
        ),
    ]
