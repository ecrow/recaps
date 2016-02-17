# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrareferencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_envio', models.DateTimeField(default=django.utils.timezone.now)),
                ('observaciones', models.TextField(blank=True)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
        ),
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domicilio', models.TextField(blank=True)),
                ('telefono', models.CharField(max_length=10, null=True, blank=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clave', models.CharField(max_length=2)),
                ('descripcion', models.CharField(max_length=100)),
                ('abreviatura', models.CharField(max_length=50)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clave', models.CharField(max_length=4)),
                ('descripcion', models.CharField(max_length=150)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
            options={
                'verbose_name_plural': 'Localidades',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clave', models.CharField(max_length=3)),
                ('descripcion', models.CharField(max_length=150)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
                ('estado', models.ForeignKey(to='registro.Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Obstetrico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fum', models.DateTimeField()),
                ('ultrasonido', models.BooleanField(default=False)),
                ('gesta', models.IntegerField()),
                ('factores_riesgo', models.TextField(blank=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('edad', models.IntegerField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
        ),
        migrations.CreateModel(
            name='Referencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_envio', models.DateTimeField(default=django.utils.timezone.now)),
                ('observaciones', models.TextField(blank=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
                ('paciente', models.ForeignKey(to='registro.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Tamizaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_consulta', models.DateTimeField(default=django.utils.timezone.now)),
                ('resultado', models.BooleanField(default=False)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
                ('paciente', models.ForeignKey(to='registro.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Tamizaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
            options={
                'verbose_name_plural': 'Tipo de tamizajes',
            },
        ),
        migrations.CreateModel(
            name='Tipo_Tratamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
            options={
                'verbose_name_plural': 'Tipo de tratamientos',
            },
        ),
        migrations.CreateModel(
            name='Tipo_Unidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
            options={
                'verbose_name_plural': 'Tipo de unidades',
            },
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clues', models.CharField(max_length=11)),
                ('descripcion', models.CharField(max_length=300)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
                ('tipo_unidad', models.ForeignKey(to='registro.Tipo_Unidad')),
            ],
            options={
                'verbose_name_plural': 'Unidades',
            },
        ),
        migrations.CreateModel(
            name='Usuario_Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Unidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
                ('unidad', models.ForeignKey(to='registro.Unidad')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tamizaje',
            name='tipo_tamizaje',
            field=models.ForeignKey(to='registro.Tipo_Tamizaje'),
        ),
        migrations.AddField(
            model_name='tamizaje',
            name='tipo_tratamiento',
            field=models.ForeignKey(to='registro.Tipo_Tratamiento'),
        ),
        migrations.AddField(
            model_name='tamizaje',
            name='usuario_registro',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='referencia',
            name='tipo_tamizaje',
            field=models.ForeignKey(to='registro.Tipo_Tamizaje'),
        ),
        migrations.AddField(
            model_name='referencia',
            name='unidad_recibe',
            field=models.ForeignKey(to='registro.Unidad'),
        ),
        migrations.AddField(
            model_name='referencia',
            name='unidad_refiere',
            field=models.ForeignKey(related_name='unidad_refiere', to='registro.Unidad'),
        ),
        migrations.AddField(
            model_name='referencia',
            name='usuario_registro',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paciente',
            name='unidad',
            field=models.ForeignKey(to='registro.Unidad'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='usuario_registro',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='obstetrico',
            name='paciente',
            field=models.ForeignKey(to='registro.Paciente'),
        ),
        migrations.AddField(
            model_name='obstetrico',
            name='usuario_registro',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='localidad',
            name='municipio',
            field=models.ForeignKey(to='registro.Municipio'),
        ),
        migrations.AddField(
            model_name='domicilio',
            name='localidad',
            field=models.ForeignKey(to='registro.Localidad'),
        ),
        migrations.AddField(
            model_name='domicilio',
            name='paciente',
            field=models.ForeignKey(to='registro.Paciente'),
        ),
        migrations.AddField(
            model_name='domicilio',
            name='usuario_registro',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contrareferencia',
            name='paciente',
            field=models.ForeignKey(to='registro.Paciente'),
        ),
        migrations.AddField(
            model_name='contrareferencia',
            name='unidad_contrarefiere',
            field=models.ForeignKey(related_name='unidad_contrarefiere', to='registro.Unidad'),
        ),
        migrations.AddField(
            model_name='contrareferencia',
            name='unidad_recibe',
            field=models.ForeignKey(to='registro.Unidad'),
        ),
        migrations.AddField(
            model_name='contrareferencia',
            name='usuario_registro',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
