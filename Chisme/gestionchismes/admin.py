from django.contrib import admin
from gestionchismes.models import Chismero, Mensaje, Favorito, Retweet
# Register your models here.

admin.site.register(Chismero)
admin.site.register(Mensaje)
admin.site.register(Favorito)
admin.site.register(Retweet)