import sys
import heapq

def read_graph(filename):
    graph = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "END OF INPUT":
                break
            a, b, d = line.split()
            d = float(d)

            graph.setdefault(a, []).append((b, d))
            graph.setdefault(b, []).append((a, d))
    return graph


def read_heuristic(filename):
    h = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "END OF INPUT":
                break
            city, val = line.split()
            h[city] = float(val)
    return h


def reconstruct(node):
    route = []
    while node["parent"] is not None:
        route.append((node["parent"]["state"], node["state"], node["cost"]))
        node = node["parent"]
    route.reverse()
    return route


def search(graph, start, goal, heuristic=None):

    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 1

    fringe = []
    start_node = {
        "state": start,
        "g": 0,
        "parent": None,
        "cost": 0
    }

    f = 0 if heuristic is None else heuristic.get(start, 0)
    heapq.heappush(fringe, (f, start_node))

    closed = set()

    while fringe:
        _, node = heapq.heappop(fringe)
        nodes_popped += 1

        state = node["state"]

        if state in closed:
            continue

        closed.add(state)
        nodes_expanded += 1

        if state == goal:
            route = reconstruct(node)
            return nodes_popped, nodes_expanded, nodes_generated, node["g"], route

        for nbr, cost in graph.get(state, []):
            child = {
                "state": nbr,
                "g": node["g"] + cost,
                "parent": node,
                "cost": cost
            }

            if heuristic is None:
                priority = child["g"]
            else:
                priority = child["g"] + heuristic.get(nbr, 0)

            heapq.heappush(fringe, (priority, child))
            nodes_generated += 1

    return nodes_popped, nodes_expanded, nodes_generated, float("inf"), None


def main():

    if len(sys.argv) not in [4, 5]:
        print("Usage: find_route input_file start goal [heuristic]")
        return

    input_file = sys.argv[1]
    start = sys.argv[2]
    goal = sys.argv[3]

    heuristic = None
    if len(sys.argv) == 5:
        heuristic = read_heuristic(sys.argv[4])

    graph = read_graph(input_file)

    popped, expanded, generated, dist, route = search(
        graph, start, goal, heuristic
    )

    print(f"Nodes Popped: {popped}")
    print(f"Nodes Expanded: {expanded}")
    print(f"Nodes Generated: {generated}")

    if dist == float("inf"):
        print("Distance: Infinity")
        print("Route:")
        print("None")
    else:
        print(f"Distance: {dist} km")
        print("Route:")
        for a, b, c in route:
            print(f"{a} to {b}, {c} km")


if __name__ == "__main__":
    main()