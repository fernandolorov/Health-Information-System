# Generated by Django 3.0.4 on 2020-03-19 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CardioApp', '0011_auto_20200319_0314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='videofile',
            new_name='imagefile',
        ),
    ]