from django.views.generic import ListView, DetailView, TemplateView
from .models import Escola, Aluno, Evento, TipoEvento, NotaEvento

# Create your views here.

## HOMEPAGE

class HomepageView(TemplateView):
    template_name = 'escolas/homepage.html'

## Escola
class ListaEscolasView(ListView):
    model = Escola
    template_name = 'escolas/lista_escolas.html'
    context_object_name = 'escolas'

class DetalheEscolaView(DetailView):
    model = Escola
    template_name = 'escolas/detalhe_escola.html'
    context_object_name = 'escola'

## Aluno
class ListaAlunosView(ListView):
    model = Aluno
    template_name = 'escolas/lista_alunos.html'
    context_object_name = 'alunos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['escolas'] = Escola.objects.all()

        if escola_id := self.request.GET.get('escola'):
            context['nome_escola'] = Escola.objects.get(id=escola_id).nome
            context['alunos'] = Aluno.objects.filter(escola__id=escola_id)

        return context

class DetalheAlunoView(DetailView):
    model = Aluno
    template_name = 'escolas/detalhe_aluno.html'
    context_object_name = 'aluno'

## Evento
class ListaEventosView(ListView):
    model = Evento
    template_name = 'escolas/lista_eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        queryset = super().get_queryset()
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        print(f'data_inicio: {data_inicio}')
        print(f'data_fim: {data_fim}')

        if data_inicio and data_fim:
            # Realize a filtragem dos eventos com base nas datas selecionadas
            queryset = queryset.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            # Filtrar por eventos com data maior ou igual à data_inicio
            queryset = queryset.filter(data__gte=data_inicio)
        elif data_fim:
            # Filtrar por eventos com data menor ou igual à data_fim
            queryset = queryset.filter(data__lte=data_fim)

        return queryset

class DetalheEventoView(DetailView):
    model = Evento
    template_name = 'escolas/detalhe_evento.html'
    context_object_name = 'evento'

# ## TipoEvento
# class ListaTiposEventoView(ListView):
#     model = TipoEvento
#     template_name = 'escolas/lista_tipos_evento.html'
#     context_object_name = 'tipos_evento'

# class DetalheTipoEventoView(DetailView):
#     model = TipoEvento
#     template_name = 'escolas/detalhe_tipo_evento.html'
#     context_object_name = 'tipo_evento'
