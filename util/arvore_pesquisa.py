from copy import deepcopy, copy
from datetime import datetime as dt
from util.sem_solucao_exception import SemSolucaoException
from util.nodes import Node, AEstrelaSimplesNode, AEstrelaPrecisaNode
from util.enums import AcoesEnum, AlgoritmosPesquisaEnum


class ArvorePesquisa:
    def __init__(self, estado_inicial: list, estado_final: list, algoritmo: AlgoritmosPesquisaEnum):
        self.__nodos_visitados = set()
        self.__fronteira = []
        self.__nodo_resultado = None
        self.__nodos_criados = 0
        self.__estado_final = estado_final
        self.__hora_inicio = dt.now()
        self.__tipo_node = algoritmo
        self.__init_primeiro_nodo(estado_inicial)

    def pesquisa(self):
        if self.__verifica_solucionabilidade():
            achou_solucao = False
            while len(self.__fronteira) and not achou_solucao:
                nodo_pesquisado = self.__fronteira.pop(0)
                self.__nodos_visitados.add(nodo_pesquisado.converte_tupla())
                if self.__is_estado_final(nodo_pesquisado):
                    self.__nodo_resultado = nodo_pesquisado
                    achou_solucao = True
                else:
                    nodos_filhos = self.__get_nodos_filhos(nodo_pesquisado)
                    for nodo_filho in nodos_filhos:
                        if not self.__is_estado_visitado(nodo_filho):
                            self.__adiciona_nodo_fronteira(nodo_filho)
            return self.get_resultado()
        else:
            raise SemSolucaoException

    def __verifica_solucionabilidade(self):
        estado_inicial = self.__fronteira[0].estado

        def distancia_manhattan():
            i, j = get_coordenada_vazio(estado_inicial)
            x, y = get_coordenada_vazio(self.__estado_final)
            distancia_manhattan = abs(i - x) + abs(j - y)
            return distancia_manhattan

        def get_coordenada_vazio(estado):
            for i in range(len(estado)):
                for j in range(len(estado)):
                    if estado[i][j] == '*':
                        return (i, j)
            raise ValueError("Valor não encontrado")

        def flatten_estado(estado):
            return [item for linha in estado for item in linha]

        estado_inicial_flat = flatten_estado(estado_inicial)
        estado_objetivo_flat = flatten_estado(self.__estado_final)

        inversoes = 0
        for index, item in enumerate(estado_objetivo_flat[:-1]):
            for item2 in estado_objetivo_flat[index+1:]:
                i = 0
                achou = False
                while i < len(estado_inicial_flat) and not achou:
                    if estado_inicial_flat[i] == item:
                        achou = True
                    else:
                        if estado_inicial_flat[i] == item2:
                            inversoes += 1
                        i += 1
        return inversoes % 2 == distancia_manhattan() % 2

    def __init_primeiro_nodo(self, estado_inicial):
        nodo = self.__cria_nodo(estado_inicial, None)
        self.__adiciona_nodo_fronteira(nodo)

    def __cria_nodo(self, estado_inicial, nodo_anterior):
        custo = 0 if nodo_anterior is None else nodo_anterior.custo + 1
        if self.__tipo_node is AlgoritmosPesquisaEnum.CUSTO_UNIFORME:
            novo_nodo = Node(estado_inicial, custo, nodo_anterior)
        elif self.__tipo_node is AlgoritmosPesquisaEnum.A_ESTRELA_SIMPLES:
            novo_nodo = AEstrelaSimplesNode(
                estado_inicial, self.__estado_final, custo, nodo_anterior)
        elif self.__tipo_node is AlgoritmosPesquisaEnum.A_ESTRELA_PRECISA:
            novo_nodo = AEstrelaPrecisaNode(
                estado_inicial, self.__estado_final, custo, nodo_anterior)
        return novo_nodo

    def __adiciona_nodo_fronteira(self, nodo):
        self.__fronteira.append(nodo)
        self.__fronteira.sort(key=lambda x: x.custo_total)
        self.__nodos_criados += 1

    def __is_estado_final(self, nodo):
        return nodo == self.__estado_final

    def __is_estado_visitado(self, nodo):
        return nodo.converte_tupla() in self.__nodos_visitados

    def __get_nodos_filhos(self, nodo):
        tamanho_estado = len(self.__estado_final) - 1
        nodos_filhos = []
        x, y = self.__get_coordenada_estrela(nodo)

        if x < tamanho_estado:
            nodos_filhos.append(self.__get_nodo_derivado_da_acao(
                nodo, AcoesEnum.BAIXO, (x, y)))

        if x > 0:
            nodos_filhos.append(self.__get_nodo_derivado_da_acao(
                nodo, AcoesEnum.CIMA, (x, y)))

        if y < tamanho_estado:
            nodos_filhos.append(self.__get_nodo_derivado_da_acao(
                nodo, AcoesEnum.DIREIRA, (x, y)))

        if y > 0:
            nodos_filhos.append(self.__get_nodo_derivado_da_acao(
                nodo, AcoesEnum.ESQUERDA, (x, y)))

        return nodos_filhos

    def __get_nodo_derivado_da_acao(self, nodo, acao: AcoesEnum, coordenada_estrela: tuple):
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
        return self.__cria_nodo(estado_novo, nodo)

    @staticmethod
    def __get_coordenada_estrela(nodo):
        for i in range(len(nodo.estado)):
            for j in range(len(nodo.estado)):
                if nodo.estado[i][j] == '*':
                    return (i, j)
        raise ValueError("Estrela não encontrada")

    def get_resultado(self):
        tempo_fim = dt.now()
        duracao = tempo_fim - self.__hora_inicio
        qtd_nodos_visitados = len(self.__nodos_visitados)
        tamanho_fronteira = len(self.__fronteira)
        qtd_nodos_criados = self.__nodos_criados
        caminho = self.__nodo_resultado.get_caminho()
        algoritmo = self.__tipo_node.value

        return (
            duracao,
            qtd_nodos_visitados,
            caminho,
            tamanho_fronteira,
            qtd_nodos_criados,
            algoritmo
        )
