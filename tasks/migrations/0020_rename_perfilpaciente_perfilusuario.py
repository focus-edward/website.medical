# Generated by Django 5.0.2 on 2024-03-19 01:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0019_perfilpaciente_apellidos_perfilpaciente_direccion_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PerfilPaciente',
            new_name='PerfilUsuario',
        ),
    ]
