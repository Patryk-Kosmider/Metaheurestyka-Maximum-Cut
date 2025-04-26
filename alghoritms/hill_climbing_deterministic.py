from graph_utils import (
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
    cut = goal_function(edges, solution)
    best_neighbour = solution
    best_cut = cut

    print(f"Punkt startowy: {solution}, cięcie: {cut}")

    print(
        f"\n{'Iteracja':<10} {'Bieżące rozwiązanie':<30} {'Cięcie':<10} {'Najlepszy sąsiad':<30} {'Cięcie sąsiada':<15} {'Akcja':<20}"
    )
    print("-" * 110)

    i = 0
    while i < max_iterations:
        neighbours = generate_neighbours(num_vertices, solution)

        for neighbour in neighbours:
            neighbour_cut = goal_function(edges, neighbour)
            if neighbour_cut > best_cut:
                best_neighbour = neighbour
                best_cut = neighbour_cut

        action = ""
        if best_cut <= cut:
            action = "Optimum lokalne, koniec"
            print(
                f"{i + 1:<10} {str(solution):<30} {cut:<10} {'-':<30} {'-':<15} {action:<20}"
            )
            break
        else:
            action = "Przechodzimy do sąsiada"
            solution = best_neighbour
            cut = best_cut

        print(
            f"{i + 1:<10} {str(solution):<30} {cut:<10} {str(best_neighbour):<30} {best_cut:<15} {action:<20}"
        )

        i += 1

    return solution, cut, i


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hill Climbing Deterministyczny")
    parser.add_argument(
        "--input", type=str, required=True, help="Ścieżka do pliku z grafem"
    )
    parser.add_argument(
        "--max_iterations", type=int, default=100, help="Maksymalna liczba iteracji"
    )

    args = parser.parse_args()

    num_vertices, edges = load_graph_from_file(args.input)

    print(
        "\n------------------------HILL CLIMBING DETERMINISTYCZNY------------------------------------"
    )
    print(f"Parametry: max_iterations={args.max_iterations}\n")

    solution, cut, i = hill_climbing_deterministic(
        num_vertices, edges, args.max_iterations
    )

    print("\nPodsumowanie:")
    print(f"Najlepsze rozwiązanie: {solution}")
    print(f"Wartość cięcia: {cut}")
    print(f"Weryfikacja: {goal_function(edges, solution)}")
    print(f"Liczba wykonanych iteracji: {i}")
