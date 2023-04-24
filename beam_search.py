from queue import PriorityQueue
from branch_and_bound import length, bound
from utils import Node

def travel(adj_mat, src=0, beam_width=10):
    optimal_tour = []
    n = len(adj_mat)
    if not n:
        raise ValueError("Invalid adj Matrix")
    PQ = PriorityQueue()
    v = Node(level=0, path=[0])
    v.bound = bound(adj_mat, v)
    PQ.put(v)
    while not PQ.empty():
        nodes = [PQ.get() for _ in range(min(beam_width, PQ.qsize()))]
        next_nodes = []
        for v in nodes:
            u = Node(level=v.level + 1, path=v.path[:])
            for i in filter(lambda x: x not in v.path, range(1, n)):
                u.path.append(i)
                if u.level == n - 2:
                    l = set(range(1, n)) - set(u.path)
                    u.path.append(list(l)[0])
                    # putting the first vertex at last
                    u.path.append(0)
                    _len = length(adj_mat, u)
                    if not optimal_tour or _len < optimal_tour[1]:
                        optimal_tour = (u.path[:], _len)
                else:
                    u.bound = bound(adj_mat, u)
                    if not optimal_tour or u.bound < optimal_tour[1]:
                        next_nodes.append(u)
                # make a new node at each iteration! python it is!!
                u = Node(level=v.level + 1, path=v.path[:])
        next_nodes = sorted(next_nodes, key=lambda x: x.bound)
        for i in range(min(beam_width, len(next_nodes))):
            PQ.put(next_nodes[i])

    # shifting to proper source(start of path)
    optimal_tour_src = optimal_tour[0]
    if src != 1:
        optimal_tour_src = optimal_tour_src[:-1]
        y = optimal_tour_src.index(src)
        optimal_tour_src = optimal_tour_src[y:] + optimal_tour_src[:y]
        optimal_tour_src.append(optimal_tour_src[0])

    return optimal_tour_src, optimal_tour[1]