# Generated by Django 3.0.3 on 2020-03-10 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CardioApp', '0007_diagnosis_investigation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='experienced_before',
            field=models.BooleanField(blank=True),
        ),
    ]
