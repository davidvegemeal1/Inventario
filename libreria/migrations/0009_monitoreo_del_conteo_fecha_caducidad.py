# Generated by Django 4.2.6 on 2023-11-14 02:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0008_rename_contraseña_login_escritorio_contrasenia'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoreo_del_conteo',
            name='fecha_caducidad',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
