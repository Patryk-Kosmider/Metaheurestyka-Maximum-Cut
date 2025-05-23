import itertools
import random


def load_graph_from_file(file):
    """
    Wczytywanie grafu z pliku tekstowego
    :param file: plik tekstowy
    :return: liczba wierzchołków, lista krawędzi
    """
    edges = []
    with open(file, "r") as f:
        lines = f.readlines()
        num_vertices = int(lines[0].strip())
        for line in lines[1:]:
            if line.strip():
                src, dest, weight = map(int, line.strip().split())
                edges.append((src, dest, weight))
    print(f"Liczba wierzchołków: {num_vertices}")
    print(f"Krawędzie: {edges}")
    return num_vertices, edges


def random_probe(num_vertices):
    """
    Generujemy losowy podział wierzchołków na dwa zbiory
    :param num_vertices: liczba wierzchołków
    :return: lista zawierająca losowy podział wierzchołków [0 / 1 dla każdego wierzchołka]
    """
    random_probe_list = []
    for _ in range(num_vertices):
        random_probe_list.append(random.randint(0, 1))
    return random_probe_list


def goal_function(edges, random_probe_list):
    """
    Funkcja celu -> celem jest uzyskanie maksymalnej sumy wag krawędzi przeciętych
    przez podział wierzchołków na dwa zbiory
    :param edges: lista krawędzi
    :param random_probe_list: losowo wygenerowana lista z random_probe()
    :return: suma wag przeciętych krawędzi
    """
    cut = 0
    seen = set()

    for src, dest, weight in edges:
        if (src, dest) not in seen and (dest, src) not in seen:
            if random_probe_list[src] != random_probe_list[dest]:
                cut += weight
            seen.add((src, dest))
            seen.add((dest, src))

    return cut


def generate_neighbours(num_vertices, random_probe_list):
    """
    Tworzymy sasiądów, wszystkie możliwe rozwiązania - rózniącę się od siebie jednym wierzchołkiem
    :param num_vertices: liczba wierzchołków
    :param random_probe_list: losowo wygenerowana lista z random_probe()
    :return: lista wszystkich możliwych rozwiązań
    """

    neighbours = []
    for i in range(num_vertices):
        neighbour = random_probe_list.copy()
        neighbour[i] = 1 - neighbour[i]
        neighbours.append(neighbour)

    return neighbours


def generate_all_solutions(num_vertices):
    """
    Generujemy WSZYSTKIE możliwe kombinacje podziałów wierzchołków
    :param num_vertices: liczba wierzchołków
    :return: lista wszystkich możliwych rozwiązań
    """
    all_solutions = []
    for solution in itertools.product([0, 1], repeat=num_vertices):
        all_solutions.append(list(solution))
    return all_solutions
