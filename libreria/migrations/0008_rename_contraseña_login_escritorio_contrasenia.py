# Generated by Django 4.2.6 on 2023-11-10 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0007_login_escritorio_apellidos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login_escritorio',
            old_name='contraseña',
            new_name='contrasenia',
        ),
    ]
