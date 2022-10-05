from algoritmos.custo_uniforme import pesquisar as pesquisar_custo_uniforme
from algoritmos.a_estrela_simples import pesquisar as pesquisar_a_estrela_simples
from algoritmos.a_estrela_precisa import pesquisar as pesquisar_a_estrela_precisa


def iniciar():
    print()
    print("/***********************\\")
    print("|     Bem Vindo         |")
    print("\\***********************/")
    print()
    print("Por favor, informe o estado inicial (use ' * ' para espaço vazio)")

    estado_inicial = get_estado()
    estado_final = get_estado_final_default()
    print()
    print("Gostaria de usar esse estado final?")
    print_estado(estado_final)
    if not pergunta_validade():
        estado_final = get_estado()

    switch_case_algoritmos = {
        1: {"nome": "Custo Uniforme (sem heurística)", "algoritmo": pesquisar_custo_uniforme},
        2: {"nome": "A* com uma heurística simples", "algoritmo": pesquisar_a_estrela_simples},
        3: {"nome": "A* com a heurística mais precisa que conseguirem", "algoritmo": pesquisar_a_estrela_precisa}
    }
    print()
    print("Escolha um algoritmo para realizar a pesquisa")
    for k, v in switch_case_algoritmos.items():
        print(f'{k}: {v["nome"]}')
    terminou_algoritmo = False
    while not terminou_algoritmo:
        try:
            input_algoritmo = int(input("Algoritmo: "))
            print()
            print()
            algoritmo_escolhido = switch_case_algoritmos[input_algoritmo]["algoritmo"]
            terminou_algoritmo = True
        except ValueError:
            print("Por favor, informe um inteiro")
        except KeyError:
            print("Informe um código válido")

        resultado = algoritmo_escolhido(estado_inicial, estado_final)
    # acoes, nodos_visitados, nodos_expandidos, tamanho = resultado

    print()
    print_resultado(resultado)


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
    duracao, qtd_nodos_visitados, caminho, tamanho_fronteira, qtd_nodos_criados = resultado
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + "\n" +
          f"Duração:                 {duracao}ms" + "\n" +
          f"Nodos visitados:         {qtd_nodos_visitados}" + "\n" +
          f"Tamanho caminho:         {len(caminho)}" + "\n" +
          f"Tamanho max. fronteira:  {tamanho_fronteira}" + "\n" +
          f"Nodos criados:           {qtd_nodos_criados}" + "\n" +
          "Caminho:" + "\n")
    for index, estado in enumerate(caminho):
        print(f"    Passo {index+1}:\n{__print_estado(estado, '      ')}")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")


if __name__ == '__main__':
    iniciar()
