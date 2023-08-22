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
        labels = {
            'nome': 'Razão Social'
        }
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
                css_class="justify-content-md-end pr-1"
            )
        )

class EditaEscolaForm(forms.ModelForm):

    class Meta:
        model = Escola
        exclude = ['operador', 'ativo']
        labels = {
            'nome': 'Razão Social'
        }
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
                    Submit('submit', 'Editar Escola', ),
                ),
                css_class="justify-content-md-end pr-1"
            )
        )

class CriaAlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ['operador', 'familia']
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'date'}),
            'info_adicionais': forms.Textarea(attrs={'rows': 2}),
            'estado': forms.Select(choices=ESTADOS_BRASILEIROS)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class="col-md-9"),
                Column('cpf', css_class="col-md-3")
            ),
            Row(
                Column('endereco', css_class="col-md-4"),
                Column('bairro', css_class="col-md-2"),
                Column('complemento')
            ),
            Row(
                Column('cep', css_class="col-md-2"),
                Column('cidade', css_class="col-md-3"),
                Column('estado', css_class="col-md-2"),               
                Column('data_nascimento')
            ),
            Row(
                Column('escola', css_class='col-md-6'),
                Column('periodo', css_class='col-md-3'),
                Column('serie', css_class='col-md-3'),
            ),
            Row(
                Column('estado_civil_pais', css_class='col-md-3'),
                Column('cras', css_class='col-md-3'),
                Column('vulnerabilidades', css_class='col-md-3'),
                Column('remedios', css_class='col-md-3'),
            ),
            Row(
                Column('info_adicionais'),
            ),
            Row(
                ButtonHolder(
                    Submit('submit', 'Cadastrar Aluno', ),
                ),
                css_class="justify-content-md-end pr-1"
            )
        )

class EditaAlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ['operador', 'familia']
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'date'}),
            'info_adicionais': forms.Textarea(attrs={'rows': 2}),
            'estado': forms.Select(choices=ESTADOS_BRASILEIROS)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class="col-md-9"),
                Column('cpf', css_class="col-md-3")
            ),
            Row(
                Column('endereco', css_class="col-md-4"),
                Column('bairro', css_class="col-md-2"),
                Column('complemento')
            ),
            Row(
                Column('cep', css_class="col-md-2"),
                Column('cidade', css_class="col-md-3"),
                Column('estado', css_class="col-md-2"),               
                Column('data_nascimento')
            ),
            Row(
                Column('escola', css_class='col-md-6'),
                Column('periodo', css_class='col-md-3'),
                Column('serie', css_class='col-md-3'),
            ),
            Row(
                Column('estado_civil_pais', css_class='col-md-3'),
                Column('cras', css_class='col-md-3'),
                Column('vulnerabilidades', css_class='col-md-3'),
                Column('remedios', css_class='col-md-3'),
            ),
            Row(
                Column('info_adicionais'),
            ),
            Row(
                ButtonHolder(
                    Submit('submit', 'Editar aluno', ),
                ),
                css_class="justify-content-md-end pr-1"
            )
        )

class ListAlunosFilter(forms.Form):
    escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.filter(ativo=True)], required=False)

class CriaParenteForm(forms.ModelForm):
    class Meta:
        model = Parente
        exclude = ['operador']
    

class ListEventosFilter(forms.Form):
    data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'  # Aplica o estilo horizontal
        self.helper.label_class = 'col-lg-2'  # Classe da label
        self.helper.field_class = 'col-lg-10'  # Classe do campo
        self.helper.layout = Layout(
            Row(
                Column('data_inicio', css_class='col-md-auto mx-1'),
                Column('data_fim', css_class='col-md-auto mx-1'),
                Submit('submit', 'Filtrar', css_class='col-md-auto'),
                css_class='align-items-start'
            )
        )


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
        self.helper.form_class = 'form-horizontal'  # Aplica o estilo horizontal
        self.helper.label_class = 'col-md-2 mr-1'  # Classe da label
        self.helper.field_class = 'col-md-8 ml-1'  # Classe do campo
        self.helper.layout = Layout(
            Row(
                Column('escola', css_class='col-md-3'),
                Column('evento', css_class='col-md-3'),
                Column('data_inicio', css_class='col-md-2'),
                Column('data_fim', css_class='col-md-2'),
                Submit('submit', 'Filtrar',),
                css_class='align-items-start'
            ),
        )

class AvaliarEventoForm(forms.Form):
    nota = forms.DecimalField(label='Nota', max_digits=5, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(AvaliarEventoForm, self).__init__(*args, **kwargs)
        
        # Crie um objeto helper para personalizar o layout
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'  # Aplica o estilo horizontal
        self.helper.label_class = 'col-lg-2'  # Classe da label
        self.helper.field_class = 'col-lg-10'  # Classe do campo

        # Defina o layout dos campos
        self.helper.layout = Layout(
            Row(
                Column('nota', css_class='col-md-8'),
                Submit('submit', 'Avaliar',),
                css_class='align-items-start'
            )
        )

