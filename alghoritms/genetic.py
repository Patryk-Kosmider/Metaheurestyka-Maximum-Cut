import random
import argparse
from graph_utils import load_graph_from_file, random_probe, goal_function


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
    for i in range(len(parent1)):
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
    for i in range(len(mutated)):
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
    crossover_type,
    mutation_type,
    stop_condition,
    max_generations=100,
    population_size=50,
    mutation_rate=0.2,
    mutation_multiple_rate=0.2,
    crossover_rate=0.5,
    max_no_improvement=20,
):
    population = [random_probe(num_vertices) for _ in range(population_size)]
    best_solution = max(population, key=lambda x: goal_function(edges, x))
    best_value = goal_function(edges, best_solution)
    no_improvement = 0

    print(f"{'Generacja':<10} {'Najlepsze cięcie':<20} {'Najlepsze rozwiązanie':<40}")
    print("-" * 110)

    for generation in range(max_generations):

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

        population = new_population[:population_size]

        current_best_solution = max(population, key=lambda x: goal_function(edges, x))
        current_best_value = goal_function(edges, current_best_solution)

        print(f"{generation:<10} {current_best_value:<20} {str(current_best_solution):<40}")


        if current_best_value > best_value:
            best_value = current_best_value
            best_solution = current_best_solution
            no_improvement = 0
        else:
            no_improvement += 1

        # Warunek zakończenia
        if stop_condition == "max_generations":
            if generation + 1 >= max_generations:
                print(f"Osiągnieto maksymalna ilość generacji, algorytm kończy działanie: {max_generations}")
                break
        elif stop_condition == "max_no_improvement":
            if no_improvement >= max_no_improvement:
                print(f"Osiągnieto maksymalną ilość generacji {no_improvement} bez poprawy, algorytm kończy działanie")
                break
        else:
            if generation + 1 >= max_generations:
                break

    return best_value, best_solution, generation, population


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorytm genetyczny")
    parser.add_argument("--input", type=str, required=True, help="Ściężka do pliku z grafem")
    parser.add_argument(
        "--crossover_type",
        type=str,
        choices=["onepoint", "uniform"],
        required=True,
        help="Metoda krzyżowania",
    )
    parser.add_argument(
        "--mutation_type",
        type=str,
        choices=["onepoint", "multiplepoint"],
        required=True,
        help="Metoda mutacji",
    )
    parser.add_argument(
        "--stop_condition",
        type=str,
        choices=["max_generations", "max_no_improvement"],
        required=True,
        help="Warunek zakończenia działania",
    )
    parser.add_argument(
        "--max_generations",
        type=int,
        default=100,
        help="Maksymalna ilość generacji",
    )
    parser.add_argument(
        "--max_generations_no_improvement",
        type=int,
        default=20,
        help="Maksymalna ilość generacji bez poprawy",
    )
    parser.add_argument(
        "--population_size",
        type=int,
        default=50,
        help="Rozmiar populacji"
    )

    args = parser.parse_args()

    num_vertices, edges = load_graph_from_file(args.input)

    print("\n--- Algorytm genetyczny ---")
    print(
        f"Metoda krzyżowania: {args.crossover_type}\n"
        f"Metoda mutacji: {args.mutation_type}\n"
        f"Warunek zakończenia działania: {args.stop_condition}\n"
        f"Maksymalna ilość generacji: 100\n"
        f"Rozmiar populacji: 50\n"
        f"Mutation rate: 0.2\n"
        f"Multiple mutation rate: 0.2\n"
        f"Crossover uniform rate: 0.5\n"
        f"Max no improvement generations: 20\n"
    )

    best_value, best_solution, generation, population = genetic_algorithm(
        num_vertices,
        edges,
        crossover_type=args.crossover_type,
        mutation_type=args.mutation_type,
        stop_condition=args.stop_condition,
        max_generations=args.max_generations,
        population_size=args.population_size,
        mutation_rate=0.2,
        mutation_multiple_rate=0.2,
        crossover_rate=0.5,
        max_no_improvement=args.max_generations_no_improvement,
    )

    start_point = population[0]
    start_cut = goal_function(edges, start_point)

    print("\nPodsumowanie:")
    print(f"Punkt startowy: {start_point}, cięcie: {start_cut}")
    print(f"Najlepsze rozwiązanie: {best_solution}, cięcie: {best_value}")
    print(f"Weryfikacja: {goal_function(edges, best_solution)}")
    print(f"Ilość generacji: {generation + 1}")
    print(f"Odwiedzono rozwiązań: {(generation + 1) * 50}")