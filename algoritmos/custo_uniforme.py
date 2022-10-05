from datetime import datetime as dt
from algoritmos.util.nodes import Node
from algoritmos.util.utils import *


def pesquisar(estado_inicial, estado_final):
    visitedPuzzleNodes = set()
    borderPuzzleNodes = []
    START_TIME = dt.now()
    result_puzzle_node = None
    MAX_BORDER_LENGTH = 0
    CREATED_NODES = 1

    # Instance the first node
    initialNode = Node(estado_inicial, 0, None)

    # Check if is finished
    if is_estado_final(initialNode, estado_final):
        result_puzzle_node = initialNode
        visitedPuzzleNodes.add(initialNode.converte_tupla())
        print("First node is the solve!")
    else:
        # Put in border
        borderPuzzleNodes.append(initialNode)

        while len(borderPuzzleNodes):
            # update the max length border size
            if len(borderPuzzleNodes) > MAX_BORDER_LENGTH:
                MAX_BORDER_LENGTH = len(borderPuzzleNodes)

            # Get the first border PuzzleNode and remove of the border list
            actualPuzzleNode: Node = borderPuzzleNodes.pop(0)
            actualPuzzleNode.get_caminho()

            # Check if is finished
            if is_estado_final(actualPuzzleNode, estado_final):
                result_puzzle_node = actualPuzzleNode
                visitedPuzzleNodes.add(actualPuzzleNode.converte_tupla())
                break

            # Add actual PuzzleNode on visited array
            visitedPuzzleNodes.add(actualPuzzleNode.converte_tupla())

            # Get children states
            derivedPuzzleNodes = get_nodos_filhos(
                actualPuzzleNode, estado_final)

            # Add the derived PuzzleNodes (childrens) in border array
            for derivedPuzzleNode in derivedPuzzleNodes:
                # Check if the derived node (children) has already visited
                if not is_estado_visitado(derivedPuzzleNode, visitedPuzzleNodes):
                    borderPuzzleNodes.append(derivedPuzzleNode)
                    borderPuzzleNodes.sort(key=lambda x: x.custo_total)
                    CREATED_NODES += 1

    return get_resultado(START_TIME, visitedPuzzleNodes, MAX_BORDER_LENGTH, CREATED_NODES, result_puzzle_node)
