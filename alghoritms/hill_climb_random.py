import random
from graph_utils import (
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
    cut = goal_function(edges, solution)
    print(f"Punkt startowy: {solution}, cięcie: {cut}")

    print(
        f"\n{'Iteracja':<10} {'Bieżące rozwiązanie':<30} {'Cięcie':<10} {'Losowy sąsiad':<30} {'Cięcie sąsiada':<15} {'Akcja':<20}"
    )
    print("-" * 110)

    i = 0
    while i < max_iterations:
        neighbours = generate_neighbours(num_vertices, solution)
        neighbour = random.choice(neighbours)
        neighbour_cut = goal_function(edges, neighbour)

        action = ""
        if neighbour_cut > cut:
            solution = neighbour
            cut = neighbour_cut
            action = "Przechodzimy do sąsiada"
        else:
            action = "Brak lepszego sąsiada"

        print(
            f"{i + 1:<10} {str(solution):<30} {cut:<10} {str(neighbour):<30} {neighbour_cut:<15} {action:<20}"
        )

        i += 1

    return solution, cut, i


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hill Climbing Losowy")
    parser.add_argument(
        "--input", type=str, required=True, help="Ścieżka do pliku z grafem"
    )
    parser.add_argument(
        "--max_iterations", type=int, default=100, help="Maksymalna liczba iteracji"
    )

    args = parser.parse_args()

    num_vertices, edges = load_graph_from_file(args.input)

    print(
        "\n------------------------HILL CLIMBING LOSOWY------------------------------------"
    )
    print(f"Parametry: max_iterations={args.max_iterations}\n")

    solutionR, cutR, iR = hill_climbing_random(num_vertices, edges, args.max_iterations)

    print("\nPodsumowanie:")
    print(f"Najlepsze rozwiązanie: {solutionR}")
    print(f"Wartość cięcia: {cutR}")
    print(f"Weryfikacja: {goal_function(edges, solutionR)}")
    print(f"Liczba wykonanych iteracji: {iR}")
