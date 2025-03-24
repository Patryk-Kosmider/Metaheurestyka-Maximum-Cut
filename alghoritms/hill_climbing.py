import random

from utils.graph_utils import random_probe, goal_function, generate_neighbours, load_graph_from_file


def hill_climbing_deterministic(num_vertices, edges, max_iterations=100):
    """
    Algorytm wspinaczkowy z deterministycznym wyborem najlepszego sąsiada
    :param num_vertices: liczba wierzchołków
    :param edges: lista krawędzi
    :param max_iterations: ilość iteracji, by algorytm nie utknął
    :return: maksymalne cięcie
    """
    best_neighbour = 0
    best_cut = 0
    solution = random_probe(num_vertices)
    cut = goal_function(num_vertices, edges, solution)

    i = 0

    while i < max_iterations:
        neighbours = generate_neighbours(num_vertices, solution)
        for neighbour in neighbours:
            neighbour_cut = goal_function(num_vertices, edges, neighbour)
            if neighbour_cut > cut:
                print(f"Sąsiad: {neighbour}, max cięcie: {neighbour_cut}")
                best_neighbour = neighbour
                best_cut = neighbour_cut
        if best_neighbour == solution:
            print(f"Znaleziono najlepszego sąsiada")
            break
        print(f"Przechodzimy do kolejnego sąsiada")
        solution = best_neighbour
        cut = best_cut
        i += 1
    return solution, cut, i


num_vertices, edges = load_graph_from_file('../graphs/graph10.txt')

print("------------------------HILL CLIMBING DETERMINISTYCZNY------------------------------------")
solution, cut, i = hill_climbing_deterministic(num_vertices, edges)
print(f"Najlepsze rozwiązanie: {solution}, wartość cięcia: {cut}, ilość iteracji {i}")


def hill_climbing_random(num_vertices, edges, max_iterations=100):
    """
    Algorytm wspinaczkowy z losowym wyborem sasiąda
    :param num_vertices: liczba wierzchołków
    :param edges: lista krawędzi
    :param max_iterations: ilość iteracji, by algorytm nie utknął
    :return: maksymalne cięcie
    """
    best_neighbour = 0
    best_cut = 0
    solution = random_probe(num_vertices)
    cut = goal_function(num_vertices, edges, solution)

    i = 0

    while i < max_iterations:
        neighbours = generate_neighbours(num_vertices, solution)
        neighbour = random.choice(neighbours)
        neighbour_cut = goal_function(num_vertices, edges, neighbour)
        if neighbour_cut > cut:
                print(f"Sąsiad: {neighbour}, max cięcie: {neighbour_cut}")
                best_neighbour = neighbour
                best_cut = neighbour_cut
        if best_neighbour == solution:
            print(f"Znaleziono najlepszego sąsiada")
            break
        print(f"Przechodzimy do kolejnego sąsiada")
        solution = best_neighbour
        cut = best_cut
        i += 1
    return solution, cut, i

print("------------------------HILL CLIMBING LOSOWY------------------------------------")
solutionR, cutR, iR = hill_climbing_random(num_vertices, edges)
print(f"Najlepsze rozwiązanie: {solutionR}, wartość cięcia: {cutR}, ilość iteracji {iR}")