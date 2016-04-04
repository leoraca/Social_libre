# Copyright [2016] [Leoncio Ramos Carrasco]
#Licensed under the Apache License, Version 2.0 you may not use this file except in compliance You may obtain a copy of the License at


from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
import hashlib
# Create your models here.

class Chismero(User):
	seguidores=models.ManyToManyField('self', blank=True, null=True, related_name='seguido_por', symmetrical=False)
	
class Mensaje(models.Model):
	mensaje_id=models.AutoField(primary_key=True)
	texto=models.CharField(max_length=140)
	username=models.ForeignKey(Chismero) #Un user tiene varios mensajes
	fecha_registro=models.DateTimeField(auto_now_add=True) #preguntar como mostrar
	num_favorito=models.IntegerField(default=0)
	num_retweet=models.IntegerField(default=0)
	def __unicode__(self):
		return self.texto
class Favorito(models.Model):
	mensaje_id=models.ForeignKey(Mensaje)
	relacion_favoritos=models.ManyToManyField(Chismero, blank=True, null=True, related_name='favorito_de', symmetrical=False)
	
class Retweet(models.Model):
	mensaje_id=models.ForeignKey(Mensaje)
	relacion_retweet=models.ManyToManyField(Chismero, blank=True, null=True, related_name='retuiteado_por', symmetrical=False)
	