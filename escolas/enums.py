from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(enum.name, enum.value) for enum in cls]

class Parentesco(BaseEnum):    
    PAI = 'Pai'
    MAE = 'Mãe'
    IRM = 'Irmãos'
    AVO = 'Avós'
    TIO = 'Tios'
    PRI = 'Primos'
    OUT = 'Outros'

class EstadosCivis(BaseEnum):
    SOL = 'Solteiro(a)'
    CAS = 'Casado(a)'
    DIV = 'Divorciado(a)'
    VIU = 'Viúvo(a)'
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

