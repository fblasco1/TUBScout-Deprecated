# Generated by Django 2.2.6 on 2020-05-01 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadistica_equipo_partido',
            name='oportunidad_tiro_libre',
        ),
        migrations.RemoveField(
            model_name='estadistica_jugador_partido',
            name='oportunidad_tiro_libre',
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='p2_rate',
            field=models.FloatField(default=0, verbose_name='2Prate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='p3_rate',
            field=models.FloatField(default=0, verbose_name='3Prate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='q1',
            field=models.FloatField(default=0, verbose_name='Q1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='q2',
            field=models.FloatField(default=0, verbose_name='Q2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='q3',
            field=models.FloatField(default=0, verbose_name='Q3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='q4',
            field=models.FloatField(default=0, verbose_name='Q4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='tcas',
            field=models.FloatField(default=0, verbose_name='TCAS'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_equipo_partido',
            name='tl_rate',
            field=models.FloatField(default=0, verbose_name='TLrate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_jugador_partido',
            name='p2_rate',
            field=models.FloatField(default=0, verbose_name='2Prate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_jugador_partido',
            name='p3_rate',
            field=models.FloatField(default=0, verbose_name='3Prate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_jugador_partido',
            name='tl_rate',
            field=models.FloatField(default=0, verbose_name='TLrate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica_jugador_partido',
            name='usg',
            field=models.FloatField(default=0, verbose_name='USG%'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estadistica_equipo_partido',
            name='localia',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='estadistica_equipo_partido',
            name='rebote_total',
            field=models.FloatField(verbose_name='RT'),
        ),
        migrations.AlterField(
            model_name='estadistica_equipo_partido',
            name='tiros_2_porcentaje',
            field=models.FloatField(verbose_name='%2P'),
        ),
        migrations.AlterField(
            model_name='estadistica_equipo_partido',
            name='tiros_3_porcentaje',
            field=models.FloatField(verbose_name='%3P'),
        ),
        migrations.AlterField(
            model_name='estadistica_equipo_partido',
            name='tiros_campo_porcentaje',
            field=models.FloatField(verbose_name='%TC'),
        ),
        migrations.AlterField(
            model_name='estadistica_equipo_partido',
            name='tiros_libre_porcentaje',
            field=models.FloatField(verbose_name='%TL'),
        ),
    ]