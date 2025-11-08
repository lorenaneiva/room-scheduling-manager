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
        'salas':salas
    }

    return render(request,'agendador/salas.html', context)

def agendar(request, sala_id):
    if request.method != 'POST':
        form = AgendamentoForm()
    else:
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                novo_agendamento = form.save(commit=False)
                novo_agendamento.professor = request.user
                novo_agendamento.sala = get_object_or_404(Sala, id=sala_id)
                hoje = date.today()
                amanha = hoje + timedelta(days=1)
                novo_agendamento.data_agendamento = amanha 
                novo_agendamento.save()
            messages.success(request, 'Solicitação de agendamento feita com sucesso!')
            return HttpResponseRedirect(reverse('salas'))
    context = {
        'form': form,
        'sala_id':sala_id
    }
    return render(request,'agendador/agendar.html', context)