from django.urls import path

from .views import (
    # homepage
    HomepageView,

    # usuarios
    UsuarioCreateView,
    UsuariosDetailView,
    UsuarioListView,
    UsuarioDesativaView,
    UsuarioUpdateView,

    # escolas
    EscolaCreateView,
    EscolasDetailView,
    EscolasListView,
    EscolaUpdateView,
    EscolaDesativaView,

    # alunos
    DetalheAlunoView,
    ListaAlunosView,
    AlunoCreateView,
    AlunoUpdateView,
    AlunoDesativaView,
    # # parente
    ParenteCreateView,
    DetalheParenteView,
    ParenteUpdateView,

    # atividades
    ListaAtividadeView,
    CriaAtividadeView,
    DetalheAtividadeView,
    EditaAtividadeView,
    RemoveAtividadeView,

    # notas
    ListaResultadosView,
    ListaResultadosAlunoView,
    AlunosSemNotasListView,
    CriarNotaView,
    ListaNotasAlunosEventoView,

    # export
    ExportarDadosNotas
)

app_name = 'escolas'

urlpatterns = [
    # homepage
    path('', HomepageView.as_view(), name='homepage'),

    # users
    path('usuarios/', UsuarioListView.as_view(), name='usuarios'),
    path('usuario/novo/', UsuarioCreateView.as_view(), name='cria_usuario'),
    path('usuario/<int:pk>/', UsuariosDetailView.as_view(), name='usuario'),
    path('usuario/<int:pk>/desativa', UsuarioDesativaView.as_view(), name='desativa_usuario'),
    path('usuario/<int:pk>/edita', UsuarioUpdateView.as_view(), name='edita_usuario'),

    # escola
    path('escolas/', EscolasListView.as_view(), name='escolas'),
    path('escola/nova/', EscolaCreateView.as_view(), name='cria_escola'),
    path('escola/<int:pk>/', EscolasDetailView.as_view(), name='escola'),
    path('escola/<int:pk>/edita', EscolaUpdateView.as_view(), name='edita_escola'),
    path('escola/<int:pk>/desativa', EscolaDesativaView.as_view(), name='desativa_escola'),

    # aluno
    path('alunos/', ListaAlunosView.as_view(), name='alunos'),
    path('aluno/novo/', AlunoCreateView.as_view(), name='cria_aluno'),
    path('aluno/<int:pk>/', DetalheAlunoView.as_view(), name='aluno'),
    path('aluno/<int:pk>/edita', AlunoUpdateView.as_view(), name='edita_aluno'),
    path('aluno/<int:pk>/desativa', AlunoDesativaView.as_view(), name='desativa_aluno'),

    # parente
    path('aluno/<int:aluno_id>/parente/novo/', ParenteCreateView.as_view(), name='cria_parente'),
    path('aluno/parente/<int:pk>/', DetalheParenteView.as_view(), name='parente'),
    path('aluno/parente/<int:pk>/edita/', ParenteUpdateView.as_view(), name='edita_parente'),

    # # atividade
    path('atividades/', ListaAtividadeView.as_view(), name='atividades'),
    path('atividade/nova/', CriaAtividadeView.as_view(), name='cria_atividade'),
    path('atividade/<int:pk>/', DetalheAtividadeView.as_view(), name='atividade'),
    path('atividade/<int:pk>/edita/', EditaAtividadeView.as_view(), name='edita_atividade'),
    path('atividade/<int:pk>/remove/', RemoveAtividadeView.as_view(), name='remove_atividade'),

    # # nota evento
    path('resultados/', ListaResultadosView.as_view(), name='resultados'),
    path('resultados/aluno/<int:aluno_id>/', ListaResultadosAlunoView.as_view(), name='resultados_aluno'),
    path('resultados/atividade/<int:atividade_id>/alunos_sem_notas', AlunosSemNotasListView.as_view(), name='alunos_sem_notas'),
    path('resultados/atividade/<int:atividade_id>/aluno/<int:aluno_id>/', CriarNotaView.as_view(), name='avaliar_aluno'),
    path('resultados/atividade/<int:atividade_id>/alunos_com_notas', ListaNotasAlunosEventoView.as_view(), name='alunos_com_notas'),

    # # dados
    path('exportar_dados_notas/', ExportarDadosNotas.as_view(), name='exportar_dados_notas')
]
                        