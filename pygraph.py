import networkx as nx
import matplotlib.pyplot as plt
import os


def ler_grafo_arquivo(nome_arquivo):
    """
    Lê um arquivo de texto e cria um grafo/dígrafo (ponderado ou não).
    
    Formato esperado:
    1ª linha: [G|D] [N|W]
        G = Grafo não direcionado
        D = Dígrafo
        N = Não ponderado
        W = Ponderado
    Demais linhas:
        Se não ponderado: u v
        Se ponderado:     u v w
    """
    try:
        with open(nome_arquivo, "r") as f:
            linhas = [linha.strip() for linha in f if linha.strip()]

        if not linhas:
            print("Arquivo vazio!")
            return None, False

        # Definição do tipo de grafo
        tipo, peso = linhas[0].split()
        if tipo == "G":
            G = nx.Graph()
        elif tipo == "D":
            G = nx.DiGraph()
        else:
            raise ValueError("Primeiro caractere deve ser 'G' ou 'D'.")

        ponderado = (peso == "W")

        # Leitura das arestas
        for linha in linhas[1:]:
            partes = linha.split()
            if ponderado:
                if len(partes) != 3:
                    raise ValueError("Esperado formato 'u v w' para grafos ponderados.")
                u, v, w = partes
                adicionar_aresta(G, u, v, w, ponderado)
            else:
                if len(partes) != 2:
                    raise ValueError("Esperado formato 'u v' para grafos não ponderados.")
                u, v = partes
                adicionar_aresta(G, u, v, ponderado)  # peso padrão 1

        print(f"Grafo criado ({'dígrafo' if tipo=='D' else 'grafo'}, "
            f"{'ponderado' if ponderado else 'não ponderado'}) com "
            f"{G.number_of_nodes()} vértices e {G.number_of_edges()} arestas.")
        return G, ponderado

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None, False


def adicionar_vertice( G, v):
    """Adiciona um vértice ao grafo, se não existir."""
    if v not in G:
        G.add_node(v)
        print(f"Vértice '{v}' adicionado.")
    else:
        print(f"Vértice '{v}' já existe.")


def adicionar_aresta( G, u, v, w=1, ponderado=False):
    """Adiciona uma aresta ao grafo."""
    if ponderado:
        G.add_edge(u, v, weight=float(w))
        print(f"Aresta '{u} - {v}' com peso {w} adicionada.")
    else:
        G.add_edge(u, v)
        print(f"Aresta '{u} - {v}' adicionada.")


def visualizar_grafo( G, ponderado=False):
    """Desenha o grafo (ou dígrafo) com ou sem pesos."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='black', node_size=1000, font_size=12,
            arrows=isinstance(G, nx.DiGraph), arrowsize=20)

    # Se for ponderado, mostrar pesos
    if ponderado:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Visualização do Grafo")
    plt.show()

# -------------------------------
# MINHA ATIVIDADE (TRANSFORMAR EM MATRIZ 2D)
# -------------------------------

def matriz_2d( G: nx.Graph, ponderado: bool = False, digrafo: bool = False, incidencia: bool = False):
    numero_vertices = G.number_of_nodes()
    matriz = [[0 for i in range(numero_vertices)] for j in range(numero_vertices)]
    #print(matriz)

    vertices = list(G.nodes())

    for i in range(numero_vertices):
        for j in range(numero_vertices):
            vertice_i = vertices[i]
            vertice_j = vertices[j]
            if G.has_edge(vertice_i, vertice_j):
                if ponderado:
                    matriz[i][j] = G[vertices[i]][vertices[j]]["weight"]
                else:
                    matriz[i][j] = 1

    if incidencia:
        numero_arestas = G.number_of_edges()
        matriz_incidencia = [[0 for i in range(numero_vertices)] for j in range(numero_arestas)]

        arestas = list(G.edges())

        for i in range(numero_vertices):
            for j in range(numero_arestas):
                vertice_i = vertices[i]
                aresta_j = arestas[j]
                if G.has_edge(vertice_i, aresta_j[0]):
                    if ponderado:
                        matriz_incidencia[j][i] = G[vertices[i]][aresta_j[0]]["weight"]
                    else:
                        matriz_incidencia[j][i] = 1

        matriz = matriz_incidencia

    return matriz
    
def lista_adjacencia( G: nx.Graph, ponderado: bool = False, digrafo: bool = False):
    lista_adj = {}

    vertices = list(G.nodes())
    numero_vertices = G.number_of_nodes()

    for i in range(numero_vertices):
        lista_vertices = []
        for j in range(numero_vertices):
            if (G.has_edge(vertices[i], vertices[j])):
                lista_vertices.append(vertices[j])
                lista_adj[vertices[i]] = lista_vertices

    return lista_adj





