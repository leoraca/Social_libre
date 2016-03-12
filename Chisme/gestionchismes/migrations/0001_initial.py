# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chismero',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('seguidores', models.ManyToManyField(related_name='seguido_por', null=True, to='gestionchismes.Chismero', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_favorito', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('mensaje_id', models.AutoField(serialize=False, primary_key=True)),
                ('texto', models.CharField(max_length=140)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('username', models.ForeignKey(to='gestionchismes.Chismero')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='favorito',
            name='mensaje_id',
            field=models.ForeignKey(to='gestionchismes.Mensaje'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favorito',
            name='relacion_favoritos',
            field=models.ManyToManyField(related_name='favorito_de', null=True, to='gestionchismes.Chismero', blank=True),
            preserve_default=True,
        ),
    ]
