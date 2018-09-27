from django.conf.urls import include, url
from . import views


app_name = 'importer'

urlpatterns = [
    url(r'^importar', views.upload_csv, name='upload_csv'),
    url(r'^exportar', views.exportar_csv, name='exportar_csv'),
    url(r'^identificar', views.identificar, name='identificar'),
    url(r'^', views.base, name='base'),
]