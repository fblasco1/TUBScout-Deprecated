# Generated by Django 2.2.6 on 2020-05-03 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfb', '0005_auto_20200503_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partidos',
            name='detalle_partido',
            field=models.DateField(null=True, verbose_name='Fecha de Partido'),
        ),
    ]