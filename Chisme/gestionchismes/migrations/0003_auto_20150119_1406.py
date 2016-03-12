# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionchismes', '0002_auto_20150117_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='retweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje_id', models.ForeignKey(to='gestionchismes.Mensaje')),
                ('relacion_retweet', models.ManyToManyField(related_name='retuiteado_por', null=True, to='gestionchismes.Chismero', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='num_retweet',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
