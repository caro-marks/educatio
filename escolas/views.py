import datetime
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView
from .models import CustomUser, Escola, Aluno, Evento, TipoEvento, NotaEvento
from .forms import UsuarioForm, CriaEscolaForm#, ListNotasEventoForm, ListAlunosForm, ListEventosForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

class UsuariosView(LoginRequiredMixin, View):
    model = CustomUser
    template_name_listagem = 'usuarios/listar_usuarios.html'
    template_name_criacao = 'usuarios/criar_usuario.html'

    def get(self, request):
        usuarios = self.model.objects.all()
        return render(request, self.template_name_listagem, {'usuarios': usuarios})
    
    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            novo_usuario = form.save()

            custom_group = Group.objects.get(name='CustomGroup')
            custom_group.user_set.add(novo_usuario)
        
            return redirect('listar_usuarios')
        
        return render(request, self.template_name_criacao, {'form': form})
    
## HOMEPAGE

class HomepageView(TemplateView):
    template_name = 'homepage.html'


### ESCOLA
class EscolasDetailView(DetailView):
    model = Escola
    template_name = 'escolas/detalhe_escola.html'
    context_object_name = 'escola'

class EscolasListView(ListView):
    model = Escola
    template_name = 'escolas/lista_escolas.html'
    context_object_name = 'escolas'

class EscolaCreateView(CreateView):
    model = Escola
    form_class = CriaEscolaForm
    template_name = 'escolas/cria_escola.html'
    success_url = '/escolas/'


# class DetalheEscolaView(LoginRequiredMixin, DetailView):
#     model = Escola
#     template_name = 'escolas/detalhe_escola.html'
#     context_object_name = 'escola'

# ## Aluno
# class ListaAlunosView(LoginRequiredMixin, ListView):
#     model = Aluno
#     template_name = 'escolas/lista_alunos.html'
#     context_object_name = 'alunos'
#     form_class = ListAlunosForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.form_class(self.request.GET)

#         if escola_id := self.request.GET.get('escola'):
#             context['alunos'] = self.model.objects.filter(escola__id=escola_id)
        
#         alunos_info = []
#         for aluno in context['alunos']:
#             alunos_info.append(
#                 {
#                     'id': aluno.id,
#                     'nome': aluno.nome,
#                     'idade': self.get_idade(aluno.data_nascimento),
#                 })
        
#         context['alunos_info'] = alunos_info
#         return context
    
#     def get_idade(self, data_nascimento):
#         data_atual = datetime.date.today()

#         idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

#         return idade

# class DetalheAlunoView(LoginRequiredMixin, DetailView):
#     model = Aluno
#     template_name = 'escolas/detalhe_aluno.html'
#     context_object_name = 'aluno'

# ## Evento
# class ListaEventosView(LoginRequiredMixin, ListView):
#     model = Evento
#     template_name = 'escolas/lista_eventos.html'
#     context_object_name = 'eventos'
#     form_class = ListEventosForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = self.form_class(self.request.GET)
#         context['form'] = form
        
#         return context

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         form = self.form_class(self.request.GET)
#         if form.is_valid():
            
#             if data_inicio := form.cleaned_data.get('data_inicio'):
#                 queryset = queryset.filter(data__gte=data_inicio)
#             if data_fim := form.cleaned_data.get('data_fim'):
#                 queryset = queryset.filter(data__lte=data_fim)
            
#         return queryset

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
