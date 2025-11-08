from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('salas', views.salas, name='salas'),
    path('agendar/<sala_id>/', views.agendar, name='agendar')
]
