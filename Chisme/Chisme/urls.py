from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from gestionchismes.views import mostrar
from gestionchismes import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Chisme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', mostrar, name='mostrar'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gestionchismes/', include('gestionchismes.urls')),
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

