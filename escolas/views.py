import datetime, csv
# from typing import Any, Dict
# from django.db.models.query import QuerySet
# from django.forms.models import BaseModelForm
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView, UpdateView, DeleteView
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
    EditaParenteForm,

    CriaAtividadeForm,
    EditaAtividadeForm,
    
    ListResultadosFilter, 
    AvaliarAtividadeForm,
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
            context['alunos'] = context['alunos'].filter(escola__id=escola_id)
        
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
        context['aluno_id'] = aluno_id
        context['aluno'] = aluno.nome

        return context
    
class ParenteUpdateView(LoginRequiredMixin, UpdateView):
    model = Parente
    form_class = EditaParenteForm
    template_name = 'alunos/edita_parente.html'
    
    def get_success_url(self) -> str:
        aluno_id = self.kwargs.get('aluno_id')
        reverse_url = reverse('escolas:parente', args=[aluno_id, self.object.pk])
        return reverse_url

    def form_valid(self, form):
        form.instance.operador = self.request.user
        return super().form_valid(form)

### Atividade
class ListaAtividadeView(LoginRequiredMixin, ListView):
    model = Atividade
    template_name = 'atividades/lista_atividades.html'
    context_object_name = 'atividades'

    def get_queryset(self):
        queryset = super().get_queryset()
        if escola_id :=  self.request.GET.get('escola'):
            queryset = queryset.filter(escola_id=escola_id)
        return queryset.order_by('descricao', 'escola', 'peso')

class CriaAtividadeView(LoginRequiredMixin, CreateView):
    model = Atividade
    template_name = 'atividades/cria_atividade.html'
    form_class = CriaAtividadeForm
    
    def get_success_url(self):
        atividade_id = self.object.pk
        escola = self.model.objects.get(pk=atividade_id).escola
        url = reverse('escolas:atividades')
        success_url = f'{url}?escola={escola.id}'
        return success_url

    def get_initial(self):
        initial = super().get_initial()
        if escola_param := self.request.GET.get('escola', None):
            initial['escola'] = escola_param
        return initial

class DetalheAtividadeView(LoginRequiredMixin, DetailView):
    model = Atividade
    template_name = 'atividades/detalhe_atividade.html'
    context_object_name = 'atividade'

class EditaAtividadeView(LoginRequiredMixin, UpdateView):
    model = Atividade
    form_class = EditaAtividadeForm
    template_name = 'atividades/edita_atividade.html'
    
    def get_success_url(self) -> str:
        return reverse('escolas:atividade', args=[self.object.pk])

class RemoveAtividadeView(LoginRequiredMixin, View):
    model = Atividade
    
    def get(self, request, pk):
        objeto = get_object_or_404(self.model, pk=pk)
        objeto.ativo = False
        objeto.delete()
        return redirect(reverse_lazy('escolas:atividades'))

# ### NotaEvento

def get_notas(resultados):
    notas = []
    alunos = [resultado.aluno for resultado in resultados]
    for aluno in list(set(alunos)):
        resultados_aluno = resultados.filter(aluno=aluno)
        total_pesos = 0
        soma_produtos = 0

        for resultado_aluno in resultados_aluno:
            peso_atividade = resultado_aluno.atividade.peso
            nota_aluno = resultado_aluno.nota

            total_pesos += peso_atividade
            soma_produtos += nota_aluno * peso_atividade

        if total_pesos != 0:
            media_ponderada = soma_produtos / total_pesos
        else:
            media_ponderada = 0
        
        notas.append(
            {
                'aluno_id': aluno.id,
                'aluno': aluno.nome,
                'resultado': round(media_ponderada, 2),
                'escola': aluno.escola.nome,
                'detalhes': [
                    {
                        'nota_id': nota_evento.id,
                        'nota': nota_evento.nota

                    } for nota_evento in resultados_aluno
                ]
            }
        )

    return sorted(
        notas,
        key=lambda media: (-media['resultado'], media['aluno']),
        # reverse=(True, False)
    )


def get_resultados(escola_id, atividade_id, data_inicio, data_fim):
    titulo = 'Media' if atividade_id else 'Resultado'
    
    if escola_id:
        resultados = Resultado.objects.filter(atividade__escola_id=escola_id)
        if atividade_id:
            resultados = resultados.filter(atividade_id=atividade_id)
    elif atividade_id:
        resultados = Resultado.objects.filter(atividade_id=atividade_id)
    else:
        resultados = Resultado.objects.all()

    if data_inicio:
        # resultados = resultados.filter(data_entrega__gte=data_inicio)
        resultados = resultados.filter(atividade__data__gte=data_inicio)
    if data_fim:
        # resultados = resultados.filter(data_entrega__lte=data_fim)
        resultados = resultados.filter(atividade__data__lte=data_fim)
    
    notas = get_notas(resultados)

    return notas, titulo

# class ExportarDadosNotas(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         escola_id = request.GET.get('escola')
#         evento_id = request.GET.get('evento')
#         data_inicio = request.GET.get('data_inicio')
#         data_fim = request.GET.get('data_fim')

#         notas_evento, nota_field = get_resultados(
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

class ListaResultadosView(LoginRequiredMixin, TemplateView):
    template_name = 'resultados/lista_resultados.html'
    form_class = ListResultadosFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(self.request.GET)
        context['form'] = form
        escola_id = self.request.GET.get('escola')
        atividade_id = self.request.GET.get('atividade')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        resultados, titulo = get_resultados(
            escola_id, atividade_id, data_inicio, data_fim
        )

        context['resultados'] = resultados
        context['titulo'] = titulo
        return context
    
class ListaResultadosAlunoView(LoginRequiredMixin, TemplateView):
    model = Resultado
    template_name = 'resultados/lista_resultados_aluno.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno_id = self.kwargs.get('aluno_id')
        aluno = Aluno.objects.get(pk=aluno_id)
        context['aluno'] = aluno
        resultados = self.model.objects.filter(aluno=aluno)
        context['resultados'] = resultados
        return context

class AlunosSemNotasListView(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = 'resultados/lista_alunos_sem_nota.html'
    context_object_name = 'alunos_sem_notas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atividade_id = self.kwargs['atividade_id']
        context['atividade'] = Atividade.objects.get(pk=atividade_id)
        context['nota_form'] = AvaliarAtividadeForm()
        return context

    def get_queryset(self):
        atividade_id = self.kwargs['atividade_id']
        escola = Atividade.objects.get(id=atividade_id).escola
        alunos_com_notas = Resultado.objects.filter(atividade_id=atividade_id).values_list('aluno_id', flat=True)
        alunos_sem_notas = self.model.objects.filter(escola=escola, ativo=True).exclude(id__in=alunos_com_notas)
        return alunos_sem_notas

class CriarNotaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        aluno_id = self.kwargs['aluno_id']
        atividade_id = self.kwargs['atividade_id']
        form = AvaliarAtividadeForm(request.POST)
        
        if form.is_valid():
            nota = form.cleaned_data['nota']
            operador = request.user
            Resultado.objects.create(
                aluno_id=aluno_id,
                atividade_id=atividade_id, 
                nota=nota,
                operador=operador
            )
        
        redirect_url = reverse('escolas:alunos_sem_notas', kwargs={'atividade_id': atividade_id})
        return redirect(redirect_url)
    
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
