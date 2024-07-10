import snappy
import networkx as nx

def laplacian(G, i, j):
    L = G.laplacian_matrix()
    L_star = L.delete_rows([i]).delete_columns([j])
    det = L_star.det()
    return L, L_star, det

def graph_of_link(L):
    dig = L.digraph()
    G = nx.DiGraph()
    for v in dig.vertices:
        G.add_node(v)
    for e in dig.edges:
        G.add_edge(e[0], e[1])
    G_und = G.to_undirected()
    return G_und

def reduced_laplacian(L, i, j):
    mtx = matrix(L)
    L_star = mtx.delete_rows([i]).delete_columns([j])
    det = L_star.det()
    return L_star, det

def laplacian_of_link(L, i, j): #returns the reduced laplacian and determinant for a link.
    K = L.sage_link()
    G = graph_of_link(L)
    ###In order to identify the link, there is a reduce function or something in snappy, or some other invariant?
    #plot = K.plot()
    #plot.show()
    lap = nx.laplacian_matrix(G).toarray()
    laplacian = reduced_laplacian(lap, i, j)
    return laplacian

i = 0
while i < 10:
    L = snappy.random_link(10)
    if len(L) == 0:
        print("Unknot")
        continue
    print(laplacian_of_link(L, 0, 0)[1])
    i+=1