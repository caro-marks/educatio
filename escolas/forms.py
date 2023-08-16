from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .enums import ESTADOS_BRASILEIROS
from .models import CustomUser, Escola, Evento, Aluno, Parente, TipoEvento
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user


class CriaEscolaForm(forms.ModelForm):

    class Meta:
        model = Escola
        exclude = ['operador', 'ativo']
        widgets = {
            'complemento': forms.Textarea(attrs={'rows': 2}),
            'estado': forms.Select(choices=ESTADOS_BRASILEIROS)
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class="col-md-8"),
                Column('cnpj', css_class="col-md-4")
            ),
            Row(
                Column('endereco', css_class="col-md-7"),
                Column('bairro', css_class="col-md-5")
            ),
            Row(
                Column('cep', css_class="col-md-2"),
                Column('cidade', css_class="col-md-3"),
                Column('estado', css_class="col-md-2"),               
                Column('diretor')
            ),
            Row(
                Column('complemento')
            ),
            Row(
                ButtonHolder(
                    Submit('submit', 'Cadastrar Escola', ),
                ),
                css_class="justify-content-md-end"
            )
        )

class CriaAlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ['operador', 'familia']
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'date'}),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()

class ListAlunosFilter(forms.Form):
    escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.filter(ativo=True)], required=False)

class CriaParenteForm(forms.ModelForm):
    class Meta:
        model = Parente
        exclude = ['operador']
    

class ListEventosFilter(forms.Form):
    data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class CriaEventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'data': DateInput(attrs={'type': 'date'}),
        }

class CriaTipoEvento(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = '__all__'


class ListNotasEventoFilter(forms.Form):
    escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.filter(ativo=True)], required=False)
    evento = forms.ChoiceField(choices=[('', '--')] + [(evento.id, evento.descricao) for evento in Evento.objects.all()], required=False)
    data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('escola', css_class='col-md-6'),
                Column('evento', css_class='col-md-6'),
            ),
            Row(
                Column('data_inicio', css_class='col-md-6'),
                Column('data_fim', css_class='col-md-6'),
                css_class='mt-3'
            ),
            ButtonHolder(
                Submit('submit', 'Filtrar',)
            )
        )

class AvaliarEventoForm(forms.Form):
    nota = forms.DecimalField(label='Nota', max_digits=5, decimal_places=2)

