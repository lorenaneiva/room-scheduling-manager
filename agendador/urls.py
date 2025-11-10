from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('salas', views.salas, name='salas'),
    path('agendar/<sala_id>/', views.agendar, name='agendar'),
    path('agendamentos_pendentes', views.agendamentos_pendentes, name='agendamentos_pendentes'),
    path('agendamentos_pendentes/<agendamento_id>/aceitar', views.aceitar_agendamento, name='aceitar'),
    path('agendamentos_pendentes/<agendamento_id>/rejeitar', views.rejeitar_agendamento, name='rejeitar'),
    path('gerenciar_salas', views.gerenciar_salas, name='gerenciar_salas')
]
