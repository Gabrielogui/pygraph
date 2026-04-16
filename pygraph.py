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


def contar_trilhas_simples(G, u, v, k):
    """
    Conta e exibe caminhos simples de u até v com comprimento <= k.
    Retorna o número total de caminhos encontrados.
    """
    def dfs_recursiva(atual, destino, k_restante, caminho_atual, visitados):
        # Se atingiu o destino, o caminho é válido
        if atual == destino:
            print(f"Caminho encontrado: {' -> '.join(caminho_atual)} (Comprimento: {len(caminho_atual)-1})")
            return 1
        
        # Se o limite de passos k acabou, interrompe essa busca
        if k_restante <= 0:
            return 0
        
        total = 0
        visitados.add(atual)
        
        # Explora vizinhos
        for vizinho in G.neighbors(atual):
            if vizinho not in visitados:
                caminho_atual.append(vizinho)
                total += dfs_recursiva(vizinho, destino, k_restante - 1, caminho_atual, visitados)
                caminho_atual.pop() # Backtracking (remove para testar outra rota)
        
        visitados.remove(atual) # Permite que o vértice seja usado em outras trilhas
        return total

    if u not in G or v not in G:
        print("Vértices de origem ou destino não existem no grafo.")
        return 0

    print(f"Buscando caminhos entre {u} e {v} com comprimento máximo {k}...")
    num_trilhas = dfs_recursiva(u, v, k, [u], set())
    print(f"Total de caminhos encontrados: {num_trilhas}")
    return num_trilhas



def verificar_sequencia(G, S):
    """
    Verifica se a sequência S é passeio, caminho, trilha ou circuito.
    """
    if not S or len(S) < 2:
        print("Sequência inválida ou muito curta.")
        return

    e_passeio = True
    arestas_percorridas = []
    
    # 1. Verificar se é Passeio e coletar arestas
    for i in range(len(S) - 1):
        u, v = S[i], S[i+1]
        if G.has_edge(u, v):
            # Armazenamos como tupla ordenada se for grafo não-direcionado 
            # para identificar repetição de aresta corretamente
            aresta = tuple(sorted((u, v))) if not G.is_directed() else (u, v)
            arestas_percorridas.append(aresta)
        else:
            e_passeio = False
            break

    if not e_passeio:
        print(f"A sequência {S} NÃO é um passeio válido (arestas inexistentes).")
        return

    # 2. Verificar se é Trilha (não repete arestas)
    e_trilha = len(arestas_percorridas) == len(set(arestas_percorridas))
    
    # 3. Verificar se é Caminho (não repete vértices)
    e_caminho = len(S) == len(set(S))
    
    # 4. Verificar se é Circuito (Trilha que volta ao início)
    e_circuito = e_trilha and (S[0] == S[-1])

    # Exibição dos Resultados
    print(f"\nAnálise da sequência {S}:")
    print(f"- Passeio: Sim")
    print(f"- Trilha: {'Sim' if e_trilha else 'Não'}")
    print(f"- Caminho: {'Sim' if e_caminho else 'Não'}")
    print(f"- Circuito: {'Sim' if e_circuito else 'Não'}")


