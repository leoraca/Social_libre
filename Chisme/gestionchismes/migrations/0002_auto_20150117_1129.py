# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionchismes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorito',
            name='num_favorito',
        ),
        migrations.AddField(
            model_name='mensaje',
            name='num_favorito',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
