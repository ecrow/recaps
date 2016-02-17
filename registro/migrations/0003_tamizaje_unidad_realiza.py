# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0002_auto_20160202_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='tamizaje',
            name='unidad_realiza',
            field=models.ForeignKey(default=1, to='registro.Unidad'),
            preserve_default=False,
        ),
    ]
