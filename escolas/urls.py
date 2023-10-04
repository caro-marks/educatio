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
    EscolaUpdateView,
    EscolaDesativaView,

#     # alunos
#     DetalheAlunoView,
#     ListaAlunosView,
#     AlunoCreateView,
#     AlunoUpdateView,
#     AlunoDesativaView,
#     # # parente
#     ParenteCreateView,
#     DetalheParenteView,

#     # eventos
#     ListaEventosView,
#     CriaEventoView,
#     CriaTipoEventoView,

#     # notas
#     ListaNotasEventoView,
#     ListaNotasAlunoView,
#     AlunosSemNotasListView,
#     CriarNotaView,
#     ListaNotasAlunosEventoView,

#     # export
#     ExportarDadosNotas
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
    path('escola/<int:pk>/edita', EscolaUpdateView.as_view(), name='edita_escola'),
    path('escola/<int:pk>/desativa', EscolaDesativaView.as_view(), name='desativa_escola'),

#     # aluno
#     path('alunos/', ListaAlunosView.as_view(), name='alunos'),
#     path('aluno/novo/', AlunoCreateView.as_view(), name='cria_aluno'),
#     path('aluno/<int:pk>/', DetalheAlunoView.as_view(), name='aluno'),
#     path('aluno/<int:pk>/edita', AlunoUpdateView.as_view(), name='edita_aluno'),
#     path('aluno/<int:pk>/desativa', AlunoDesativaView.as_view(), name='desativa_aluno'),

#     # parente
#     path('aluno/<int:aluno_id>/parente/novo/', ParenteCreateView.as_view(), name='cria_parente'),
#     path('aluno/<int:aluno_id>/parente/<int:pk>/', DetalheParenteView.as_view(), name='parente'),

#     # # evento
#     path('eventos/', ListaEventosView.as_view(), name='eventos'),
#     path('evento/novo/', CriaEventoView.as_view(), name='cria_evento'),
#     path('cria_tipo_evento/', CriaTipoEventoView.as_view(), name='cria_tipo_evento'),

#     # # nota evento
#     path('notas_evento/', ListaNotasEventoView.as_view(), name='notas_evento'),
#     path('notas_evento/aluno/<int:aluno_id>/', ListaNotasAlunoView.as_view(), name='notas_aluno'),
#     path('notas_evento/evento/<int:evento_id>/alunos_sem_notas', AlunosSemNotasListView.as_view(), name='alunos_sem_notas'),
#     path('notas_evento/evento/<int:evento_id>/aluno/<int:aluno_id>/', CriarNotaView.as_view(), name='criar_nota_aluno'),
#     path('notas_evento/evento/<int:evento_id>/alunos_com_notas', ListaNotasAlunosEventoView.as_view(), name='alunos_com_notas'),

#     # # dados
#     path('exportar_dados_notas/', ExportarDadosNotas.as_view(), name='exportar_dados_notas')
]
                        