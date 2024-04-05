# Generated by Django 5.0.2 on 2024-03-17 04:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_citas_especialidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Esp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('Especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.esp')),
            ],
        ),
        migrations.AlterField(
            model_name='citas',
            name='Especialidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.esp'),
        ),
    ]