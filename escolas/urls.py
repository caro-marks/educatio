from django.urls import path

from .views import (
    # homepage
    HomepageView,

    # usuarios
    UsuarioCreateView,
    UsuariosDetailView,
    UsuarioListView,

    # escolas
    EscolaCreateView,
    EscolasDetailView,
    EscolasListView,

    # alunos
    DetalheAlunoView,
    ListaAlunosView,
    AlunoCreateView,
    # # parente
    ParenteCreateView,
    DetalheParenteView,

    # eventos
    # DetalheEventoView,
    ListaEventosView,
    CriaEventoView,
    CriaTipoEventoView,
    # # DetalheTipoEventoView
    # ListaTiposEventoView,

    # notas
    # ListaNotasEventoView
)

app_name = 'escolas'

urlpatterns = [
    # homepage
    path('', HomepageView.as_view(), name='homepage'),

    # users
    path('usuarios/', UsuarioListView.as_view(), name='usuarios'),
    path('usuario/novo/', UsuarioCreateView.as_view(), name='cria_usuario'),
    path('usuario/<int:pk>/', UsuariosDetailView.as_view(), name='usuario'),

    # escola
    path('escolas/', EscolasListView.as_view(), name='escolas'),
    path('escola/nova/', EscolaCreateView.as_view(), name='cria_escola'),
    path('escola/<int:pk>/', EscolasDetailView.as_view(), name='escola'),

    # aluno
    path('alunos/', ListaAlunosView.as_view(), name='alunos'),
    path('aluno/novo/', AlunoCreateView.as_view(), name='cria_aluno'),
    path('aluno/<int:pk>/', DetalheAlunoView.as_view(), name='aluno'),

    # parente
    path('aluno/<int:aluno_id>/parente/novo/', ParenteCreateView.as_view(), name='cria_parente'),
    path('aluno/<int:aluno_id>/parente/<int:pk>/', DetalheParenteView.as_view(), name='parente'),

    # # evento
    path('eventos/', ListaEventosView.as_view(), name='eventos'),
    path('evento/novo/', CriaEventoView.as_view(), name='cria_evento'),
    path('cria_tipo_evento/', CriaTipoEventoView.as_view(), name='cria_tipo_evento'),
    # path('evento/<int:pk>/', DetalheEventoView.as_view(), name='evento'),

    # # # tipo evento
    # # path('tipos_evento/', ListaTiposEventoView.as_view(), name='tipos_evento'),
    # # path('tipo_evento/<int:pk>/', DetalheTipoEventoView.as_view(), name='tipo_evento')

    # # nota evento
    # path('notas_evento/', ListaNotasEventoView.as_view(), name='notas_evento'),
    # # path('nota_evento/<int:pk>/', DetalheTipoEventoView.as_view(), name='tipo_evento')
]

                
                
                # <li class="nav-item">
                #     <a class="nav-link" href="{% url 'escolas:notas_evento' %}">Relatórios</a>
                # </li>
                        