from graph_utils import random_probe, goal_function, load_graph_from_file, generate_neighbours,back_to_work_point


def tabu_search(num_vertices, edges, max_iterations=10000, tabu_size=10, history_size=10):
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
    history = []

    solution = random_probe(num_vertices)
    cut = goal_function(edges, solution)
    print(f"Punkt startowy: {solution}, cięcie: {cut}")

    best_solution = solution[:]
    best_cut = cut

    print(
        f"\n{'Iteracja':<10} {'Bieżące rozwiązanie':<30} {'Cięcie':<10} {'Najlepszy sąsiad':<30} {'Cięcie sąsiada':<15} {'Ruch':<10} {'Lista tabu':<20} {'Akcja':<20}"
    )
    print("-" * 120)

    while i < max_iterations:
        best_neighbour = None
        best_neighbour_cut = -1
        best_move = None
        available_work_points = []

        neighbours = generate_neighbours(num_vertices, solution)

        for neighbour in neighbours:
            neigh_cut = goal_function(edges, neighbour)

            if neighbour not in tabu_list or neigh_cut > best_cut:
                if neigh_cut > best_neighbour_cut:
                    best_neighbour = neighbour
                    best_neighbour_cut = neigh_cut
                    best_move = neighbour

                available_work_points.append((neighbour, neigh_cut))

        if best_neighbour is None:
            get_from_history = back_to_work_point(history, edges, tabu_list)
            if get_from_history:
                solution = get_from_history["solution"]
                cut = get_from_history["cut"]
                print(
                    f"{i + 1:<10} {str(solution):<30} {cut:<10} {'-':<30} {'-':<15} {'-':<10} {str(tabu_list):<20} Cofnięce do punktu roboczego: {solution} / {cut}"
                )
                continue
            else:
                print(
                    f"{i + 1:<10} {str(solution):<30} {cut:<10} {'-':<30} {'-':<15} {'-':<10} {str(tabu_list):<20} Brak dostępnych ruchów"
                )
            break

        history.append({"solution": solution[:], "cut": cut})
        if len(history) > history_size:
            history.pop(0)

        solution = best_neighbour
        cut = best_neighbour_cut

        tabu_list.append(best_neighbour)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        action = ""
        if cut > best_cut:
            best_cut = cut
            best_solution = solution[:]
            action = "Nowy najlepszy wynik"

        print(
            f"{i + 1:<10} {str(solution):<30} {cut:<10} {str(best_neighbour):<30} {best_neighbour_cut:<15} {str(best_move):<10} {str(tabu_list):<20} {action:<20}"
        )

        i += 1

    return best_cut, best_solution


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Tabu Search for Maximum Cut problem")
    parser.add_argument(
        "--input", type=str, required=True, help="Ścieżka do pliku z grafem"
    )
    parser.add_argument(
        "--max_iterations", type=int, default=100, help="Maksymalna liczba iteracji"
    )
    parser.add_argument("--tabu_size", type=int, default=10, help="Rozmiar tabu")

    args = parser.parse_args()

    num_vertices, edges = load_graph_from_file(args.input)

    print("\n------------------------TABU SEARCH------------------------------------")
    print(
        f"Parametry: max_iterations={args.max_iterations}, tabu_size={args.tabu_size}\n"
    )

    max_cut, best_solution = tabu_search(
        num_vertices, edges, args.max_iterations, args.tabu_size
    )

    print("\nPodsumowanie:")
    print(f"Wartość cięcia: {max_cut}")
    print(f"Najlepsze rozwiązanie: {best_solution}")

