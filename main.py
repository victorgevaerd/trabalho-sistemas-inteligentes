from util.sem_solucao_exception import SemSolucaoException
from util.arvore_pesquisa import ArvorePesquisa
from util.enums import AlgoritmosPesquisaEnum


def iniciar():
    print()
    print("/***********************\\")
    print("|       Bem Vindo       |")
    print("\\***********************/")
    print()

    rodando_programa = True
    while rodando_programa:
        print("Por favor, informe o estado inicial (use ' * ' para espaço vazio)")
        estado_inicial = get_estado()
        estado_final = get_estado_final_default()
        print()
        print("Gostaria de usar esse estado final?")
        print_estado(estado_final)
        if not pergunta_validade():
            estado_final = get_estado()

        switch_case_algoritmos = {
            1: AlgoritmosPesquisaEnum.CUSTO_UNIFORME,
            2: AlgoritmosPesquisaEnum.A_ESTRELA_SIMPLES,
            3: AlgoritmosPesquisaEnum.A_ESTRELA_PRECISA
        }
        print()
        print("Escolha um algoritmo para realizar a pesquisa")
        for k, v in switch_case_algoritmos.items():
            print(f'{k}: {v.value}')
        terminou_algoritmo = False
        while not terminou_algoritmo:
            try:
                input_algoritmo = int(input("Algoritmo: "))
                print()
                print()
                algoritmo_escolhido = switch_case_algoritmos[input_algoritmo]
                terminou_algoritmo = True
            except ValueError:
                print("Por favor, informe um inteiro")
            except KeyError:
                print("Informe um código válido")

        arvore_pesquisa = ArvorePesquisa(
            estado_inicial, estado_final, algoritmo_escolhido)
        try:
            arvore_pesquisa.pesquisa()
            print()
            print_resultado(arvore_pesquisa.get_resultado())
            rodando_programa = False
        except SemSolucaoException as e:
            print()
            print(e)
            print()
            print("Gostaria de tentar de novo?")
            if not pergunta_validade():
                rodando_programa = False
            print()


def get_estado_final_default():
    return [["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "*"]]


def get_estado():
    terminou_estado = False
    while not terminou_estado:
        estado = []
        for i in range(1, 4):
            terminou_linha = False
            while not terminou_linha:
                linha_str = input(f"{i}ª linha: ").strip()
                linha_list = linha_str.split(" ")
                if len(linha_list) != 3:
                    print("Use espaços em branco como separadores dos inputs")
                else:
                    estado.append(linha_list)
                    terminou_linha = True
        estado_flat = [item for linha in estado for item in linha]
        if "*" not in estado_flat or estado_flat.count("*") > 1:
            print("Não informado espaço vazio ou mais de um espaço vazio informado")
        else:
            print()
            print("Correto?")
            print_estado(estado)
            if pergunta_validade():
                terminou_estado = True
            print()

    return estado


def pergunta_validade():
    aceite_estado_final = input("S/N: ")
    return aceite_estado_final.strip().capitalize() == "S"


def print_estado(estado):
    print(__print_estado(estado))


def __print_estado(estado, espaco_linha=""):
    len_estado = len(estado)
    texto = espaco_linha + "---"*len_estado + "\n"
    for i in range(len_estado):
        texto_linha = espaco_linha + "| "
        for j in range(len_estado):
            texto_linha += f"{estado[i][j]} "
        texto_linha += "|"
        texto += texto_linha + "\n"
    texto += espaco_linha + "---"*len_estado
    return texto


def print_resultado(resultado: tuple):
    duracao, qtd_nodos_visitados, caminho, tamanho_fronteira, qtd_nodos_criados, algoritmo = resultado
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + "\n" +
          algoritmo + "\n" +
          f"Duração:             {duracao}ms" + "\n" +
          f"Nodos criados:       {qtd_nodos_criados}" + "\n" +
          f"Nodos visitados:     {qtd_nodos_visitados}" + "\n" +
          f"Tamanho fronteira:   {tamanho_fronteira}" + "\n" +
          f"Tamanho caminho:     {len(caminho)}" + "\n" +
          "Caminho:" + "\n")
    for index, estado in enumerate(caminho):
        print(f"    Passo {index+1}:\n{__print_estado(estado, '      ')}")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")


if __name__ == '__main__':
    iniciar()
