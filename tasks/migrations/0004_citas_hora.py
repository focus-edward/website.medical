# Generated by Django 5.0.2 on 2024-03-13 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_citas_consultorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='citas',
            name='Hora',
            field=models.IntegerField(null=True),
        ),
    ]
