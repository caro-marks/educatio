from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.exceptions import ValidationError
# from django.core.files.base import File
# from django.db.models.base import Model
# from django.forms.utils import ErrorList
from .enums import ESTADOS_BRASILEIROS
from .models import CustomUser, Escola, Aluno, Parente, Atividade, Resultado
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

class TelefoneWidget(forms.TextInput):  
    def format_value(self, value):
        if value:
            return f'({value[:2]}) {value[2:6]}-{value[6:]}'
        return value


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
    telefone_principal = forms.CharField(required=True)

    class Meta:
        model = Escola
        exclude = ['operador', 'ativo']
        labels = {
            'nome': 'Razão Social',
            'telefone_principal': 'Telefone',
            'telefone_secundario': 'WhatsApp'
        }
        widgets = {
            'complemento': forms.Textarea(attrs={'rows': 2}),
            'estado': forms.Select(choices=ESTADOS_BRASILEIROS),
            'telefone_principal': TelefoneWidget(),
            'telefone_secundario': TelefoneWidget()
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
                Column('telefone_principal', css_class="col-md-3"),
                Column('telefone_secundario', css_class="col-md-3"),
                Column('email', css_class="col-md-3"),              
                Column('diretor')
            ),
            Row(
                Column('endereco', css_class="col-md-4"),
                Column('bairro', css_class="col-md-2"),
                Column('cep', css_class="col-md-2"),
                Column('cidade', css_class="col-md-2"),
                Column('estado', css_class="col"), 
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

    def clean(self):
        super(CriaEscolaForm, self).clean()

        if cnpj := self.cleaned_data.get('cnpj'):
            if len(cnpj) != 18:
                raise ValidationError("O campo 'CNPJ' deve ter 14 dígitos")
        
        if cep := self.cleaned_data.get('cep'):
            if len(cep) != 9:
                raise ValidationError("O campo 'CEP' deve ter 9 dígitos")


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
    escola = forms.ModelChoiceField(
        queryset=Escola.objects.filter(ativo=True),
        empty_label="--",
        required=False
    )
    class Meta:
        model = Aluno
        exclude = ['operador', 'familia']
        labels = {
            'estado_civil_pais': 'Estado civil dos pais',
            'info_adicionais': 'Informações adicionais',
            'data_nascimento': 'Data Nasc.'
        }
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'date'}),
            'vulnerabilidades': forms.Textarea(attrs={'rows': 2}),
            'info_adicionais': forms.Textarea(attrs={'rows': 3}),
            'estado': forms.Select(choices=ESTADOS_BRASILEIROS)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class="col-md-8"),
                Column('cpf', css_class="col-md-2"),    
                Column('data_nascimento', css_class='col-md-2'),
            ),
            Row(
                Column('endereco', css_class="col-md-4"),
                Column('bairro', css_class="col-md-2"),
                Column('cidade', css_class="col-md-2"),
                Column('estado', css_class="col-md-2"), 
                Column('cep', css_class="col-md-2"),  
            ),
            Row(        
                Column('complemento'),
            ),
            Row(
                Column('estado_civil_pais', css_class='col-md-2'),
                Column('cras', css_class='col-md-2'),
                Column('alergias', css_class='col-md-4'),
                Column('remedios', css_class='col-md-4'),
            ),
            Row(
                Column('escola', css_class='col-md-6'),
                Column('periodo', css_class='col-md-3'),
                Column('serie', css_class='col-md-3'),
            ),
            Row(
                Column('vulnerabilidades'),
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
    data_nascimento = forms.DateField(required=False)
    class Meta:
        model = Aluno
        exclude = ['operador', 'familia']
        labels = {
            'estado_civil_pais': 'Estado civil dos pais',
            'info_adicionais': 'Informações adicionais'
        }
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'date'}),
            'vulnerabilidades': forms.Textarea(attrs={'rows': 2}),
            'info_adicionais': forms.Textarea(attrs={'rows': 2}),
            'estado': forms.Select(choices=ESTADOS_BRASILEIROS)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class="col-md-8"),
                Column('cpf', css_class="col-md-2"),    
                Column('data_nascimento', css_class='col-md-2'),
            ),
            Row(
                Column('endereco', css_class="col-md-4"),
                Column('bairro', css_class="col-md-2"),
                Column('cidade', css_class="col-md-2"),
                Column('estado', css_class="col-md-2"), 
                Column('cep', css_class="col-md-2"),  
            ),
            Row(        
                Column('complemento'),
            ),
            Row(
                Column('estado_civil_pais', css_class='col-md-2'),
                Column('cras', css_class='col-md-2'),
                Column('alergias', css_class='col-md-4'),
                Column('remedios', css_class='col-md-4'),
            ),
            Row(
                Column('escola', css_class='col-md-6'),
                Column('periodo', css_class='col-md-3'),
                Column('serie', css_class='col-md-3'),
            ),
            Row(
                Column('vulnerabilidades'),
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
        labels = {
            'principal_responsavel': 'Principal Responsável'
        }


class EditaParenteForm(forms.ModelForm):
    class Meta:
        model = Parente
        exclude = ['operador']
        labels = {
            'principal_responsavel': 'Principal Responsável'
        }


class CriaAtividadeForm(forms.ModelForm):
    escola = forms.ModelChoiceField(
        queryset=Escola.objects.filter(ativo=True),
        empty_label="--",
        required=False
    )
    
    class Meta:
        model = Atividade
        fields = '__all__'
        widgets = {
            'data': DateInput(attrs={'type': 'date'}),
        }


class EditaAtividadeForm(forms.ModelForm):
    escola = forms.ModelChoiceField(
        queryset=Escola.objects.filter(ativo=True),
        empty_label="--",
        required=False
    )
    data = forms.DateField(required=False)

    class Meta:
        model = Atividade
        fields = '__all__'
        widgets = {
            'data': DateInput(attrs={'type': 'date'}),
        }

class ListResultadosFilter(forms.Form):
    escola = forms.ChoiceField(
        choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.filter(ativo=True)],
        required=False
    )
    # escola = forms.ModelChoiceField(
    #     queryset=Escola.objects.filter(ativo=True),
    #     empty_label="--",
    #     required=False
    # )
    atividade = forms.ChoiceField(
        choices=[('', '--')] + [(atividade.id, atividade.descricao) for atividade in Atividade.objects.all()],
        required=False
    )
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
                Column('atividade', css_class='col-md-3'),
                Column('data_inicio', css_class='col-md-2'),
                Column('data_fim', css_class='col-md-2'),
                Submit('submit', 'Filtrar',),
                css_class='justify-content-between align-items-start'
            ),
        )


class AvaliarAtividadeForm(forms.Form):
    nota = forms.DecimalField(label='Nota', max_digits=4, decimal_places=2, validators=[
        MinValueValidator(0, "Nota mínima é 0"),
        MaxValueValidator(10, "Nota máxima é 10")
    ])

    def __init__(self, *args, **kwargs):
        super(AvaliarAtividadeForm, self).__init__(*args, **kwargs)
        
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

