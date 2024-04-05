# Generated by Django 5.0.2 on 2024-03-17 04:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_esp_doctor_alter_citas_especialidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='esp',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='citas',
            name='Doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.doctor'),
        ),
        migrations.AlterField(
            model_name='citas',
            name='Especialidad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.esp'),
        ),
    ]