from django.urls import path

from .views import (
    # homepage
    HomepageView,

    # lista
    ListaAlunosView,
    ListaEscolasView,
    ListaEventosView,
    # ListaTiposEventoView,

    # detalhe
    DetalheAlunoView,
    DetalheEscolaView,
    DetalheEventoView,
    # DetalheTipoEventoView
)

app_name = 'escolas'

urlpatterns = [
    # homepage
    path('', HomepageView.as_view(), name='homepage'),

    # escola
    path('escolas/', ListaEscolasView.as_view(), name='escolas'),
    path('escola/<int:pk>/', DetalheEscolaView.as_view(), name='escola'),

    # aluno
    path('alunos/', ListaAlunosView.as_view(), name='alunos'),
    path('aluno/<int:pk>/', DetalheAlunoView.as_view(), name='aluno'),

    # evento
    path('eventos/', ListaEventosView.as_view(), name='eventos'),
    path('evento/<int:pk>/', DetalheEventoView.as_view(), name='evento'),

    # # tipo evento
    # path('tipos_evento/', ListaTiposEventoView.as_view(), name='tipos_evento'),
    # path('tipo_evento/<int:pk>/', DetalheTipoEventoView.as_view(), name='tipo_evento')
]
