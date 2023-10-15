from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(enum.name, enum.value) for enum in cls]

class ParentescoChoices(BaseEnum):    
    PAI = 'Pai'
    MAE = 'Mãe'
    IRM = 'Irmãos'
    AVO = 'Avós'
    TIO = 'Tios'
    PRI = 'Primos'
    OUT = 'Outros'

class EstadosCivis(BaseEnum):
    SOL = 'Solteiros'
    CAS = 'Casados'
    DIV = 'Divorciados'
    VIU = 'Viúvos'
    UNI = 'União Estável'
    OUT = 'Outro'
    
class PeriodoEscola(BaseEnum):
    MAT = 'Matutino'
    VES = 'Vespertino'
    NOT = 'Noturno'
    
class SerieEscolar(BaseEnum):
    PRI = '1º ano'
    SEG = '2º ano'
    TER = '3º ano'
    QUA = '4º ano'
    QUI = '5º ano'
    SEX = '6º ano'
    SET = '7º ano'
    OIT = '8º ano'
    NON = '9º ano'
    PEM = '1º E. M.'
    SEM = '2º E. M.'
    TEM = '3º E. M.'

ESTADOS_BRASILEIROS = [
    ('', '--'),
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]
