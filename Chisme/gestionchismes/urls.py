# Copyright [2016] [Leoncio Ramos Carrasco]
#Licensed under the Apache License, Version 2.0 you may not use this file except in compliance You may obtain a copy of the License at

from django.conf.urls import patterns, url
from gestionchismes import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =  patterns('', 
	url(r'logueo/$', views.logueo, name='logueo'),
	url(r'logoff/$', views.logoff, name='logoff'),
	url(r'crear/$', views.create, name='create'),
	url(r'crearchisme/$', views.crearchisme, name='crearchisme'),
	url(r'cuenta/$', views.cuenta, name='cuenta'),
	url(r'seguir/(?P<user_id>\w+)/$', views.seguir, name='seguirusuario'),
	url(r'dejar/(?P<user_id>\w+)/$', views.dejar, name='dejar'),
	url(r'eliminar/(?P<mens_id>\d+)/$', views.eliminarchisme, name='eliminarchisme'),
	url(r'fav/(?P<user_id>\w+)/(?P<mens_id>\d+)/$', views.fav, name='fav'),
	url(r'baja/(?P<user_id>\w+)/$', views.dardebaja, name='baja'),
	url(r'pulsan_favorito/(?P<mens_id>\d+)/$', views.pulsan_favorito, name='pulsan_favorito'),
	url(r'pulsan_retweet/(?P<mens_id>\d+)/$', views.pulsan_retweet, name='pulsan_retweet'),
	url(r'buscapersonalizada/$', views.buscar, name='buscar'),
	url(r'retuit/(?P<user_id>\w+)/(?P<mens_id>\d+)/$', views.retuit, name='retwit'),
	
 #para acceder hay que poner nombre_api/add
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


