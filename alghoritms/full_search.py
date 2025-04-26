from graph_utils import generate_all_solutions, goal_function, load_graph_from_file


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


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Full search algorithm")
    parser.add_argument(
        "--input", type=str, required=True, help="Ścieżka do pliku z grafem"
    )

    args = parser.parse_args()

    num_vertices, edges = load_graph_from_file(args.input)

    print(
        "------------------------ALGORYTM PEŁNEGO PRZEGLĄDU------------------------------------"
    )
    best_solution, best_cut = full_search(num_vertices, edges)
    print(f"Najlepsze rozwiązanie: {best_solution}, wartość cięcia: {best_cut}")
