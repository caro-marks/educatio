from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import ParentescoChoices, EstadosCivis, PeriodoEscola, SerieEscolar
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from datetime import date

# Create your models here.

class CustomUser(AbstractUser):
    ativo = models.BooleanField(default=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Escola(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=40)
    estado = models.CharField(max_length=2)
    complemento = models.CharField(max_length=50, null=True, blank=True)
    diretor = models.CharField(max_length=50)
    telefone_principal = models.CharField(
        max_length=15, blank=True, null=True,
        validators=[
            MinLengthValidator(13, 'Número de telefone deve ter no mínimo 10 dígitos'),
        ]
    )
    telefone_secundario = models.CharField(
        max_length=15, blank=True, null=True,
        validators=[
            MinLengthValidator(13, 'Número de telefone deve ter no mínimo 10 dígitos'),
        ]
    )
    email = models.EmailField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    operador = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    
    def get_endereco_junto_display(self):
        return f'{self.endereco}, {self.bairro} - {self.cidade}/{self.estado}'

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=15, unique=True, blank=True, null=True)
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=9, blank=True)
    cidade = models.CharField(max_length=40)
    estado = models.CharField(max_length=2)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField()
    estado_civil_pais = models.CharField(max_length=3, choices=EstadosCivis.choices(), blank=True, null=True)
    cras = models.CharField(blank=True, null=True, max_length=30)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=3, choices=PeriodoEscola.choices(), blank=True, null=True)
    serie = models.CharField(max_length=3, choices=SerieEscolar.choices(), blank=True, null=True)
    vulnerabilidades = models.CharField(max_length=150, blank=True)
    remedios = models.CharField(max_length=100, blank=True)
    alergias = models.CharField(max_length=100, blank=True)
    info_adicionais = models.CharField(max_length=200, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    operador = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)

    def get_student_info_display(self):
        serie = dict(SerieEscolar.choices()).get(self.serie, 'Desconhecida')
        periodo = dict(PeriodoEscola.choices()).get(self.periodo, 'Desconhecido')
        return f"{serie} - {periodo}"
    
    def get_endereco_junto_display(self):
        return f'{self.endereco}, {self.bairro} - {self.cidade}/{self.estado}'
    
    def get_estado_civil_pais_display(self):
        return f'{dict(EstadosCivis.choices()).get(self.estado_civil_pais)}'

    def __str__(self):
        return self.nome
    

class Parente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, unique=True, blank=True, null=True)
    idade = models.PositiveSmallIntegerField(blank=True, null=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    info_adicionais = models.CharField(max_length=300, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    operador = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)

    def get_idade_atual_display(self):
        return f'{self.idade + (date.today().year - self.criado_em.year)}'

    def __str__(self):
        return self.nome


class Parentesco(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='parentescos')
    parente = models.ForeignKey(Parente, on_delete=models.CASCADE, related_name='parentescos')
    grau_parentesco = models.CharField(max_length=3, choices=ParentescoChoices.choices())
    principal_responsavel = models.BooleanField(default=False)

    def get_grau_parentesco_display(self):
        return f'{dict(ParentescoChoices.choices()).get(self.grau_parentesco)} de {self.aluno}'

    def __str__(self) -> str:
        return f'{self.parente}, {self.get_grau_parentesco_display()}'


class Atividade(models.Model):
    descricao = models.CharField(max_length=100)
    peso = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, "Peso deve ser no minimo 1"),
        MaxValueValidator(100, "Peso deve ser no maximo 100")
    ])
    data = models.DateField()
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.escola} - {self.descricao}'


class Resultado(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, null=True)
    nota = models.DecimalField(max_digits=4, decimal_places=2, validators=[
        MinValueValidator(0, "Nota mínima é 0"),
        MaxValueValidator(10, "Nota máxima é 10")
    ])
    observacoes = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    operador = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.atividade} - {self.aluno}'
