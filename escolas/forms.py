from django import forms
from .models import CustomUser, Escola, Evento, Aluno, Parente, TipoEvento, NotaEvento
from django.forms.widgets import DateInput


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
        exclude = ['operador']

class CriaAlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ['operador', 'familia']
        widgets = {
            'data_nascimento': DateInput(attrs={'type': 'date'}),
        }

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

class ListNotasEventoOfAlunoFilter(forms.Form):
    evento = forms.ChoiceField(choices=[('', '--')] + [(evento.id, evento.descricao) for evento in Evento.objects.all()], required=False)
    data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

