from django.shortcuts import render
from .models import User, Agendamento, Sala
from datetime import date

def index(request):
    data_atual = date.today()
    agendamentos = (Agendamento.objects.filter(data_agendamento=data_atual, status='aceito')
                    .distinct()
                    .select_related('professor','sala')
                    )
    salas = Sala.objects.order_by('capacidade')
    context = {
        'data_atual':data_atual,
        'agendamentos':agendamentos,
        'salas':salas     
        }
    return render(request, 'agendador/index.html', context)

def agendar(request):
    salas = Sala.objects.order_by('capacidade')

    context = {
        'salas':salas
    }

    return render(request,'agendador/agendar.html', context)