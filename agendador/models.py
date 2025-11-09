from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('professor','Professor'),
        ('administrador','Administrador'),
    ]
    role = models.CharField(max_length=20,choices=ROLE_CHOICES, default='professor')
    def __str__(self):
        return self.username


class Sala(models.Model):

    nome = models.CharField(max_length=200)
    capacidade = models.IntegerField()
    recursos = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    localização = models.CharField(max_length=300)
    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado')
    ]

    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
    materia = models.CharField(max_length=200)
    observação = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='pendente', max_length=30)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="salas")
    data_agendamento = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.sala.nome} - {self.hora_inicio} até {self.hora_fim} do dia {self.data_agendamento} - {self.professor.username}"