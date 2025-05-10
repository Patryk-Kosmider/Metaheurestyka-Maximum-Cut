import random
from graph_utils import (
    load_graph_from_file,
    random_probe,
    goal_function,
)


# Krzyzowanie jednopunktowe -> zamiana fragementow miedzy rodzicami z losowym wyborem punktu podzialu


def crossover_onepoint_random(parent1, parent2):
    """
    :param parent1: Pierwszy rodzic
    :param parent2: Drugi rodzic
    :return: Zwraca jedno i drugie dziecko, powstale w wyniku zamiany wzgledem ustalonego punktu
    """
    cross_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:cross_point] + parent2[cross_point:]
    child2 = parent2[:cross_point] + parent1[cross_point:]
    return child1, child2


# Krzyzowanie uniform -> kazdy gen jest losowo wybierany sposrod rodzicow z okreslonym prawdopodobienstwem


def crossover_uniform(parent1, parent2, crossover_rate=0.5):
    """
    :param parent1: Pierwszy rodzic
    :param parent2: Drugi rodzic
    :param crossover_rate: Prawdopodobienstwo zamiany
    :return: Zwraca jedno i drugie dziecko, powstale w wyniku wymieszania genow miedzy rodzicami
    """
    child1, child2 = [], []
    for i in range(0, len(parent1)):
        if random.random() < crossover_rate:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    return child1, child2


# Mutacja flip -> odwracamy jeden wierzcholek
def mutate_onepoint(solution):
    """
    :param solution: Lista wierzcholkow w formacie 0-1
    :return: Lista z odwroconym jednym wierzcholkiem, wybranym w losowy sposob
    """
    mutated = solution[:]
    i = random.randint(0, len(solution) - 1)
    mutated[i] = 1 - mutated[i]
    return mutated


# Mutacja multiple flip -> odwracanie wielu bitow, z prawodopodobienstwem, ze to sie wykona


def mutate_multiplepoint(solution, mutation_rate=0.2):
    """
    :param solution: Lista wierzcholkow formacie 0-1
    :param mutation_rate: Prawdopodobienstwo zamiany
    :return: Lista z odwroconymi wierzcholkami
    """
    mutated = solution[:]
    for i in range(0, len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = 1 - mutated[i]
    return mutated


# Tournament selection -> chyba najlepszy wybor, duza rodnorodnosc, bo u nas grupy wierzcholkow maja wyrazne roznice w funkcji celu, oraz dobre wyniki dla duzych problemow


def selection_tournament(population, edges, k=3):
    """
    :param population: Lista zawieracja rozwiazanie powstale w aktualnej generacji algorytmu
    :param edges: lista krawędzi
    :param k: Ile rozwiazan zostanie wybranych do turnieju
    :return: Rozwiazanie z najlepsza funkcja celu
    """
    selected = random.sample(population, k)
    selected.sort(key=lambda x: goal_function(edges, x), reverse=True)
    return selected[0]


def genetic_algorithm(
    num_vertices,
    edges,
    max_generations,
    population_size,
    mutation_rate,
    mutation_multiple_rate,
    crossover_rate,
    mutation_type,
    crossover_type,
    max_no_improvement,
    elite_size,
):
    population = [random_probe(num_vertices) for _ in range(population_size)]
    best_solution = max(population, key=lambda x: goal_function(edges, x))
    best_value = goal_function(edges, best_solution)
    no_improvement = 0

    current_best_solution = None
    current_best_value = 0

    print(
        f"{'Pokolenie': <10} {'Najlepsze cięcie': <20} {'Najlepsze rozwiązanie': <40}"
    )
    print("-" * 110)

    for generation in range(max_generations):

        if elite_size > 0:
            # Elita włączona -> zapisuje najlepsze wyniki
            elite = sorted(
                population, key=lambda x: goal_function(edges, x), reverse=True
            )[:elite_size]

        new_population = []
        while len(new_population) < population_size:
            parent1 = selection_tournament(population, edges)
            parent2 = selection_tournament(population, edges)

            if crossover_type == "onepoint":
                child1, child2 = crossover_onepoint_random(parent1, parent2)
            else:
                child1, child2 = crossover_uniform(parent1, parent2, crossover_rate)

            if random.random() < mutation_rate:
                child1 = (
                    mutate_onepoint(child1)
                    if mutation_type == "onepoint"
                    else mutate_multiplepoint(child1, mutation_multiple_rate)
                )
            if random.random() < mutation_rate:
                child2 = (
                    mutate_onepoint(child2)
                    if mutation_type == "onepoint"
                    else mutate_multiplepoint(child2, mutation_multiple_rate)
                )

            new_population.extend([child1, child2])

        population = new_population[: population_size - elite_size] + elite

        current_best_solution = max(population, key=lambda x: goal_function(edges, x))
        current_best_value = goal_function(edges, current_best_solution)

        print(
            f"{generation:<10} {current_best_value:<20} {str(current_best_solution):<40}"
        )

        if current_best_value > best_value:
            best_value = current_best_value
            best_solution = current_best_solution
        else:
            no_improvement += 1

        if no_improvement >= max_no_improvement:
            print(
                f"Brak poprawy od {no_improvement} generacji - algorytm przerywa pracę"
            )
            break

    return best_value, best_solution, generation, population


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Algorytm genetyczny")
    parser.add_argument(
        "--input", type=str, required=True, help="Ścieżka do pliku z grafem"
    )
    parser.add_argument(
        "--max_generations", type=int, default=100, help="Maksymalna liczba iteracji"
    )
    parser.add_argument(
        "--population_size", type=int, default=50, help="Maksymalna liczba pokoleń"
    )
    parser.add_argument(
        "--mutation_rate", type=float, default=0.2, help="Prawdopodobienstwo mutacji"
    )
    parser.add_argument(
        "--mutation_multiple_rate",
        type=float,
        default=0.2,
        help="Prawdopodobienstwo dokonania zamiany w mutacji multiple points",
    )
    parser.add_argument(
        "--crossover_rate",
        type=float,
        default=0.2,
        help="Prawdopodobienstwo dokonania zamiany w krzyzowaniu uniform",
    )
    parser.add_argument(
        "--mutation_type",
        type=str,
        required=True,
        choices=["onepoint", "multiplepoint"],
        help="Typ mutacji",
    )
    parser.add_argument(
        "--crossover_type",
        type=str,
        required=True,
        choices=["onepoint", "uniform"],
        help="Typ krzyżowania",
    )
    parser.add_argument(
        "--max_no_improvement",
        type=int,
        default=20,
        help="Maksymalna liczba pokoleń bez poprawy",
    )
    parser.add_argument(
        "--elite_size",
        type=int,
        default=0,
        help="Ilosc elity, najlepszych rozwiazan do przechowania",
    )

    args = parser.parse_args()
    num_vertices, edges = load_graph_from_file(args.input)

    print(
        "\n------------------------GENETYCZNY ALGORYTM------------------------------------"
    )
    print(
        f"Wybrany typ mutacji: {args.mutation_type}, typ krzyzowania: {args.crossover_type}\n"
        f"Ustalono: \n"
        f" -Maksymalną ilość generacji: {args.max_generations}\n"
        f" -Rozmiar populacji: {args.population_size}\n"
        f" -Dopuszczalna ilość pokoleń bez poprawy: {args.max_no_improvement}\n"
        f" -Prawdopodobieństwo dokonania mutacji: {args.mutation_rate}\n"
        f" -Prawdopodobieństwo dokonania zmiany dla uniform krzyzowania (jeśli wybrano): {args.crossover_rate}\n"
        f" -Prawdopodobieństwo dokonania zmiany dla mutacji multiplepoint (jeśli wybrano): {args.mutation_multiple_rate}\n"
        f" -Elita: {args.elite_size}"
    )

    best_value, best_solution, generation, population = genetic_algorithm(
        num_vertices,
        edges,
        args.max_generations,
        args.population_size,
        args.mutation_rate,
        args.mutation_multiple_rate,
        args.crossover_rate,
        args.mutation_type,
        args.crossover_type,
        args.max_no_improvement,
        args.elite_size,
    )

    start_point = population[0]
    start_cut = goal_function(edges, start_point)

    print("\nPODSUMOWANIE:")
    print(f"Punkt startowy: {start_point}, cięcie: {start_cut}")
    print(f"Najlepsze rozwiązanie: {best_solution}, cięcie: {best_value}")
    print(f"Weryfikacja funkcji celu: {goal_function(edges, best_solution)}")
    print(f"Liczba pokoleń: {generation + 1}")
    print(f"Liczba odwiedzonych rozwiązań: {(generation + 1) * args.population_size}")
