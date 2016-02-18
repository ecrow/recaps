# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0003_tamizaje_unidad_realiza'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unidad_Asignacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Activo'), (b'C', b'Cancelado')])),
                ('envia', models.ForeignKey(related_name='envia', to='registro.Unidad')),
                ('recibe', models.ForeignKey(to='registro.Unidad')),
            ],
            options={
                'verbose_name_plural': 'Unidad_Asignaciones',
            },
        ),
    ]
