# A. Максимальный поток минимальной стоимости

import sys
from collections import defaultdict, deque


class Edge:
    def __init__(self, from_, to, flow, capacity, cost, reverse_edge=None):
        self.from_ = from_
        self.to = to
        self.flow = flow
        self.capacity = capacity
        self.cost = cost
        self.reverse_edge = reverse_edge


def main():
    n_vertex, n_edges = map(int, sys.stdin.readline().split())
    source_vertex_idx, finish_vertex_idx = 0, n_vertex - 1

    edges = []
    for _ in range(n_edges):
        from_vertex_idx, to_vertex_idx, edge_capacity, edge_cost = map(int, sys.stdin.readline().split())
        from_vertex_idx -= 1
        to_vertex_idx -= 1

        straight_edge = Edge(from_vertex_idx, to_vertex_idx, 0, edge_capacity, edge_cost, None)
        reverse_edge = Edge(to_vertex_idx, from_vertex_idx, 0, 0, -edge_cost, straight_edge)
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

    # drop negative loops
    residual_network = [None] * len(edges)
    for edge_idx, edge in enumerate(edges):
        residual_network_edge = [
            edge.from_,
            edge.to,
            edge.cost if edge.capacity - edge.flow > 0 else 0
        ]
        residual_network[edge_idx] = residual_network_edge

    while True:
        vertex_distance = [0] * n_vertex
        parent_edge_idx = [None] * n_vertex
        for _ in range(n_vertex):
            last_updated_vertex = -1
            for edge_idx, (u, v, w) in enumerate(residual_network):
                if w != 0 and vertex_distance[v] > vertex_distance[u] + w:
                    vertex_distance[v] = vertex_distance[u] + w
                    parent_edge_idx[v] = edge_idx
                    last_updated_vertex = v
            if last_updated_vertex == -1:
                break

        # no negative loops
        if last_updated_vertex == -1:
            break

        loop_vertexes = set()
        loop_vertexes.add(last_updated_vertex)
        while True:
            last_updated_vertex = edges[parent_edge_idx[last_updated_vertex]].from_
            if last_updated_vertex in loop_vertexes:
                break

        max_additional_flow = float('inf')
        temp_vertex = last_updated_vertex
        while True:
            edge = edges[parent_edge_idx[temp_vertex]]
            max_additional_flow = min(max_additional_flow, edge.capacity - edge.flow)
            temp_vertex = edge.from_
            if temp_vertex == last_updated_vertex:
                break

        while True:
            edge_idx = parent_edge_idx[temp_vertex]
            reverse_edge_idx = edge_idx + 1 if edge_idx % 2 == 0 else edge_idx - 1
            edge, reverse_edge = edges[edge_idx], edges[reverse_edge_idx]
            edge.flow += max_additional_flow
            reverse_edge.flow -= max_additional_flow

            residual_network[edge_idx][2] = edge.cost if edge.capacity - edge.flow > 0 else 0
            residual_network[reverse_edge_idx][2] = reverse_edge.cost if reverse_edge.capacity - reverse_edge.flow > 0 else 0

            temp_vertex = edge.from_
            if temp_vertex == last_updated_vertex:
                break

    total_weight = 0
    for edge in edges:
        if edge.flow > 0:
            total_weight += edge.flow * edge.cost
    print(total_weight)


if __name__ == "__main__":
    main()
