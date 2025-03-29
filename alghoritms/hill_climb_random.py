import random

from utils.graph_utils import (
    random_probe,
    goal_function,
    generate_neighbours,
    load_graph_from_file,
)

def hill_climbing_random(num_vertices, edges, max_iterations=100):
    """
    Algorytm wspinaczkowy z losowym wyborem sasiąda
    :param num_vertices: liczba wierzchołków
    :param edges: lista krawędzi
    :param max_iterations: ilość iteracji, by algorytm nie utknął
    :return: maksymalne cięcie
    """
    solution = random_probe(num_vertices)
    cut = goal_function(num_vertices, edges, solution)

    print(f"Punkt startowy: {solution}, cięcie: {cut}")

    i = 0

    while i < max_iterations:
        print(f"Iteracja {i+1}:")
        neighbours = generate_neighbours(num_vertices, solution)
        neighbour = random.choice(neighbours)
        neighbour_cut = goal_function(num_vertices, edges, neighbour)

        print(f"Losowy sąsiad: {neighbour}, cięcie: {neighbour_cut}")

        if neighbour_cut > cut:
            solution = neighbour
            cut = neighbour_cut
            print(f"Przechodzimy do {solution}, cięcie: {cut}")
        else:
            print("Brak lepszego sasiąda - szukamy dalej")

        i += 1
    return solution, cut, i

num_vertices, edges = load_graph_from_file("../graphs/graph10.txt")

print(
    "------------------------HILL CLIMBING LOSOWY------------------------------------"
)
solutionR, cutR, iR = hill_climbing_random(num_vertices, edges)
print(
    f"Najlepsze rozwiązanie: {solutionR}, wartość cięcia: {cutR}, ilość iteracji {iR}"
)