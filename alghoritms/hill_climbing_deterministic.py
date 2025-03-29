import random

from utils.graph_utils import (
    random_probe,
    goal_function,
    generate_neighbours,
    load_graph_from_file,
)


def hill_climbing_deterministic(num_vertices, edges, max_iterations=100):
    """
    Algorytm wspinaczkowy z deterministycznym wyborem najlepszego sąsiada
    :param num_vertices: liczba wierzchołków
    :param edges: lista krawędzi
    :param max_iterations: ilość iteracji, by algorytm nie utknął
    :return: maksymalne cięcie
    """

    solution = random_probe(num_vertices)
    cut = goal_function(num_vertices, edges, solution)
    best_neighbour = solution
    best_cut = cut

    print(f"Punkt startowy: {solution}, cięcie: {cut}")

    i = 0

    while i < max_iterations:
        print(f"Iteracja {i+1}:")
        neighbours = generate_neighbours(num_vertices, solution)
        print(f"Sasiędzi: {neighbours}")
        for neighbour in neighbours:
            neighbour_cut = goal_function(num_vertices, edges, neighbour)
            print(f"Sąsiad: {neighbour}, max cięcie: {neighbour_cut}")
            if neighbour_cut > cut:
                best_neighbour = neighbour
                best_cut = neighbour_cut
        if best_cut <= cut:
            print(f"Brak lepszego sasiąda - optimum lokalne")
            break
        print(f"Przechodzimy do {best_neighbour}, cięcie: {best_cut}")
        solution = best_neighbour
        cut = best_cut
        i += 1
    return solution, cut, i


num_vertices, edges = load_graph_from_file("../graphs/graph10.txt")

print(
    "------------------------HILL CLIMBING DETERMINISTYCZNY------------------------------------"
)
solution, cut, i = hill_climbing_deterministic(num_vertices, edges)
print(f"Najlepsze rozwiązanie: {solution}, wartość cięcia: {cut}, ilość iteracji {i}")

