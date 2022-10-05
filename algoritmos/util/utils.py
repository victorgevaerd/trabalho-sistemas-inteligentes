from enum import Enum
from algoritmos.util.nodes import Node, AEstrelaSimplesNode, AEstrelaPrecisaNode
from datetime import datetime as dt
from copy import deepcopy, copy


class AcoesEnum(Enum):
    CIMA = 1
    BAIXO = 2
    DIREIRA = 3
    ESQUERDA = 4


def is_estado_final(nodo: Node, estado_objetivo: list):
    return nodo == estado_objetivo


def is_estado_visitado(nodo: Node, nodos_visitados: set):
    return nodo.converte_tupla() in nodos_visitados


def __get_coordenada_estrela(nodo: Node):
    for i in range(len(nodo.estado)):
        for j in range(len(nodo.estado)):
            if nodo.estado[i][j] == '*':
                return (i, j)
    raise ValueError("Estrela não encontrada")


def get_nodos_filhos(nodo: Node, estado_final: list):
    tamanho_estado = len(estado_final) - 1
    nodos_filhos = []
    x, y = __get_coordenada_estrela(nodo)

    if x < tamanho_estado:
        nodos_filhos.append(__get_nodo_derivado_da_acao(
            nodo, AcoesEnum.BAIXO, (x, y), estado_final))

    if x > 0:
        nodos_filhos.append(__get_nodo_derivado_da_acao(
            nodo, AcoesEnum.CIMA, (x, y), estado_final))

    if y < tamanho_estado:
        nodos_filhos.append(__get_nodo_derivado_da_acao(
            nodo, AcoesEnum.DIREIRA, (x, y), estado_final))

    if y > 0:
        nodos_filhos.append(__get_nodo_derivado_da_acao(
            nodo, AcoesEnum.ESQUERDA, (x, y), estado_final))

    return nodos_filhos


def __get_nodo_derivado_da_acao(nodo: Node, acao: AcoesEnum, coordenada_estrela: tuple, estado_final: list = None):
    estado_novo = deepcopy(nodo.estado)
    x, y = coordenada_estrela

    def move_para_cima():
        valor_anterior_cima = copy(estado_novo[x-1][y])
        valor_anterior_estrela = copy(estado_novo[x][y])
        estado_novo[x-1][y] = valor_anterior_estrela
        estado_novo[x][y] = valor_anterior_cima

    def move_para_esquerda():
        valor_anterior_esquerda = copy(estado_novo[x][y-1])
        valor_anterior_estrela = copy(estado_novo[x][y])
        estado_novo[x][y-1] = valor_anterior_estrela
        estado_novo[x][y] = valor_anterior_esquerda

    def move_para_direita():
        valor_anterior_direita = copy(estado_novo[x][y+1])
        valor_anterior_estrela = copy(estado_novo[x][y])
        estado_novo[x][y+1] = valor_anterior_estrela
        estado_novo[x][y] = valor_anterior_direita

    def move_para_baixo():
        valor_anterior_baixo = copy(estado_novo[x+1][y])
        valor_anterior_estrela = copy(estado_novo[x][y])
        estado_novo[x+1][y] = valor_anterior_estrela
        estado_novo[x][y] = valor_anterior_baixo

    switch_case = {
        AcoesEnum.CIMA: move_para_cima,
        AcoesEnum.ESQUERDA: move_para_esquerda,
        AcoesEnum.DIREIRA: move_para_direita,
        AcoesEnum.BAIXO: move_para_baixo
    }

    switch_case[acao]()
    if type(nodo) == Node:
        novo_nodo = Node(estado_novo, nodo.custo + 1, nodo)
    elif type(nodo) == AEstrelaSimplesNode:
        novo_nodo = AEstrelaSimplesNode(
            estado_novo, estado_final, nodo.custo + 1, nodo)
    elif type(nodo) == AEstrelaPrecisaNode:
        novo_nodo = AEstrelaPrecisaNode(
            estado_novo, estado_final, nodo.custo + 1, nodo)

    return novo_nodo


def get_resultado(tempo_inicio: dt, nodos_visitados: list, tamanho_fronteira: int, qtd_nodos_criados: int, nodo_sucesso: Node):
    tempo_fim = dt.now()
    duracao = tempo_fim - tempo_inicio
    qtd_nodos_visitados = len(nodos_visitados)
    caminho = nodo_sucesso.get_caminho()

    return (
        duracao,
        qtd_nodos_visitados,
        caminho,
        tamanho_fronteira,
        qtd_nodos_criados
    )
