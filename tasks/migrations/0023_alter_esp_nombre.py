# Generated by Django 5.0.2 on 2024-03-23 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_citas_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esp',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
