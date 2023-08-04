from django import forms
from .models import CustomUser, Escola, Evento
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
    
    def __init__(self, *args, **kwargs):
        self.fields['is_superuser'].widget = forms.HiddenInput()
        self.fields['is_staff'].widget = forms.HiddenInput()

class CriaEscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = '__all__' 


# class ListAlunosForm(forms.Form):
#     escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.all()], required=False)


# class ListEventosForm(forms.Form):
#     data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

#     # def __init__(self, *args, **kwargs):
#     #     super(ListEventosForm, self).__init__(*args, **kwargs)
#     #     self.helper = FormHelper()
#     #     # self.helper.form_method = 'get'
#     #     # self.helper.form_class = 'form-horizontal'
#     #     # self.helper.label_class = 'col-lg-2'
#     #     # self.helper.field_class = 'col-lg-8'
#     #     self.helper.layout = Layout(
#     #         Row(
#     #             Column(
#     #                 'data_inicio', css_class='col-sm-6'
#     #             ),
#     #             Column(
#     #                 'data_fim',
#     #                 css_class='col-sm-6'
#     #             )
#     #         ),
#     #         Submit('submit', 'Filtrar', css_class='btn-primary')
#     #     )


# class ListNotasEventoForm(forms.Form):
    # escola = forms.ChoiceField(choices=[('', '--')] + [(escola.id, escola.nome) for escola in Escola.objects.all()], required=False)
    # evento = forms.ChoiceField(choices=[('', '--')] + [(evento.id, evento.descricao) for evento in Evento.objects.all()], required=False)
    # data_inicio = forms.DateField(label='De', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    # data_fim = forms.DateField(label='Até', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
