# Generated by Django 5.0.2 on 2024-04-09 23:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Esp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cedula', models.TextField(max_length=11)),
                ('edad', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DisponibilidadCita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=12)),
                ('hora', models.TimeField()),
                ('cupos_disponibles', models.PositiveIntegerField()),
                ('consultorio', models.IntegerField(null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.doctor')),
                ('especialidad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.esp')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='Especialidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.esp'),
        ),
        migrations.CreateModel(
            name='Citas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(default='01/01/2024', max_length=12)),
                ('Hora', models.TimeField()),
                ('Consultorio', models.CharField(max_length=3)),
                ('Estado', models.TextField(default='Pendiente')),
                ('Nombre_del_paciente', models.TextField(max_length=100)),
                ('Cédula_del_paciente', models.TextField(max_length=11)),
                ('edad', models.IntegerField(null=True)),
                ('Teléfono_de_contacto', models.TextField(max_length=20)),
                ('Síntomas', models.TextField(max_length=100)),
                ('Información_relevante', models.TextField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datecompleted', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('Calendario_de_disponibilidad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.disponibilidadcita')),
                ('Doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.doctor')),
                ('Especialidad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.esp')),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='PerfilAnalista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.TextField(max_length=50, null=True)),
                ('apellidos', models.TextField(max_length=50, null=True)),
                ('edad', models.IntegerField(null=True)),
                ('direccion', models.CharField(max_length=254, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paciente',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.perfilusuario'),
        ),
    ]