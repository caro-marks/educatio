import datetime
from typing import Any, Dict
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView
from .models import CustomUser, Escola, Aluno, Evento, TipoEvento, NotaEvento, Parente
from .forms import UsuarioForm, CriaEscolaForm, ListAlunosFilter, CriaAlunoForm, CriaParenteForm, ListEventosFilter, CriaEventoForm, CriaTipoEvento#, ListNotasEventoFilter
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
    
### HOMEPAGE

class HomepageView(TemplateView):
    template_name = 'homepage.html'


### USUARIOS

class UsuariosDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'usuarios/detalhe_usuario.html'
    context_object_name = 'usuario'

class UsuarioListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'usuarios/lista_usuarios.html'
    context_object_name = 'usuarios'

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = UsuarioForm
    template_name = 'usuarios/cria_usuario.html'
    success_url = '/usuarios/'

    def form_valid(self, form):
        response = super().form_valid(form)
        novo_usuario = form.instance

        custom_group = Group.objects.get(name='Geral')
        custom_group.user_set.add(novo_usuario)

        return response


### ESCOLAS

class EscolasDetailView(LoginRequiredMixin, DetailView):
    model = Escola
    template_name = 'escolas/detalhe_escola.html'
    context_object_name = 'escola'

class EscolasListView(LoginRequiredMixin, ListView):
    model = Escola
    template_name = 'escolas/lista_escolas.html'
    context_object_name = 'escolas'

class EscolaCreateView(LoginRequiredMixin, CreateView):
    model = Escola
    form_class = CriaEscolaForm
    template_name = 'escolas/cria_escola.html'
    success_url = '/escolas/'

    def form_valid(self, form):
        form.instance.operador = self.request.user
        return super().form_valid(form)


### Aluno

class DetalheAlunoView(LoginRequiredMixin, DetailView):
    model = Aluno
    template_name = 'alunos/detalhe_aluno.html'
    context_object_name = 'aluno'

class ListaAlunosView(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = 'alunos/lista_alunos.html'
    context_object_name = 'alunos'
    form_class = ListAlunosFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        context['alunos'] = self.model.objects.filter(
            ativo=True
        )

        if escola_id := self.request.GET.get('escola'):
            context['alunos'] = self.model.objects.filter(escola__id=escola_id)
        
        alunos_info = []
        for aluno in context['alunos']:
            alunos_info.append(
                {
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'idade': self.get_idade(aluno.data_nascimento),
                })
        
        context['alunos_info'] = alunos_info
        return context
    
    def get_idade(self, data_nascimento):
        data_atual = datetime.date.today()

        idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

        return idade

class AlunoCreateView(LoginRequiredMixin, CreateView):
    model = Aluno
    form_class = CriaAlunoForm
    template_name = 'alunos/cria_aluno.html'

    def get_initial(self):
        initial = super().get_initial()
        if escola_param := self.request.GET.get('escola', None):
            initial['escola'] = escola_param
        return initial
    
    def get_success_url(self):
        aluno_id = self.object.pk
        success_url = reverse('escolas:aluno', kwargs={'pk': aluno_id})
        return success_url

    def form_valid(self, form):
        form.instance.operador = self.request.user
        return super().form_valid(form)


### Parente

class ParenteCreateView(LoginRequiredMixin, CreateView):
    model = Parente
    form_class = CriaParenteForm
    template_name = 'alunos/cria_parente.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['aluno_id'] = self.kwargs.get('aluno_id')
        return context
    
    def get_success_url(self):
        aluno_id = self.kwargs.get('aluno_id')
        success_url = reverse_lazy('escolas:aluno', kwargs={'pk': aluno_id})
        return success_url

    def form_valid(self, form):
        form.instance.operador = self.request.user
        parente = form.save()
        aluno = Aluno.objects.get(pk=self.kwargs.get('aluno_id'))
        aluno.familia.add(parente)
        aluno.save()
        return super().form_valid(form)


class DetalheParenteView(LoginRequiredMixin, DetailView):
    model = Parente
    template_name = 'alunos/detalhe_parente.html'
    context_object_name = 'parente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno_id = self.kwargs.get('aluno_id')
        aluno = Aluno.objects.get(pk=aluno_id)
        context['aluno'] = aluno.nome

        return context


### Evento
class ListaEventosView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/lista_eventos.html'
    context_object_name = 'eventos'
    form_class = ListEventosFilter

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)

        if escola_id := self.request.GET.get('escola'):
            context['eventos'] = self.model.objects.filter(escola__id=escola_id)
        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            
            if data_inicio := form.cleaned_data.get('data_inicio'):
                queryset = queryset.filter(data__gte=data_inicio)
            if data_fim := form.cleaned_data.get('data_fim'):
                queryset = queryset.filter(data__lte=data_fim)
            
        return queryset

class CriaEventoView(LoginRequiredMixin, CreateView):
    model = Evento
    template_name = 'eventos/cria_evento.html'
    form_class = CriaEventoForm
    
    def get_success_url(self):
        evento_id = self.object.pk
        escola = self.model.objects.get(pk=evento_id).escola
        url = reverse('escolas:eventos')
        success_url = f'{url}?escola={escola.id}'
        return success_url

    def get_initial(self):
        initial = super().get_initial()
        if escola_param := self.request.GET.get('escola', None):
            initial['escola'] = escola_param
        return initial

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['form_tipo_evento'] = CriaTipoEvento(self.request.POST)

        return context

class CriaTipoEventoView(LoginRequiredMixin, CreateView):
    model = TipoEvento
    template_name = 'eventos/cria_tipo_evento.html'
    form_class = CriaTipoEvento
    success_url = '/evento/novo/'

# class DetalheEventoView(LoginRequiredMixin, DetailView):
#     model = Evento
#     template_name = 'escolas/detalhe_evento.html'
#     context_object_name = 'evento'

# # ## TipoEvento
# # class ListaTiposEventoView(ListView):
# #     model = TipoEvento
# #     template_name = 'escolas/lista_tipos_evento.html'
# #     context_object_name = 'tipos_evento'

# # class DetalheTipoEventoView(DetailView):
# #     model = TipoEvento
# #     template_name = 'escolas/detalhe_tipo_evento.html'
# #     context_object_name = 'tipo_evento'

# ## NotaEvento
# class ListaNotasEventoView(LoginRequiredMixin, ListView):
#     model = NotaEvento
#     template_name = 'escolas/lista_notas_evento.html'
#     context_object_name = 'notas_evento'
#     form_class = ListNotasEventoForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = self.form_class(self.request.GET)
#         context['form'] = form
#         escola_id = self.request.GET.get('escola')
#         evento_id = self.request.GET.get('evento')
#         data_inicio = self.request.GET.get('data_inicio')
#         data_fim = self.request.GET.get('data_fim')

#         if escola_id:
#             notas_evento = self.model.objects.filter(evento__escola_id=escola_id)
#             if evento_id:
#                 notas_evento = notas_evento.filter(evento_id=evento_id)
#         else:
#             notas_evento = self.model.objects.all()
            
#         if data_inicio:
#             notas_evento = notas_evento.filter(evento__data__gte=data_inicio)
#         if data_fim:
#             notas_evento = notas_evento.filter(evento__data__lte=data_fim)

#         medias = self.get_medias(notas_evento=notas_evento)

#         context['medias'] = medias
#         return context
    
#     def get_medias(self, notas_evento):
#         medias = []
#         alunos = [nota_evento.aluno for nota_evento in notas_evento]
#         for aluno in list(set(alunos)):
#             notas_eventos = notas_evento.filter(aluno=aluno)
#             total_pesos = 0
#             soma_produtos = 0

#             for nota_evento in notas_eventos:
#                 tipo_evento = nota_evento.evento.tipo_evento
#                 peso_evento = tipo_evento.peso
#                 nota_aluno = nota_evento.nota

#                 total_pesos += peso_evento
#                 soma_produtos += nota_aluno * peso_evento

#             if total_pesos != 0:
#                 media_ponderada = soma_produtos / total_pesos
#             else:
#                 media_ponderada = 0
            
#             medias.append(
#                 {
#                     'aluno': aluno.nome,
#                     'media': round(media_ponderada, 2)
#                 }
#             )
#         return medias

# # class DetalheNotaEventoView(DetailView):
# #     model = NotaEvento
# #     template_name = 'escolas/detalhe_nota_evento.html'
# #     context_object_name = 'nota_evento'
