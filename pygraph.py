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


def algoritmo_tarjan(G):
    """
    Objetivo: Identificar todas as Componentes Fortemente Conectadas (SCCs) 
    do dígrafo utilizando uma única busca em profundidade (DFS).
    """
    
    # --- Variáveis Auxiliares ---
    # discovery_time: Dicionário para armazenar a ordem em que cada nó foi visitado.
    # low_link: Menor índice de descoberta alcançável a partir do nó (incluindo ele mesmo).
    # stack: Pilha para manter os nós que estão na DFS atual e podem formar uma SCC.
    # on_stack: Conjunto para verificação rápida (O(1)) se um nó está na pilha.
    # sccs: Lista que armazenará as listas de componentes encontradas.
    
    discovery_time = {}
    low_link = {}
    stack = []
    on_stack = set()
    sccs = []
    tempo = 0 # Contador global para os índices de descoberta

    def dfs_tarjan(u):
        nonlocal tempo
        # Inicializa o tempo de descoberta e o low-link do nó atual
        discovery_time[u] = low_link[u] = tempo
        tempo += 1
        stack.append(u)
        on_stack.add(u)

        # Explora os vizinhos do vértice u
        for v in G.neighbors(u):
            # Caso 1: Vizinho ainda não foi visitado
            if v not in discovery_time:
                dfs_tarjan(v)
                # Após a volta da recursão, atualiza o low-link de u
                low_link[u] = min(low_link[u], low_link[v])
            
            # Caso 2: Vizinho está na pilha (faz parte da SCC atual)
            elif v in on_stack:
                # Atualiza o low-link com o tempo de descoberta do vizinho
                low_link[u] = min(low_link[u], discovery_time[v])

        # Se u é a "raiz" de uma SCC (seu low-link é igual ao seu tempo de descoberta)
        if low_link[u] == discovery_time[u]:
            nova_scc = []
            while True:
                no = stack.pop()
                on_stack.remove(no)
                nova_scc.append(no)
                if no == u: # Para quando voltamos ao nó raiz da SCC
                    break
            sccs.append(nova_scc)

    # Garante que todos os vértices sejam visitados (trata grafos desconexos)
    for vertice in G.nodes():
        if vertice not in discovery_time:
            dfs_tarjan(vertice)

    # --- Exibição dos Resultados ---
    print("\n--- Componentes Fortemente Conectadas (Tarjan) ---")
    print(f"Total de SCCs encontradas: {len(sccs)}")
    for i, componente in enumerate(sccs, 1):
        print(f"SCC {i}: {componente}")
    
    return sccs


def algoritmo_dijkstra(G: nx.Graph, origem, destino):
    # 1. Inicialização correta dos dicionários
    d = {u: float("inf") for u in G.nodes()} 
    p = {u: None for u in G.nodes()}
    q = list(G.nodes()) # Fila de nós a visitar

    d[origem] = 0

    while q:
        # 2. Extrair o nó com a menor distância atual
        # (Em implementações profissionais, usa-se heapq para ser O(log V))
        u = min(q, key=lambda node: d[node])

        # Se a menor distância for infinito, os nós restantes são inacessíveis
        if d[u] == float("inf"):
            break
            
        # Se chegamos ao destino, podemos parar (otimização)
        if u == destino:
            break

        q.remove(u)

        # 3. Relaxamento das arestas vizinhas
        for v in G.neighbors(u):
            peso = G[u][v].get("weight", 1)
            if d[v] > d[u] + peso:
                d[v] = d[u] + peso
                p[v] = u

    # 4. Reconstrução do caminho
    caminho = []
    atual = destino
    # Verifica se o destino é alcançável antes de montar o caminho
    if d[destino] == float("inf"):
        return None # Ou [], indicando que não há caminho

    while atual is not None:
        caminho.append(atual)
        atual = p[atual]

    caminho.reverse()
    return caminho

    '''for u in G.nodes():
        d.append(float("inf"))
        p.append(None)
        q.append(u)

    d[origem] = 0

    while q != None:
        u = min(d)
        if u == float("inf"):
            break

        q.remove(u)

        for v in G.neighbors(u):
            if d[v] > d[u] + G[u][v]["weight"]:
                d[v] = d[u] + G[u][v]["weight"]
                p[v] = u
    
    caminho = [destino]
    while p[destino] != None:
        caminho.append(p[destino])
        destino = p[destino]

    caminho.reverse()
    return caminho'''
        
def algoritmo_bellman_ford(G, origem, destino):
    # 1. Inicialização: Distância infinita e sem antecessores
    d = {u: float("inf") for u in G.nodes()}
    p = {u: None for u in G.nodes()}
    
    d[origem] = 0

    # 2. Relaxamento repetido (V - 1 vezes)
    for _ in range(G.number_of_nodes() - 1):
        for u, v, data in G.edges(data=True):
            peso = data.get("weight", 1)
            
            # Relaxar aresta u -> v
            if d[u] != float("inf") and d[v] > d[u] + peso:
                d[v] = d[u] + peso
                p[v] = u
            
            # Se o grafo for não-direcionado, relaxar v -> u também
            if not G.is_directed():
                if d[v] != float("inf") and d[u] > d[v] + peso:
                    d[u] = d[v] + peso
                    p[u] = v

    # 3. Verificação de ciclos negativos (Opcional, mas recomendado)
    for u, v, data in G.edges(data=True):
        peso = data.get("weight", 1)
        if d[u] != float("inf") and d[v] > d[u] + peso:
            raise ValueError("O grafo contém um ciclo de peso negativo!")

    # Reconstruir o caminho do destino para a origem
    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        atual = p[atual]
    
    # Se o primeiro elemento não for a origem, o destino é inacessível
    if caminho[0] != origem:
        return float("inf"), []

    return d[destino], caminho


def algoritmo_kruskal(G: nx.Graph):
    """
    Calcula a Árvore Geradora Mínima (MST) de um grafo utilizando o algoritmo de Kruskal.
    Retorna um conjunto de tuplas (u, v) representando as arestas da MST.
    """
    # Ordena todas as arestas do grafo pelo peso ('weight')
    arestas_ordenadas = sorted(G.edges(data=True), key=lambda x: x[2].get('weight', 1))
    
    # Estrutura Union-Find para controle de ciclos
    # Inicialmente, cada nó é pai de si mesmo
    pai = {u: u for u in G.nodes()}
    
    def find(u):
        # Encontra a raiz do conjunto do nó u (com compressão de caminho)
        if pai[u] != u:
            pai[u] = find(pai[u])
        return pai[u]
        
    def union(u, v):
        # Une os conjuntos dos nós u e v
        raiz_u = find(u)
        raiz_v = find(v)
        if raiz_u != raiz_v:
            pai[raiz_u] = raiz_v
            return True
        return False

    mst_edges = set()
    
    # Percorre as arestas ordenadas e adiciona na MST se não formarem ciclo
    for u, v, data in arestas_ordenadas:
        if union(u, v):
            # Armazena de forma padronizada (menor, maior) para facilitar a comparação no plot
            mst_edges.add((min(u, v), max(u, v)))
            
            # Uma MST sempre tem exatamente V - 1 arestas. Se atingir, podemos parar.
            if len(mst_edges) == G.number_of_nodes() - 1:
                break
                
    return mst_edges

def visualizar_grafo_mst(G, mst_edges, ponderado=True):
    """
    Desenha o grafo destacando as arestas da MST em azul e as demais em cinza.
    """
    pos = nx.spring_layout(G, seed=42) # seed fixo para manter o mesmo layout se rodar mais de uma vez
    
    # Separa as arestas em dois grupos com base no retorno do Kruskal
    arestas_mst = []
    arestas_restantes = []
    
    for u, v in G.edges():
        aresta_padrao = (min(u, v), max(u, v))
        if aresta_padrao in mst_edges:
            arestas_mst.append((u, v))
        else:
            arestas_restantes.append((u, v))
            
    # 1. Desenha os nós
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=12)
    
    # 2. Desenha as arestas normais (Cinza, mais finas e tracejadas)
    nx.draw_networkx_edges(G, pos, edgelist=arestas_restantes, edge_color='gray', width=1.5, style='dashed')
    
    # 3. Desenha as arestas da MST (Azul, mais grossas)
    nx.draw_networkx_edges(G, pos, edgelist=arestas_mst, edge_color='blue', width=3.5)
    
    # 4. Mostrar pesos se o grafo for ponderado
    if ponderado:
        labels = nx.get_edge_attributes(G, 'weight')
        # Formatação simples para remover o '.0' de números inteiros na exibição
        labels_formatados = {k: int(v) if v.is_integer() else v for k, v in labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_formatados)
        
    plt.title("Árvore Geradora Mínima (Kruskal) - MST em Azul")
    plt.axis('off') # Remove as bordas dos eixos para um visual mais limpo
    plt.show()

def ford_fulkerson(G, exibir_passos=True):
    """
    Implementa o Algoritmo de Ford-Fulkerson (Edmonds-Karp) para encontrar o fluxo máximo.
    Retorna o valor do fluxo máximo, os caminhos aumentantes e o dicionário de fluxos finais.
    """
    if not isinstance(G, nx.DiGraph):
        print("Erro: Ford-Fulkerson requer um Gráfico Direcionado (Dígrafo).")
        return 0, [], {}, None, None

    # 1. Identificar fontes (grau de entrada = 0) e sorvedouros (grau de saída = 0)
    fontes_nativas = [n for n in G.nodes() if G.in_degree(n) == 0]
    sorvedouros_nativos = [n for n in G.nodes() if G.out_degree(n) == 0]

    # Criar uma cópia do grafo para trabalhar com a rede de fluxo e os nós fictícios
    F = G.copy()
    
    # Inicializar os fluxos de todas as arestas originais com 0
    for u, v in F.edges():
        F[u][v]['flow'] = 0.0

    s_ficticio = "super_source"
    t_ficticio = "super_sink"

    # Conectar super-origem às fontes nativas
    for f in fontes_nativas:
        F.add_edge(s_ficticio, f, weight=float('inf'), flow=0.0)
    
    # Conectar sorvedouros nativos ao super-sorvedouro
    for s in sorvedouros_nativos:
        F.add_edge(s, t_ficticio, weight=float('inf'), flow=0.0)

    # 2. Função auxiliar BFS para encontrar o caminho aumentante na Rede Residual
    def encontrar_caminho_bfs(residual_adj, txt_s, txt_t):
        fila = [txt_s]
        pais = {txt_s: None}
        
        while fila:
            atual = fila.pop(0)
            if atual == txt_t:
                # Reconstruir o caminho
                caminho = []
                while atual is not None:
                    caminho.insert(0, atual)
                    atual = pais[atual]
                return caminho
            
            for vizinho, cap_residual in residual_adj[atual].items():
                if vizinho not in pais and cap_residual > 0:
                    pais[vizinho] = atual
                    fila.append(vizinho)
        return None

    fluxo_maximo = 0.0
    caminhos_aumentantes = []

    # 3. Loop Principal do Ford-Fulkerson
    while True:
        # Construir a rede residual explicitamente a partir do estado atual de F
        rede_residual = {n: {} for n in F.nodes()}
        for u, v, data in F.edges(data=True):
            cap = data.get('weight', 0.0)
            flx = data.get('flow', 0.0)
            
            # Aresta direta: capacidade restante
            cap_direta = cap - flx
            if cap_direta > 0:
                rede_residual[u][v] = rede_residual[u].get(v, 0.0) + cap_direta
                
            # Aresta reversa: fluxo que pode ser cancelado
            if flx > 0:
                rede_residual[v][u] = rede_residual[v].get(u, 0.0) + flx

        # Buscar caminho aumentante na rede residual
        caminho = encontrar_caminho_bfs(rede_residual, s_ficticio, t_ficticio)
        if not caminho:
            break  # Nenhum caminho encontrado = fluxo máximo atingido

        # Encontrar a capacidade gargalo do caminho escolhido
        gargalo = float('inf')
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i+1]
            gargalo = min(gargalo, rede_residual[u][v])

        # Atualizar os fluxos ao longo do caminho na rede original
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i+1]
            if F.has_edge(u, v):
                F[u][v]['flow'] += gargalo
            else:
                # Se a aresta percorrida na rede residual for reversa
                F[v][u]['flow'] -= gargalo

        fluxo_maximo += gargalo
        caminhos_aumentantes.append((caminho, gargalo))
        
        if exibir_passos:
            print(f"Caminho Aumentante: {' -> '.join(caminho)} | Gargalo: {gargalo}")

    # Montar a tabela final apenas com as arestas originais do grafo
    tabela_fluxos = {}
    for u, v in G.edges():
        tabela_fluxos[(u, v)] = {
            'capacidade': F[u][v]['weight'],
            'fluxo': F[u][v]['flow']
        }

    return fluxo_maximo, caminhos_aumentantes, tabela_fluxos, s_ficticio, t_ficticio


def visualizar_fluxo_maximo(G, tabela_fluxos):
    """
    Gera o plot do grafo destacando em vermelho as arestas onde o fluxo é igual à capacidade
    (arestas saturadas / gargalos) e exibindo o rótulo como Fluxo/Capacidade.
    """
    pos = nx.spring_layout(G, seed=42)
    
    arestas_saturadas = []
    arestas_com_fluxo = []
    arestas_vazias = []
    
    labels_arestas = {}
    
    for u, v in G.edges():
        fluxo = tabela_fluxos[(u, v)]['fluxo']
        capacidade = tabela_fluxos[(u, v)]['capacidade']
        labels_arestas[(u, v)] = f"{int(fluxo)}/{int(capacidade)}"
        
        if fluxo == capacidade and capacidade > 0:
            arestas_saturadas.append((u, v))
        elif fluxo > 0:
            arestas_com_fluxo.append((u, v))
        else:
            arestas_vazias.append((u, v))

    # Desenhar os nós
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Desenhar as arestas por categorias de fluxo
    nx.draw_networkx_edges(G, pos, edgelist=arestas_vazias, edge_color='gray', width=1.5, style='dashed', arrowsize=15)
    nx.draw_networkx_edges(G, pos, edgelist=arestas_com_fluxo, edge_color='blue', width=2.5, arrowsize=18)
    nx.draw_networkx_edges(G, pos, edgelist=arestas_saturadas, edge_color='red', width=4.0, arrowsize=22)
    
    # Rótulos das arestas (Fluxo/Capacidade)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_arestas, font_size=10)
    
    plt.title("Rede de Fluxo Máximo Final\n(Vermelho: Saturada | Azul: Com Fluxo | Tracejado: Vazia)")
    plt.axis('off')
    plt.show()