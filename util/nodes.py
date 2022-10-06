from copy import deepcopy


class Node:
    def __init__(self, estado, custo=0, node_anterior=None):
        self._estado = estado
        self._custo = custo
        self._node_anterior = deepcopy(node_anterior)
        self.__custo_total = custo

    @property
    def estado(self):
        return self._estado

    @property
    def custo(self):
        return self._custo

    @property
    def custo_total(self):
        return self.__custo_total

    def get_caminho(self) -> list:
        if self._node_anterior is not None:
            caminho_anterior: list = self._node_anterior.get_caminho()
            caminho_anterior.append(deepcopy(self._estado))
            return caminho_anterior
        else:
            return [deepcopy(self._estado)]

    def __eq__(self, other):
        estado_a_comparar = other if not isinstance(
            other, Node) else other.estado
        for i in range(len(self._estado)):
            for j in range(len(self._estado)):
                if self._estado[i][j] != estado_a_comparar[i][j]:
                    return False
        return True

    def __str__(self, espaco_linha=""):
        len_estado = len(self._estado)
        texto = espaco_linha + "---"*len_estado + "\n"
        for i in range(len_estado):
            texto_linha = espaco_linha + "| "
            for j in range(len_estado):
                texto_linha += f"{self._estado[i][j]} "
            texto_linha += "|"
            texto += texto_linha + "\n"
        texto += espaco_linha + "---"*len_estado
        return texto

    def converte_tupla(self):
        linhas = []
        for linha in self._estado:
            linhas.append(tuple(linha))
        return tuple(linhas)


class AEstrelaSimplesNode(Node):
    def __init__(self, estado, estado_objetivo, custo=0, node_anterior=None):
        super().__init__(estado, custo, node_anterior)
        self.__valor_heuristica = self.__calcula_heuristica(estado_objetivo)
        self.__custo_total = self._custo + self.__valor_heuristica

    @property
    def custo_total(self):
        return self.__custo_total

    def __calcula_heuristica(self, estado_objetivo):
        """Número de Nodes fora do lugar"""
        heuristica = 9
        for i in range(len(self._estado)):
            for j in range(len(self._estado)):
                if self._estado[i][j] == estado_objetivo[i][j]:
                    heuristica -= 1
        return heuristica


class AEstrelaPrecisaNode(Node):
    def __init__(self, estado, estado_objetivo, custo=0, node_anterior=None):
        super().__init__(estado, custo, node_anterior)
        self.__valor_heuristica = self.__calcula_heuristica(estado_objetivo)
        self.__custo_total = self._custo + self.__valor_heuristica

    @property
    def custo_total(self):
        return self.__custo_total

    def __calcula_heuristica(self, estado_objetivo):
        distancia_manhattan = 0

        for i in range(len(self._estado)):
            for j in range(len(self._estado)):
                x, y = self.__get_coordenada_correta(
                    self._estado[i][j], estado_objetivo)
                distancia_manhattan += abs(i - x) + abs(j - y)

        return distancia_manhattan

    @staticmethod
    def __get_coordenada_correta(pesquisa, estado):
        for i in range(len(estado)):
            for j in range(len(estado)):
                if estado[i][j] == pesquisa:
                    return (i, j)
        raise ValueError("Valor não encontrado")
