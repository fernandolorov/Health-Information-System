# Generated by Django 3.0.4 on 2020-03-23 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CardioApp', '0016_snomed_diagnosis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosis',
            name='diagnosis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CardioApp.SNOMED_Diagnosis'),
        ),
    ]
