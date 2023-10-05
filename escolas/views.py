import datetime, csv
# from typing import Any, Dict
# from django.db.models.query import QuerySet
# from django.forms.models import BaseModelForm
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView, UpdateView
from .models import CustomUser, Escola, Aluno, Parente, Atividade, Resultado
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
# from django.http import HttpRequest, HttpResponse
from .forms import (
    UsuarioForm, 
    
    CriaEscolaForm, 
    EditaEscolaForm, 
    
    ListAlunosFilter, 
    CriaAlunoForm,
    EditaAlunoForm,
    CriaParenteForm, 

#     # ListEventosFilter, 

#     CriaEventoForm, 
#     CriaTipoEventoForm, 
    
#     ListNotasEventoFilter, 
#     AvaliarEventoForm,
)
    
### HOMEPAGE

class HomepageView(TemplateView):
    """
    Pagina inicial da aplicaçao. É protegida no frontend, mas nao esconde nada, alem de um navegador com links pra rotas protegidas pelo backend.

    TODO: ver se é possível utilizar esta mesma view pra acrescentar dados relevantes sobre os objetos da aplicaçao, como quantidade de alunos ativos por escola, eventos sem avaliações, media mais alta na semana/mes, etc. Ps.: dados relevantes são subjetivos, e limitados pela estrutura do sistema.
    """
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
    """
    Lista as escolas ativas
    """
    model = Escola
    template_name = 'escolas/lista_escolas.html'
    context_object_name = 'escolas'

    def get_queryset(self):
        queryset = super().get_queryset().filter(ativo=True)
        return queryset.order_by('nome')
 
class EscolaCreateView(LoginRequiredMixin, CreateView):
    """
    Cria uma escola, e retorna pra lista de escolas
    """
    model = Escola
    form_class = CriaEscolaForm
    template_name = 'escolas/cria_escola.html'
    
    def get_success_url(self):
        return reverse('escolas:escola', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.operador = self.request.user
        form.instance.ativo = True
        return super().form_valid(form)

class EscolaUpdateView(LoginRequiredMixin, UpdateView):
    model = Escola
    form_class = EditaEscolaForm
    template_name = 'escolas/edita_escola.html'
    
    def get_success_url(self):
        return reverse('escolas:escola', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.operador = self.request.user
        return super().form_valid(form)
    
class EscolaDesativaView(LoginRequiredMixin, View):
    model = Escola
    # success_url ='/escolas/'
    
    def get(self, request, pk):
        objeto = get_object_or_404(self.model, pk=pk)
        objeto.ativo = False
        objeto.save()
        redirect_url = reverse('escolas:escolas')
        return redirect(redirect_url) 


### Aluno
class DetalheAlunoView(LoginRequiredMixin, DetailView):
    model = Aluno
    template_name = 'alunos/detalhe_aluno.html'
    context_object_name = 'aluno'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parente_form'] = CriaParenteForm()
        return context

class ListaAlunosView(LoginRequiredMixin, TemplateView):
    model = Aluno
    template_name = 'alunos/lista_alunos.html'
    form_class = ListAlunosFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        context['alunos'] = self.model.objects.filter(
            ativo=True
        ).order_by('nome')

        if escola_id := self.request.GET.get('escola'):
            context['alunos'] = self.model.objects.filter(escola__id=escola_id)
        
        alunos_info = []
        for aluno in context['alunos']:
            alunos_info.append(
                {
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'escola': aluno.escola,
                    'idade': self.get_idade(aluno.data_nascimento),
                })
        
        context['alunos'] = alunos_info
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
        form.instance.ativo = True
        return super().form_valid(form)

class AlunoUpdateView(LoginRequiredMixin, UpdateView):
    model = Aluno
    form_class = EditaAlunoForm
    template_name = 'alunos/edita_aluno.html'
    
    def get_success_url(self) -> str:
        return reverse('escolas:aluno', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.operador = self.request.user
        return super().form_valid(form)

class AlunoDesativaView(LoginRequiredMixin, View):
    model = Aluno
    
    def get(self, request, pk):
        objeto = get_object_or_404(self.model, pk=pk)
        objeto.ativo = False
        objeto.save()
        redirect_url = reverse('escolas:alunos')
        return redirect(redirect_url) 

### Parente
class ParenteCreateView(LoginRequiredMixin, CreateView):
    model = Parente
    form_class = CriaParenteForm
    template_name = 'alunos/cria_parente.html'

    def get_context_data(self, **kwargs):
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


# ### Evento
# class ListaEventosView(LoginRequiredMixin, ListView):
#     model = Evento
#     template_name = 'eventos/lista_eventos.html'
#     context_object_name = 'eventos'
#     # form_class = ListEventosFilter

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         # context['form'] = self.form_class(self.request.GET)

#         # if escola_id := self.request.GET.get('escola'):
#         #     context['eventos'] = self.model.objects.filter(escola__id=escola_id).order_by('descricao', 'tipo_evento', 'escola')
        
#         return context

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # form = self.form_class(self.request.GET)
#         # if form.is_valid():
            
#         #     if data_inicio := form.cleaned_data.get('data_inicio'):
#         #         queryset = queryset.filter(data__gte=data_inicio)
#         #     if data_fim := form.cleaned_data.get('data_fim'):
#         #         queryset = queryset.filter(data__lte=data_fim)
            
#         return queryset.order_by('descricao', 'tipo_evento','escola')

# class CriaEventoView(LoginRequiredMixin, CreateView):
#     model = Evento
#     template_name = 'eventos/cria_evento.html'
#     form_class = CriaEventoForm
    
#     def get_success_url(self):
#         evento_id = self.object.pk
#         escola = self.model.objects.get(pk=evento_id).escola
#         url = reverse('escolas:eventos')
#         success_url = f'{url}?escola={escola.id}'
#         return success_url

#     def get_initial(self):
#         initial = super().get_initial()
#         if escola_param := self.request.GET.get('escola', None):
#             initial['escola'] = escola_param
#         return initial

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context =  super().get_context_data(**kwargs)
#         context['form_tipo_evento'] = CriaTipoEventoForm()

#         return context
    
#     def form_valid(self, form: BaseModelForm) -> HttpResponse:
#         form = super().form_valid(form)
#         print(f'form: {form}')
#         return form

# class CriaTipoEventoView(LoginRequiredMixin, CreateView):
#     model = TipoEvento
#     template_name = 'eventos/cria_tipo_evento.html'
#     form_class = CriaTipoEventoForm
#     success_url = '/evento/novo/'


# ### NotaEvento

# def get_notas_data(notas_evento):
#     medias = []
#     alunos = [notas_evento.aluno for notas_evento in notas_evento]
#     for aluno in list(set(alunos)):
#         notas_eventos = notas_evento.filter(aluno=aluno)
#         total_pesos = 0
#         soma_produtos = 0

#         for nota_evento in notas_eventos:
#             tipo_evento = nota_evento.evento.tipo_evento
#             peso_evento = tipo_evento.peso
#             nota_aluno = nota_evento.nota

#             total_pesos += peso_evento
#             soma_produtos += nota_aluno * peso_evento

#         if total_pesos != 0:
#             media_ponderada = soma_produtos / total_pesos
#         else:
#             media_ponderada = 0
        
#         medias.append(
#             {
#                 'aluno_id': aluno.id,
#                 'aluno': aluno.nome,
#                 'resultado': round(media_ponderada, 2),
#                 'escola': aluno.escola.nome,
#                 'detalhes': [
#                     {
#                         'nota_id': nota_eventos.id,
#                         'nota': nota_eventos.nota

#                     } for nota_eventos in notas_eventos
#                 ]
#             }
#         )

#     return sorted(
#         medias,
#         key=lambda media: (-media['resultado'], media['aluno']),
#         # reverse=(True, False)
#     )


# def get_notas_evento(escola_id, evento_id, data_inicio, data_fim):
#     nota_field = 'Media' if evento_id else 'Avaliação'
#     # se for especificado o evento_id, o resultado nao vai ser media, e sim avaliaçao
#     if escola_id:
#         notas_evento = NotaEvento.objects.filter(evento__escola_id=escola_id)
#         if evento_id:
#             notas_evento = notas_evento.filter(evento_id=evento_id)
#     elif evento_id:
#         notas_evento = NotaEvento.objects.filter(evento_id=evento_id)
#     else:
#         notas_evento = NotaEvento.objects.all()

#     if data_inicio:
#         notas_evento = notas_evento.filter(data_entrega__gte=data_inicio)
#         # notas_evento = notas_evento.filter(evento__data__gte=data_inicio)
#     if data_fim:
#         notas_evento = notas_evento.filter(data_entrega__lte=data_fim)
#         # notas_evento = notas_evento.filter(evento__data__lte=data_fim)
    
#     notas = get_notas_data(notas_evento)

#     return notas, nota_field

# class ExportarDadosNotas(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         escola_id = request.GET.get('escola')
#         evento_id = request.GET.get('evento')
#         data_inicio = request.GET.get('data_inicio')
#         data_fim = request.GET.get('data_fim')

#         notas_evento, nota_field = get_notas_evento(
#             escola_id, evento_id, data_inicio, data_fim
#         )

#         filename_raw = f"notas"
#         if escola_id:
#             filename_raw += f"-escola_{escola_id}"
#         if evento_id:
#             filename_raw += f"-evento_{evento_id}"
#         if data_inicio:
#             filename_raw += f"-from_{data_inicio}"
#         if data_fim:
#             filename_raw += f"-to_{data_fim}"

#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename="{filename_raw}.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['Aluno', nota_field])
        
#         for nota in notas_evento:
#             writer.writerow([nota['aluno'], nota['resultado'], nota['escola'], nota['detalhes']])
        
#         return response

# class ListaNotasEventoView(LoginRequiredMixin, TemplateView):
#     template_name = 'notas/lista_notas_evento.html'
#     form_class = ListNotasEventoFilter

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = self.form_class(self.request.GET)
#         context['form'] = form
#         escola_id = self.request.GET.get('escola')
#         evento_id = self.request.GET.get('evento')
#         data_inicio = self.request.GET.get('data_inicio')
#         data_fim = self.request.GET.get('data_fim')

#         notas_evento, nota_field = get_notas_evento(
#             escola_id, evento_id, data_inicio, data_fim
#         )

#         context['notas'] = notas_evento
#         context['nota_field'] = nota_field
#         return context
    
# class ListaNotasAlunoView(LoginRequiredMixin, TemplateView):
#     model = NotaEvento
#     template_name = 'notas/lista_notas_aluno.html'
#     # context_object_name = 'notas_evento'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         aluno_id = self.kwargs.get('aluno_id')
#         aluno = Aluno.objects.get(pk=aluno_id)
#         context['aluno'] = aluno
#         notas_evento = self.model.objects.filter(aluno=aluno)
#         context['notas_evento'] = notas_evento
#         return context

# class AlunosSemNotasListView(LoginRequiredMixin, ListView):
#     model = Aluno
#     template_name = 'notas/lista_alunos_sem_nota.html'
#     context_object_name = 'alunos_sem_notas'

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         evento_id = self.kwargs['evento_id']
#         context['evento'] = Evento.objects.get(pk=evento_id)
#         context['nota_form'] = AvaliarEventoForm()
#         return context

#     def get_queryset(self):
#         evento_id = self.kwargs['evento_id']
#         evento_escola = Evento.objects.get(id=evento_id).escola
#         alunos_com_notas = NotaEvento.objects.filter(evento_id=evento_id).values_list('aluno_id', flat=True)
#         alunos_sem_notas = self.model.objects.filter(escola=evento_escola).exclude(id__in=alunos_com_notas)
#         return alunos_sem_notas

# class CriarNotaView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         aluno_id = self.kwargs['aluno_id']
#         evento_id = self.kwargs['evento_id']
#         form = AvaliarEventoForm(request.POST)
        
#         if form.is_valid():
#             nota = form.cleaned_data['nota']
#             operador = request.user
#             NotaEvento.objects.create(
#                 aluno_id=aluno_id,
#                 evento_id=evento_id, 
#                 nota=nota,
#                 operador=operador
#             )
        
#         redirect_url = reverse('escolas:alunos_sem_notas', kwargs={'evento_id': evento_id})
#         return redirect(redirect_url)
    
# class ListaNotasAlunosEventoView(LoginRequiredMixin, ListView):
#     model = NotaEvento
#     template_name = 'notas/lista_notas_alunos_por_evento.html'
#     context_object_name = 'notas_alunos'

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['evento'] = Evento.objects.get(pk=self.kwargs['evento_id'])
#         return context

#     def get_queryset(self) -> QuerySet[Any]:
#         evento_id = self.kwargs['evento_id']
#         return self.model.objects.filter(evento_id=evento_id)
