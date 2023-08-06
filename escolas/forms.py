from django import forms
from .models import CustomUser, Escola, Evento, Aluno, Parente
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column


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

    
    # def __init__(self, *args, **kwargs):
    #     self.fields['is_superuser'].widget = forms.HiddenInput()
    #     self.fields['is_staff'].widget = forms.HiddenInput()

class CriaEscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        exclude = ['operador']

class CriaAlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ['operador', 'familia']

class ListAlunosFilter(forms.Form):
    escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.all()], required=False)

class CriaParenteForm(forms.ModelForm):
    class Meta:
        model = Parente
        exclude = ['operador']
    

# class ListEventosForm(forms.Form):
#     data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


# class ListNotasEventoForm(forms.Form):
    # escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.all()], required=False)
    # evento = forms.ChoiceField(choices=[('', '--')] + [(evento.id, evento.descricao) for evento in Evento.objects.all()], required=False)
    # data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    # data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
