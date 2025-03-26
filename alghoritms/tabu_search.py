from utils.graph_utils import random_probe, goal_function, generate_neighbours, load_graph_from_file


def tabu_search(num_vertices, edges, max_iterations=100, tabu_size=5):
    """
    Klasyczny algorytm tabu z losowym startem
    :param num_vertices: liczba wierzchołków
    :param edges: lista krawędzi
    :param max_iterations: ilość iteracji, by algorytm nie utknął
    :param tabu_size: rozmiar listy tabu
    :return: najlepsze cięcie
    """
    i = 0
    tabu_list = []

    solution = random_probe(num_vertices)
    cut = goal_function(num_vertices, edges, solution)
    best_solution = solution[:]
    best_cut = cut

    while i < max_iterations:
        neighbours = generate_neighbours(num_vertices, solution)
        neighbour_cut = 0
        move = 0
        neighbour = None

        for n, neigh in enumerate(neighbours):
            neigh_cut = goal_function(num_vertices, edges, neigh)
            if (n not in tabu_list or neigh_cut > best_cut) and neigh_cut > neighbour_cut:
                neighbour_cut = neigh_cut
                neighbour = neigh
                move = n

        if neighbour is None:
            break

        solution = neighbour
        cut = neighbour_cut

        tabu_list.append(move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        if cut > best_cut:
            best_cut = cut
            best_solution = neighbour[:]

        i += 1

    return best_cut, best_solution

num_vertices, edges = load_graph_from_file('../graphs/graph10.txt')
print("------------------------TABU SEARCH------------------------------------")

max_cut, best_solution = tabu_search(num_vertices, edges)
print(f"  Wartość cięcia: {max_cut}")
print(f"  Rozwiązanie: {best_solution}")
print(f"  Weryfikacja: {goal_function(num_vertices, edges, best_solution)}")