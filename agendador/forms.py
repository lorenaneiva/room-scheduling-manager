from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    hora_inicio, hora_fim = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type':'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
        label='Prazo')
    
    class Meta():
        model = Agendamento
        fields = ['hora_inicio','hora_fim','materia','observação']
        labels = {'hora_inicio':'Hora inicial','hora_fim': 'Hora final', 'materia':'Matéria', 'observação': 'Observação'}