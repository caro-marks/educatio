from django import forms
from .models import Escola, Evento

class FiltroForm(forms.Form):
    escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.all()], required=False)
    evento = forms.ChoiceField(choices=[('', '--')] + [(evento.id, evento.descricao) for evento in Evento.objects.all()], required=False)
    data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))