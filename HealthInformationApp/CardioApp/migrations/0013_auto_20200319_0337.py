# Generated by Django 3.0.4 on 2020-03-19 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CardioApp', '0012_auto_20200319_0331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='imagefile',
            new_name='videofile',
        ),
    ]