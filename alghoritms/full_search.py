from utils.graph_utils import generate_all_solutions, goal_function, load_graph_from_file


def full_search(num_vertices, edges):
    """
    Algorytm pełnego przeglądu - generacja wszystkich rozwiązań, obliczenie kosztu, wybranie najlepszej opcji
    :param num_vertices: : liczba wierzchołków
    :param edges: lista krawędzi
    :return: maksymalne cięcie
    """

    best_cut = 0
    best_solution = 0

    all_solutions = generate_all_solutions(num_vertices)
    for solution in all_solutions:
        current_cut = goal_function(edges, solution)
        print(f"Rozwiązanie: {solution}, max cięce: {current_cut}")
        if current_cut > best_cut:
            best_cut = current_cut
            best_solution = solution
    return best_solution, best_cut


num_vertices, edges = load_graph_from_file('../graphs/graph10.txt')

print("------------------------ALGORYTM PEŁNEGO PRZEGLĄDU------------------------------------")
best_solution, best_cut = full_search(num_vertices, edges)
print(f"Najlepsze rozwiązanie: {best_solution}, wartość cięcia: {best_cut}")

