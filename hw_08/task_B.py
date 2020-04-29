# B. Разрез

from collections import defaultdict, deque


class Edge:
    def __init__(self, from_, to, flow, capacity, reverse_edge=None):
        self.from_ = from_
        self.to = to
        self.flow = flow
        self.capacity = capacity
        self.reverse_edge = reverse_edge


def main():
    n_vertex, n_edges = map(int, input().split())
    source_vertex_idx, finish_vertex_idx = 0, n_vertex - 1

    edges = []
    for _ in range(n_edges):
        from_vertex_idx, to_vertex_idx, edge_capacity = map(int, input().split())
        from_vertex_idx -= 1
        to_vertex_idx -= 1

        straight_edge = Edge(from_vertex_idx, to_vertex_idx, 0, edge_capacity, None)
        reverse_edge = Edge(to_vertex_idx, from_vertex_idx, 0, edge_capacity, straight_edge)
        straight_edge.reverse_edge = reverse_edge

        edges.append(straight_edge)
        edges.append(reverse_edge)

    outgoing_edges = defaultdict(list)
    for edge_idx, edge in enumerate(edges):
        outgoing_edges[edge.from_].append(edge_idx)

    while True:
        queue = deque()
        queue.append(source_vertex_idx)

        reverse_edges = [None] * n_vertex
        reverse_edges[source_vertex_idx] = 0

        # bfs
        while queue:
            cur_node_idx = queue.popleft()
            if cur_node_idx == finish_vertex_idx:
                break

            for edge_idx in outgoing_edges[cur_node_idx]:
                next_edge = edges[edge_idx]
                if reverse_edges[next_edge.to] is None and next_edge.flow < next_edge.capacity:
                    reverse_edges[next_edge.to] = edge_idx
                    queue.append(next_edge.to)

        # no paths from source to finish
        if reverse_edges[finish_vertex_idx] is None:
            break

        min_flow_capacity = float('inf')
        temp_vertex_idx = finish_vertex_idx
        while temp_vertex_idx != source_vertex_idx:
            edge = edges[reverse_edges[temp_vertex_idx]]
            free_capacity = edge.capacity - edge.flow
            if free_capacity < min_flow_capacity:
                min_flow_capacity = free_capacity
            temp_vertex_idx = edge.from_

        temp_vertex_idx = finish_vertex_idx
        while temp_vertex_idx != source_vertex_idx:
            edge = edges[reverse_edges[temp_vertex_idx]]
            edge.flow += min_flow_capacity
            edge.reverse_edge.flow -= min_flow_capacity
            temp_vertex_idx = edge.from_

    max_flow = 0
    for edge_idx in outgoing_edges[source_vertex_idx]:
        max_flow += edges[edge_idx].flow

    min_cut_vertexes = [False] * n_vertex
    min_cut_vertexes[source_vertex_idx] = True
    queue = deque()
    queue.append(source_vertex_idx)
    while queue:
        vertex = queue.popleft()
        for edge_idx in outgoing_edges[vertex]:
            next_edge = edges[edge_idx]
            if min_cut_vertexes[next_edge.to] is False and next_edge.capacity != abs(next_edge.flow):
                min_cut_vertexes[next_edge.to] = True
                queue.append(next_edge.to)

    min_cut_edges = []
    for edge_idx in range(n_edges):
        edge = edges[edge_idx * 2]
        if min_cut_vertexes[edge.from_] ^ min_cut_vertexes[edge.to]:
            min_cut_edges.append(edge_idx + 1)

    print(len(min_cut_edges), max_flow)
    print(*min_cut_edges)


if __name__ == "__main__":
    main()
