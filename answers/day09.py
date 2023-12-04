from itertools import permutations


# Straylight to Arbre = 127
class City:
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        self.distances = []
        self.visited = False

    def __repr__(self):
        return f"City:{self.name}"

    def add_neighbour(self, neighbour, distance):
        self.neighbours.append(neighbour)
        self.distances.append(distance)

    def outro_nao_mesmo(self, origem):
        pass

    def distance_to(self, city):
        for idx, c in enumerate(self.neighbours):
            if c.name == city:
                return int(self.distances[idx])
        raise ValueError(f"{city} not neighbour of {self}")


"""
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
  function Dijkstra(Graph, source):

      create vertex set Q

      for each vertex v in Graph:
          dist[v] ← INFINITY
          prev[v] ← UNDEFINED
          add v to Q
      dist[source] ← 0

      while Q is not empty:
          u ← vertex in Q with min dist[u]

          remove u from Q

          for each neighbor v of u:           // only v that are still in Q
              alt ← dist[u] + length(u, v)
              if alt < dist[v]:
                  dist[v] ← alt
                  prev[v] ← u

      return dist[], prev[]
"""


def Dijkstra(cities, source, target):
    Q = list()

    dist = dict()
    prev = dict()
    for v in cities:
        dist[v] = 65000
        prev[v] = None
        Q.append(v)
    dist[source.name] = 0
    # print(dist)
    # print(prev)

    while len(Q) > 0:
        min_temp = min(dist.values())
        u_list = [uu for uu in Q if dist[uu] == min_temp]
        for u in u_list:
            Q.remove(u)
        if u == target.name:
            break
        for u in u_list:
            for idx, v in enumerate(cities[u].neighbours):
                if v.name in Q:
                    alt = dist[u] + cities[u].distance[idx]
                    if alt < dist[v.name]:
                        dist[v.name] = alt
                        prev[v.name] = u
    return dist, prev


"""
def brute_force_search(source, running, path):
    new_path = path
    new_running = running
    for idx, c in enumerate(source.neighbours):
        if c.name not in path:
            new_path += [c.name]
            new_running += [source.distances[idx]]
            new_path, new_running = brute_force_search(c, new_path, new_running)
    return new_path, new_running
"""


def brute_force_search(cities):
    perms = list(permutations(cities.keys()))
    dist = list()
    for path in perms:
        running = 0
        for i in range(len(path) - 1):
            running += cities[path[i]].distance_to(path[i + 1])
        dist.append(running)

    min_dist = min(dist)
    min_dist_idx = dist.index(min_dist)
    least_path = perms[min_dist_idx]

    max_dist = max(dist)
    max_dist_idx = dist.index(max_dist)
    most_path = perms[max_dist_idx]

    return least_path, min_dist, most_path, max_dist


def run(input):
    data = input.read().splitlines()

    cities = {}
    for line in data:
        city1, _, city2, _, dist = line.split()
        if city1 not in cities.keys():
            cities[city1] = City(city1)
        if city2 not in cities.keys():
            cities[city2] = City(city2)
        cities[city1].add_neighbour(cities[city2], dist)
        cities[city2].add_neighbour(cities[city1], dist)

    least_path, min_dist, most_path, max_dist = brute_force_search(cities)
    print(least_path, min_dist)
    print(most_path, max_dist)
