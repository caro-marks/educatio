from django import forms
from django.core.exceptions import ValidationError
from .enums import ESTADOS_BRASILEIROS, ParentescoChoices
from .models import CustomUser, Escola, Aluno, Parente, Atividade, Resultado
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit
from django.core.validators import MinValueValidator, MaxValueValidator

class AtividadeSelectFilter(forms.Select):
    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            atividade = Atividade.objects.get(pk=int(str(value)))
            option["attrs"]["data-escola"] = atividade.escola.id
        return option


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'cargo', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EditaUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'cargo', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
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
            'nome': 'Razão Social',
            'telefone_principal': 'Telefone',
            'telefone_secundario': 'WhatsApp'
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
                Column('telefone_principal', css_class="col-md-3"),
                Column('telefone_secundario', css_class="col-md-3"),
                Column('email', css_class="col-md-3"),              
                Column('diretor')
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
        exclude = ['operador', 'familia', 'ativo']
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


class AdicionaParenteForm(forms.Form):
    parente = forms.ModelChoiceField(
        queryset=Parente.objects.all(),
        label="Selecione um parente existente",
        required=False
    )
    nome = forms.CharField(
        max_length=100,
        required=False,
        label='Nome*',
        widget=forms.TextInput(attrs={'class': 'optionalRequired'})
    )
    cpf = forms.CharField(max_length=15, required=False)
    grau_parentesco = forms.ChoiceField(
        choices=[('', 'Escolha um grau de parentesco')] + ParentescoChoices.choices(),        
        widget=forms.Select(attrs={'class': 'optionalRequired'}),
        label='Grau de Parentesco*',
        required=False
    )
    idade = forms.IntegerField(required=False)
    principal_responsavel = forms.BooleanField(initial=False, required=False)
    telefone = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(required=False)
    info_adicionais = forms.CharField(max_length=200, required=False)


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


class EditaNotaForm(forms.ModelForm):

    class Meta:
        model = Resultado
        fields = ['nota', 'observacoes']



class ListResultadosFilter(forms.Form):
    escola = forms.ModelChoiceField(
        queryset=Escola.objects.filter(ativo=True),
        empty_label="--",
        required=False,
        widget=forms.Select(attrs={'id': 'escola-select'})
    )
    atividade = forms.ModelChoiceField(
        queryset=Atividade.objects.all(),
        empty_label="--",
        required=False,
        widget=AtividadeSelectFilter(attrs={'id': 'atividade-select'})
    )
    data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('escola', css_class='col-md-4'),
                Column('atividade', css_class='col-md-4'),
                Column('data_inicio', css_class='col-md-2'),
                Column('data_fim', css_class='col-md-2'),
                Submit('submit', 'Filtrar',),
                css_class='justify-content-between align-items-start'
            ),
        )


class AvaliarAtividadeForm(forms.Form):
    nota = forms.DecimalField(label='Nota', help_text='Nota deve ser entre 0 e 10',max_digits=4, decimal_places=2, validators=[
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


class SimpleDataFilter(forms.Form):
    data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal my-0 py-0'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Row(
                Column('data_inicio', css_class='col-md-5'),
                Column('data_fim', css_class='col-md-5'),
                Submit('submit', 'Filtrar',),
                css_class='align-items-start'
            ),
        )
