# Generated by Django 2.2.6 on 2020-05-02 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tfb', '0002_auto_20200501_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estadistica_equipo_partido',
            old_name='tcas',
            new_name='tiros_campo_asistidos',
        ),
        migrations.AddField(
            model_name='jugadores',
            name='apellido',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]