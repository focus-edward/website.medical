# Generated by Django 5.0.2 on 2024-04-02 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0032_alter_citas_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citas',
            name='Hora',
            field=models.CharField(default=1000, max_length=3),
            preserve_default=False,
        ),
    ]