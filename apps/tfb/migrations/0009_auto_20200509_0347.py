# Generated by Django 2.2.6 on 2020-05-09 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfb', '0008_estadistica_jugador_partido_inicial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadistica_jugador_partido',
            name='usg',
            field=models.FloatField(null=True, verbose_name='USG%'),
        ),
    ]