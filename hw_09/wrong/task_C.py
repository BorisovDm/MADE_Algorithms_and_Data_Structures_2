# C. План эвакуации


class Edge:
    def __init__(self, from_, to, flow, capacity, cost, reverse_edge=None):
        self.from_ = from_
        self.to = to
        self.flow = flow
        self.capacity = capacity
        self.cost = cost
        self.reverse_edge = reverse_edge


def distance(point_1, point_2):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1]) + 1


def main():
    n, m = map(int, input().split())

    buildings = []
    for _ in range(n):
        x, y, _ = map(int, input().split())
        buildings.append((x, y))

    shelters = []
    for _ in range(m):
        p, q, c = map(int, input().split())
        shelters.append([p, q, c])

    evacuation_graph = [
        list(map(int, input().split()))
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(m):
            shelters[j][2] -= evacuation_graph[i][j]

    edges = []
    for i in range(n):
        for j in range(m):
            d = distance(buildings[i], shelters[j][:2])

            straight_edge = Edge(i, j + n, evacuation_graph[i][j], evacuation_graph[i][j] + 1, d, None)
            reverse_edge = Edge(j + n, i, 0, 0, (-d if evacuation_graph[i][j] > 0 else 0), straight_edge)
            straight_edge.reverse_edge = reverse_edge

            edges.append(straight_edge)
            edges.append(reverse_edge)

    n_vertex = n + m
    vertex_distance = [0] * n_vertex
    parent_edge_idx = [None] * n_vertex

    for _ in range(n_vertex):
        last_updated_vertex = -1
        for edge_idx, edge in enumerate(edges):
            u, v, w = edge.from_, edge.to, edge.cost

            if w != 0 and vertex_distance[v] > vertex_distance[u] + w and shelters[v - n if edge_idx % 2 == 0 else v][2] > 0:
                vertex_distance[v] = vertex_distance[u] + w
                parent_edge_idx[v] = edge_idx
                last_updated_vertex = v

        if last_updated_vertex == -1:
            print('OPTIMAL')
            return

    loop_vertexes = set()
    loop_vertexes.add(last_updated_vertex)
    while True:
        last_updated_vertex = edges[parent_edge_idx[last_updated_vertex]].from_
        if last_updated_vertex in loop_vertexes:
            break

    temp_vertex = last_updated_vertex
    while True:
        edge_idx = parent_edge_idx[temp_vertex]
        reverse_edge_idx = edge_idx + 1 if edge_idx % 2 == 0 else edge_idx - 1
        edge, reverse_edge = edges[edge_idx], edges[reverse_edge_idx]
        edge.flow += 1
        reverse_edge.flow -= 1

        temp_vertex = edge.from_
        if temp_vertex == last_updated_vertex:
            break

    print('SUBOPTIMAL')

    for i in range(n):
        for j in range(m):
            edge_idx = (i * n + j) * 2
            print(edges[edge_idx].flow, end=' ')
        print()


if __name__ == "__main__":
    main()
