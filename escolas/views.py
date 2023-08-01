from django.views.generic import ListView, DetailView, TemplateView
from .models import Escola, Aluno, Evento, TipoEvento, NotaEvento
from .forms import FiltroForm

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
        # if not data_inicio or not data_fim:
        #     queryset = queryset.none()
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

class ListaNotasEventoView(ListView):
    model = NotaEvento
    template_name = 'escolas/lista_notas_evento.html'
    context_object_name = 'notas_evento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FiltroForm(self.request.GET)
        context['form'] = form
        escola_id = self.request.GET.get('escola')
        evento_id = self.request.GET.get('evento')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if escola_id:
            notas_evento = NotaEvento.objects.filter(evento__escola_id=escola_id)
            if evento_id:
                notas_evento = notas_evento.filter(evento_id=evento_id)
        else:
            notas_evento = NotaEvento.objects.all()
        
        if data_inicio:
            notas_evento = notas_evento.filter(evento__data__gte=data_inicio)
        if data_fim:
            notas_evento = notas_evento.filter(evento__data__gte=data_fim)

        medias = self.get_medias(notas_evento=notas_evento)

        context['medias'] = medias
        return context
    
    def get_medias(self, notas_evento):
        medias = []
        alunos = [nota_evento.aluno for nota_evento in notas_evento]
        print(f'alunos: {alunos}')
        for aluno in list(set(alunos)):
            print(f'aluno: {aluno}')
            notas_eventos = notas_evento.filter(aluno=aluno)
            print(f'notas_eventos: {notas_eventos}')
            total_pesos = 0
            soma_produtos = 0

            for nota_evento in notas_eventos:
                tipo_evento = nota_evento.evento.tipo_evento
                peso_evento = tipo_evento.peso
                nota_aluno = nota_evento.nota

                total_pesos += peso_evento
                soma_produtos += nota_aluno * peso_evento

            if total_pesos != 0:
                media_ponderada = soma_produtos / total_pesos
            else:
                media_ponderada = 0
            
            medias.append(
                {
                    'aluno': aluno.nome,
                    'media': round(media_ponderada, 2)
                }
            )
        return medias

class DetalheNotaEventoView(DetailView):
    model = NotaEvento
    template_name = 'escolas/detalhe_nota_evento.html'
    context_object_name = 'nota_evento'
