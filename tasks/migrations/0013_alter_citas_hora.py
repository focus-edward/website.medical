# Generated by Django 5.0.2 on 2024-03-18 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_delete_hora_alter_citas_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citas',
            name='Hora',
            field=models.TimeField(null=True),
        ),
    ]
