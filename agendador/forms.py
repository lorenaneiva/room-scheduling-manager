from django import forms
from .models import Agendamento
from django.forms import widgets
from django.core.exceptions import ValidationError

class AgendamentoForm(forms.ModelForm):
    hora_fim = forms.TimeField(
        widget=widgets.TimeInput(attrs={'type': 'time'}),
        label='Hora final')
    hora_inicio = forms.TimeField(
        widget=widgets.TimeInput(attrs={'type': 'time'}),
        label='Hora inicial')
    
    class Meta():
        model = Agendamento
        fields = ['hora_inicio','hora_fim','materia','observação']
        labels = {'materia':'Matéria', 'observação': 'Observação'}

    def clean(self):
        # clean da classe pai
        cleaned_data = super().clean()
        hora_i = cleaned_data.get('hora_inicio')
        hora_f = cleaned_data.get('hora_fim')

        if hora_i and hora_f:
            inicio_segundos = hora_i.hour * 3600 + hora_i.minute * 60 + hora_i.second
            fim_segundos = hora_f.hour * 3600 + hora_f.minute * 60 + hora_f.second
            duracao = fim_segundos - inicio_segundos
            if hora_i >= hora_f:
                raise ValidationError("A hora inicial deve ser antes da hora final.")
            if duracao < 3600:
                raise ValidationError("A reserva da sala deve ser de pelo menos 1h.")
            if duracao > 14400:
                raise ValidationError("A reserva da sala deve ser de no máximo 4h.")
