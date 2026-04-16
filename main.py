import pygraph as pg
import os

# -------------------------------
# Exemplo de uso do programa
# -------------------------------
if __name__ == "__main__":
    # Ler grafo a partir de arquivo
    # system_dir = "D:\Users\Gabriel\Documents\Gabriel\07_FACULDADE\8º Semestre\Teoria dos Grafos\atividade"
    nome_arquivo = "grafo01.txt"  # Arquivo de entrada
    file = os.path.join(nome_arquivo)
    G, ponderado = pg.ler_grafo_arquivo(file)

    # Adicionar vértice manualmente
    # pg.adicionar_vertice(G, "E")

    # Adicionar aresta manualmente
    # pg.adicionar_aresta(G, "E", "A")

    # Visualizar grafo
    pg.visualizar_grafo(G, ponderado)

    # Transformar em matriz 2D
    print(pg.matriz_2d(G, ponderado, incidencia=True))

    # Lista de adjacencias
    print(pg.lista_adjacencia(G, ponderado))
