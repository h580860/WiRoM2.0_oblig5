import heapq
import queue
from collections import defaultdict
from queue import PriorityQueue


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.weight = w

    def other(self, node):
        if node == self.u:
            return self.v
        else:
            return self.u


def scan(graph, edges, adj_matrix, marked, pq, v):
    marked[v] = True
    for edge in graph[v]:
        if not marked[edge.other(v)]:
            pq.put((edge.weight, edge))


def prim(graph, edges, adj_matrix, marked, pq, mst, weight, s):
    scan(graph, edges, adj_matrix, marked, pq, s)

    while pq:
        # Because the PriorityQueue consists of a tuple of (edge weight, edge), we take its second element right away,
        # namely the Edge object
        edge = pq.get()[1]
        u = edge.u
        v = edge.v
        if marked[u] and marked[v]:
            continue
        mst.append(edge)
        weight += edge.weight
        if not marked[u]:
            scan(graph, edges, adj_matrix, marked, pq, u)
        if not marked[v]:
            scan(graph, edges, adj_matrix, marked, pq, v)

    print(f'Total Cost = {weight}')
    print(f'mst:\n{mst}')






def prim_mst(n, m, graph, edges, adj_matrix):
    # Source: https://algs4.cs.princeton.edu/43mst/LazyPrimMST.java.html
    mst = []
    # The priority queue is on the form:
    # (edge.weight, edge)
    pq = PriorityQueue()
    weight = 0
    marked = [False for _ in range(n)]
    for v in range(n):
        if not marked[v]:
            prim(graph, edges, adj_matrix, marked, pq, mst, weight, v)


def prims_algorithm(graph):
    # Source: https://www.programiz.com/dsa/prim-algorithm
    pass


def prim_adj_matrix(n, m, adj_matrix):
    # Source: https://favtutor.com/blogs/prims-algorithm-python
    selected_node = [False for _ in range(n)]
    no_edge = 0
    cost = 0
    selected_node[0] = True
    paths = []
    while no_edge < n - 1:
        minimum = float('inf')
        a = 0
        b = 0
        for i in range(n):
            if selected_node[i]:
                for j in range(n):
                    if not selected_node[j] and adj_matrix[i][j] > -1:
                        if minimum > adj_matrix[i][j]:
                            minimum = adj_matrix[i][j]
                            a = i
                            b = j
        # print(f"{a} - {b} : {adj_matrix[a][b]}")
        paths.append((a, b))
        cost += adj_matrix[a][b]
        selected_node[b] = True
        no_edge += 1
    if cost < 0:
        print("Impossible")
        return

    print(cost)
    # print(f"Total cost = {cost}")
    for x in paths:
        print(f'{x[0]} {x[1]}')


def node_in_queue(queue, node):
    for x in queue:
        if node in x[1]:
            return True
    return False


def jarnik_prim_algoritm(n, m, graph, edges_weighted, adj_matrix):
    # Soure: http://www.programming-algorithms.net/article/43764/Jarnik-Prim-algorithm
    # priority_queue = list(range(n))
    priority_queue = PriorityQueue()
    print(graph)

    for edge in edges_weighted:
        # heapq.heappush(priority_queue, (edge[2], (edge[0], edge[1])))
        priority_queue.put((edge[2], (edge[0], edge[1])))

    print(priority_queue)
    # while priority_queue:
    #     print(priority_queue.get())

    distances = [float('inf') for _ in range(m)]
    distances[0] = 0

    predecessors = []
    #
    while priority_queue:
        u = priority_queue.get()
        print(f'u = {u}')
        print(f"v={graph[u[1][0]]}")
        for node in graph[u[1][0]]:
            print(f"node={node}")
            if node_in_queue(priority_queue, node) and adj_matrix[u][node] < distances[node]:
                predecessors[node] = u
                distances[node] = adj_matrix[u][node]

    print("Predecessors")
    print(predecessors)


def solve():
    while True:
        n, m = [int(x) for x in input().split()]
        if n == 0 and m == 0:
            return

        # graph = defaultdict(list)
        # graph = [[]]
        vertices = list(range(n))
        # edges_weighted = []
        # adj_matrix = [[-1 for _ in range(n)] for _ in range(n)]
        adj_matrix = [[0 for _ in range(n)] for _ in range(n)]

        graph = defaultdict(list)
        edges = []

        for _ in range(m):
            # graph[u].append((v, w))
            u, v, w = [int(x) for x in input().split()]
            # edges_weighted.append((u, v, w))
            edge = Edge(u, v, w)
            graph[u].append(edge)
            graph[v].append(edge)
            # edges.append((u, v, w))
            edges.append(edge)
            adj_matrix[u][v] = w
            adj_matrix[v][u] = w
        # jarnik_prim_algoritm(n, m, graph, edges, adj_matrix)
        prim_mst(n, m, graph, edges, adj_matrix)
        return
        # for x in adj_matrix:
        #     print(x)
        # res = prims_algorithm(graph)
        # res = prim_from_pseudo(vertices, edges_weighted)
        # prim_adj_matrix(n, m, adj_matrix)
        # if res:
        #     print(res)
        # else:
        #     print("Impossible")


def solve_kattis_lostmap():
    n = int(input())
    adj_matrix = []
    for _ in range(n):
        adj_matrix.append([int(x) for x in input()])



if __name__ == '__main__':
    solve()
    # solve2()
    solve_kattis_lostmap()
