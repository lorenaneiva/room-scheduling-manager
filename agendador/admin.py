from django.contrib import admin
from agendador.models import User, Agendamento, Sala

admin.site.register(User)
admin.site.register(Agendamento)
admin.site.register(Sala)