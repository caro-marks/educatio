from django.contrib import admin
from .models import Escola, Aluno, TipoEvento, Evento, NotaEvento

# Register your models here.

admin.site.register(Escola)
admin.site.register(Aluno)
admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(NotaEvento)
