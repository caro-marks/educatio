from django.contrib import admin
from .models import CustomUser, Escola, Aluno, Parente, Atividade, Resultado, Parentesco

# Register your models here.

admin.site.register(CustomUser),
admin.site.register(Escola)
admin.site.register(Aluno)
admin.site.register(Parente)
admin.site.register(Parentesco)
admin.site.register(Atividade)
admin.site.register(Resultado)
