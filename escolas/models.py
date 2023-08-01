from django.db import models

# Create your models here.

class Escola(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=40)
    estado = models.CharField(max_length=2)
    complemento = models.CharField(max_length=50, null=True)
    diretor = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
# PARENTESCO = (
#     'pai', 'PAI',
#     'mae', 'MAE',
#     'irm', 'IRMAOS',
#     'avo', 'AVOS',
#     'tio', 'TIOS',
#     'pri', 'PRIMOS',
#     'out', 'OUTROS'
# )

class Aluno(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, unique=True)
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=40)
    estado = models.CharField(max_length=2)
    complemento = models.CharField(max_length=50, null=True)
    data_nascimento = models.DateField()
    # nome_mae = models.CharField(max_length=50)
    # nome_pai = models.CharField(max_length=50)
    # nome_responsavel = models.CharField(max_length=50)
    # grau_de_parentesco = models.CharField(max_length=3, choices=PARENTESCO) // ENUM
    # estado_civil_pais = models.CharField() // ENUM
    # familia = models.CharField() // cadastrar nome, grau de parentesco, idade
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='alunos')
    # periodo = models.CharField() ENUM
    # serie = models.CharField()
    # cras = models.CharField() nulo ou id na rede socio assistencial
    # vulnerabilidades = models.CharField()
    # remedios = models.CharField() 
    # informacoes_adicionais = models.CharField()

    def __str__(self):
        return self.nome


class TipoEvento(models.Model):
    descricao = models.CharField(max_length=50)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    # intervalo_de_avaliacao = models.CharField() // 

    def __str__(self):
        return self.descricao


class Evento(models.Model):
    descricao = models.CharField(max_length=100)
    data = models.DateField(blank=True, null=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='eventos')
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.escola} {self.tipo_evento} {self.descricao}'


class NotaEvento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    # data_entrega = models.DateField()

    def __str__(self):
        return f'{self.evento} - {self.aluno}'

