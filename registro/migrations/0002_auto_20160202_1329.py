# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
            ],
        ),
        migrations.AlterModelOptions(
            name='tipo_unidad',
            options={'verbose_name_plural': 'Tipos de unidades'},
        ),
        migrations.AlterField(
            model_name='tamizaje',
            name='resultado',
            field=models.ForeignKey(to='registro.Resultado'),
        ),
    ]
