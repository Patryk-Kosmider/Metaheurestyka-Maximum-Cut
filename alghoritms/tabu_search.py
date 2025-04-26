from graph_utils import random_probe, goal_function, load_graph_from_file


def tabu_search(num_vertices, edges, max_iterations=10000, tabu_size=10):
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
    cut = goal_function(edges, solution)

    print(f"Punkt startowy: {solution}, cięcie: {cut}")

    best_solution = solution[:]
    best_cut = cut

    while i < max_iterations:
        print(f"Iteracja {i + 1}:")
        best_neighbour = None
        best_neighbour_cut = -1
        best_move = None

        for vertex in range(num_vertices):
            neighbour = solution.copy()
            neighbour[vertex] = 1 - neighbour[vertex]
            neigh_cut = goal_function(edges, neighbour)

            move = vertex

            if (move not in tabu_list) or (neigh_cut > best_cut):
                if neigh_cut > best_neighbour_cut:
                    best_neighbour = neighbour
                    best_neighbour_cut = neigh_cut
                    best_move = move

        if best_neighbour is None:
            print("Brak dostępnych ruchów, koniec.")
            break

        solution = best_neighbour
        cut = best_neighbour_cut

        tabu_list.append(best_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        print(f"Lista tabu: {tabu_list}")

        if cut > best_cut:
            best_cut = cut
            best_solution = solution[:]
            print(f"Nowe najlepsze rozwiązanie: {best_solution}, cięcie: {best_cut}")

        i += 1

    return best_cut, best_solution


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hill Climbing Losowy")
    parser.add_argument(
        "--input", type=str, required=True, help="Ścieżka do pliku z grafem"
    )
    parser.add_argument(
        "--max_iterations", type=int, default=100, help="Maksymalna liczba iteracji"
    )
    parser.add_argument("--tabu_size", type=int, default=10, help="Rozmiar tabu")
    args = parser.parse_args()

    num_vertices, edges = load_graph_from_file(args.input)

    print("------------------------TABU SEARCH------------------------------------")

    max_cut, best_solution = tabu_search(
        num_vertices, edges, args.max_iterations, args.tabu_size
    )
    print(f"  Wartość cięcia: {max_cut}")
    print(f"  Rozwiązanie: {best_solution}")
    print(f"  Weryfikacja: {goal_function(edges, best_solution)}")
