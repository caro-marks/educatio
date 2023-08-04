from django.contrib import admin
from .models import CustomUser, Escola, Aluno, TipoEvento, Evento, NotaEvento, Parente

# Register your models here.

admin.site.register(CustomUser),
admin.site.register(Escola)
admin.site.register(Aluno)
admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(NotaEvento)
admin.site.register(Parente)
