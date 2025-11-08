from django.shortcuts import render
from .models import User, Agendamento, Sala
from .forms import AgendamentoForm
from datetime import date, timedelta
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

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

def salas(request):
    salas = Sala.objects.order_by('capacidade')
    context = {
        'salas':salas,
    }

    return render(request,'agendador/salas.html', context)

def agendar(request, sala_id):
    if request.method != 'POST':
        form = AgendamentoForm()
    else:
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            
            novo_agendamento = form.save(commit=False)
            novo_agendamento.professor = request.user
            novo_agendamento.sala = get_object_or_404(Sala, id=sala_id)
            novo_agendamento.data_agendamento = date.today() + timedelta(days=1)
        
            conflito = Agendamento.objects.filter(
                sala=novo_agendamento.sala,
                data_agendamento=novo_agendamento.data_agendamento,
                status='aceito'
            ).filter(
                hora_inicio__lt=novo_agendamento.hora_fim, # hora_inicio é menor que a hora_fim
                hora_fim__gt=novo_agendamento.hora_inicio # hora_fim é maior que a hora_inicio
            ).exists()
            if conflito:
                hoje = date.today()
                amanha = hoje + timedelta(days=1)  
                messages.error(request, "Essa sala já está reservada nesse horário.")
                return render(request, 'agendador/agendar.html', {'form': form, 'sala_id': sala_id, 'amanha':amanha})
            
            with transaction.atomic():
                novo_agendamento.save()
            messages.success(request, 'Solicitação de agendamento feita com sucesso!')
            return HttpResponseRedirect(reverse('salas'))
    hoje = date.today()
    amanha = hoje + timedelta(days=1)    
    context = {
        'form': form,
        'sala_id':sala_id,
        'amanha':amanha
    }
    return render(request,'agendador/agendar.html', context)

def agendamentos_pendentes(request):
    agendamentos = (Agendamento.objects.filter(status='pendente')
                    .distinct()
                    .select_related('professor','sala')
                    )
    salas = Sala.objects.order_by('capacidade')
    context = {
        'agendamentos':agendamentos,
        'salas':salas
    }
    return render(request,'agendador/agendamentos_pendentes.html', context)
