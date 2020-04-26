# Generated by Django 2.2.6 on 2020-04-23 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre Completo')),
                ('tipo_licencia', models.CharField(choices=[('B', 'BASICO'), ('P', 'PRO'), ('F', 'FULL')], max_length=1)),
                ('rol_usuario', models.CharField(choices=[('E', 'ENTRENADOR'), ('J', 'JUGADOR'), ('A', 'AGENTE'), ('P', 'PERIODISTA')], max_length=1)),
                ('id_equipo', models.IntegerField(blank=True, null=True)),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación de licencia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('key', models.CharField(blank=True, max_length=120, null=True)),
                ('activado', models.BooleanField(default=False)),
                ('expiracion_forzada', models.BooleanField(default=False)),
                ('expiracion', models.IntegerField(default=14)),
                ('fecha_alta', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]