from enum import Enum, auto


class AcoesEnum(Enum):
    CIMA = auto()
    BAIXO = auto()
    DIREIRA = auto()
    ESQUERDA = auto()


class AlgoritmosPesquisaEnum(Enum):
    CUSTO_UNIFORME = "Custo Uniforme (sem heurística)"
    A_ESTRELA_SIMPLES = "A* com uma heurística simples"
    A_ESTRELA_PRECISA = "A* com a heurística (Manhattan Distance)"
