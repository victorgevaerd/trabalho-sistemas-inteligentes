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
            algoritmo_escolhido = switch_case_algoritmos[input_algoritmo]["algoritmo"]
            terminou_algoritmo = True
        except ValueError:
            print("Por favor, informe um inteiro")
        except KeyError:
            print("Informe um código válido")
    resultado = algoritmo_escolhido(estado_inicial, estado_final)
    # acoes, nodos_visitados, nodos_expandidos, tamanho = resultado

    print()
    print("Resultados:")
    print(resultado)


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
        if "*" not in [item for linha in estado for item in linha]:
            print("Não informado espaço vazio")
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
    len_estado = len(estado)
    print("---"*len_estado)
    for i in range(len_estado):
        texto_linha = "| "
        for j in range(len_estado):
            texto_linha += f"{estado[i][j]} "
        texto_linha += "|"
        print(texto_linha)
    print("---"*len_estado)


if __name__ == '__main__':
    iniciar()
