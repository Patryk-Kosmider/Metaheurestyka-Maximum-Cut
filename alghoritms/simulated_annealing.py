import random
import math
from graph_utils import (
    load_graph_from_file,
    random_probe,
    goal_function,
    generate_neighbours,
)


# Harmonogram chłodzenia (geometryczny)
def T(k, T0, alpha):
    return T0 * (alpha**k)


def sim_annealing(num_vertices, edges, max_iterations, T, T0, alpha):
    """
       Algorytm symulowanego wyzarzania, z geometrycznym harmnogramem chłodzenia.
       :param num_vertices: liczba wierzchołków
       :param edges: lista krawędzi
       :param max_iterations: ilość iteracji, by algorytm nie utknął
       :param T: temperatura z harmonogramu chłodzenia
       :param T0: temparatura początkowa
       :param alpha: współczynnik alfa (0 < alpha < 1)
       :return: maksymalne cięcie
    """
    s = random_probe(num_vertices)

    V = [s]
    best_s = s
    best_value = goal_function(edges, s)

    print(
        f"{'Iteracja':<10} {'Temperatura':<15} {'Bieżące rozwiązanie':<30} {'Cięcie':<10} {'Sąsiad':<30} {'Cięcie sąsiada':<15} {'Akcja':<20}"
    )
    print("-" * 110)

    for k in range(1, max_iterations):
        temp = T(k, T0, alpha)

        neighbours = generate_neighbours(num_vertices, s)
        t = random.choice(neighbours)

        current_value = goal_function(edges, s)
        new_value = goal_function(edges, t)

        action = ""

        if new_value >= current_value:
            action = "Przechodzimy (lepszy/równy)"
            s = t
        else:
            delta = new_value - current_value
            prob = math.exp(delta / temp)
            action = f"Gorszy (delta={delta}, prob={prob:.4f})"
            if random.random() < prob:
                action += " -> Akceptujemy"
                s = t
            else:
                action += " -> Odrzucamy"

        current_value = goal_function(edges, s)
        if current_value > best_value:
            best_value = current_value
            best_s = s[:]

        print(
            f"{k:<10} {temp:<15.2f} {str(s):<30} {current_value:<10} {str(t):<30} {new_value:<15} {action:<20}"
        )

        V.append(s)

    return (
        best_s,
        best_value,
        V,
        [goal_function(edges, e) for e in V],
        s,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simulated Annealing")
    parser.add_argument(
        "--input", type=str, required=True, help="Ścieżka do pliku z grafem"
    )
    parser.add_argument("--max_iterations", type=int, default=100, help="Maksymalna liczba iteracji")
    parser.add_argument(
        "--T0", type=float, required=True, help="Początkowa temperatura (T0)"
    )
    parser.add_argument(
        "--alpha",
        type=float,
        required=True,
        help="Współczynnik chłodzenia (alpha, 0 < alpha < 1)",
    )

    args = parser.parse_args()

    num_vertices, edges = load_graph_from_file(args.input)

    print(
        "\n------------------------SIMULATED ANNEALING------------------------------------"
    )
    print(
        f"Początkowa temperatura (T0): {args.T0}, współczynnik chłodzenia (alpha): {args.alpha}\n"
    )

    best_solution, best_cut, points, cuts, start_point = sim_annealing(
        num_vertices, edges, args.max_iterations, T, args.T0, args.alpha
    )

    start_cut = goal_function(edges, start_point)
    print("\nPodsumowanie:")
    print(f"Punkt startowy: {start_point}, cięcie: {start_cut}")
    print(f"Najlepsze rozwiązanie: {best_solution}, cięcie: {best_cut}")
    print(f"Weryfikacja: {goal_function(edges, best_solution)}")
    print(f"Ostatnie rozwiązanie: {points[-1]}, cięcie: {cuts[-1]}")
    print(f"Liczba odwiedzonych rozwiązań: {len(points)}")
