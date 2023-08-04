from django.urls import path

from .views import (
    # homepage
    HomepageView,

    # usuarios
    UsuariosView,

    # escolas
    EscolaCreateView,
    EscolasDetailView,
    EscolasListView,

    # alunos
    # DetalheAlunoView,
    # ListaAlunosView,

    # eventos
    # DetalheEventoView,
    # ListaEventosView,
    # # DetalheTipoEventoView
    # ListaTiposEventoView,

    # notas
    # ListaNotasEventoView
)

app_name = 'escolas'

urlpatterns = [
    # users
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    path('usuario/novo/', UsuariosView.as_view(), name='cria_usuario'),

    # homepage
    path('', HomepageView.as_view(), name='homepage'),

    # escola
    path('escolas/', EscolasListView.as_view(), name='escolas'),
    path('escola/nova/', EscolaCreateView.as_view(), name='cria_escola'),
    path('escola/<int:pk>/', EscolasDetailView.as_view(), name='escola'),

    # # aluno
    # path('alunos/', ListaAlunosView.as_view(), name='alunos'),
    # path('aluno/<int:pk>/', DetalheAlunoView.as_view(), name='aluno'),

    # # evento
    # path('eventos/', ListaEventosView.as_view(), name='eventos'),
    # path('evento/<int:pk>/', DetalheEventoView.as_view(), name='evento'),

    # # # tipo evento
    # # path('tipos_evento/', ListaTiposEventoView.as_view(), name='tipos_evento'),
    # # path('tipo_evento/<int:pk>/', DetalheTipoEventoView.as_view(), name='tipo_evento')

    # # nota evento
    # path('notas_evento/', ListaNotasEventoView.as_view(), name='notas_evento'),
    # # path('nota_evento/<int:pk>/', DetalheTipoEventoView.as_view(), name='tipo_evento')
]

                # <li class="nav-item">
                #     <a class="nav-link" href="{% url 'escolas:alunos' %}">Alunos</a>
                # </li>
                # <li class="nav-item">
                #     <a class="nav-link" href="{% url 'escolas:eventos' %}">Eventos</a>
                # </li>
                # <li class="nav-item">
                #     <a class="nav-link" href="{% url 'escolas:notas_evento' %}">Relatórios</a>
                # </li>


                
                        # <a role="button" class="btn btn-secondary" href="{% url 'escolas:alunos' %}?escola={{ escola.id|urlencode }}">
                        #     Alunos
                        # </a>
