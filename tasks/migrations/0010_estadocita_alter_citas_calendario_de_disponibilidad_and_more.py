# Generated by Django 5.0.2 on 2024-03-17 07:24

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_citas_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoCita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Estado', models.TextField(default='Pendiente')),
            ],
        ),
        migrations.AlterField(
            model_name='citas',
            name='Calendario_de_disponibilidad',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='citas',
            name='Cédula_del_paciente',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.validate_integer]),
        ),
        migrations.AlterField(
            model_name='citas',
            name='Información_relevante',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='citas',
            name='Teléfono_de_contacto',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.validate_integer]),
        ),
        migrations.AlterField(
            model_name='citas',
            name='Estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.estadocita'),
        ),
    ]
