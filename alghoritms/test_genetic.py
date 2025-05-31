import pytest
import random
from alghoritms.genetic import crossover_onepoint_random, crossover_uniform, mutate_onepoint, mutate_multiplepoint, \
    selection_tournament
from alghoritms.graph_utils import goal_function

EDGES = [
    (0, 1, 2),
    (0, 2, 5),
    (1, 3, 7),
    (1, 4, 1),
]

NUM_VERTICES = 5

class TestGenetic:
    @classmethod
    def setUp(cls):
        random.seed(1)
    @pytest.mark.parametrize(
        "parent1, parent2",
        [
            ([0,0,0,0,0], [1,1,1,1,1]),
            ([1,0,1,0,1], [0,1,0,1,0]),
            ([0,1,0,1,0], [1,0,1,0,1]),
        ]
    )
    def test_crossover_uniform(self, parent1, parent2):

        """
        Krzyzowanie uniform wykonuje się z podanym 0.5 p.p, jest szansa że nie dojdzie do krzyżowania!
        Test steps:
        1. Krzyżowanie uniform na dwóch rodzicach
        2. Sprawdź czy długość dzieic jest odpowiednia
        3. Sprawdź czy geny dzieci to 0/1
        4. Sprawdź czy dzieci róznią się od rodziców
        :return:
        """
        child1, child2 = crossover_uniform(parent1, parent2)
        after_crossover = (child1 != parent1) or (child2 != parent2)
        assert len(child1) == len(parent1)
        assert len(child2) == len(parent2)
        assert all(gene in [0, 1] for gene in child1)
        assert all(gene in [0, 1] for gene in child2)
        assert after_crossover

    @pytest.mark.parametrize(
        "parent1, parent2",
        [
            ([0, 1, 0, 1, 0], [1, 0, 1, 0, 1]),
            ([1, 1, 1, 1, 1], [0, 0, 0, 0, 0]),
            ([0, 0, 1, 1, 0], [1, 1, 0, 0, 1]),
        ]
    )
    def test_crossover_onepoint(self, parent1, parent2):
        """
        Test steps:
        1. Krzyżowanie jednopunktowe na dwóch rodzicach
        2. Sprawdź czy długość dzieic jest odpowiednia
        3. Sprawdź czy geny dzieci to 0/1
        4. Sprawdź czy dzieci róznią się od rodziców
        :return:
        """
        child1, child2 = crossover_onepoint_random(parent1, parent2)
        after_crossover = (child1 != parent1) or (child2 != parent2)
        assert len(child1) == len(parent1)
        assert len(child2) == len(parent2)
        assert all(gene in [0, 1] for gene in child1)
        assert all(gene in [0, 1] for gene in child2)
        assert after_crossover

    @pytest.mark.parametrize(
        "solution",
        [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 1],
        ]
    )
    def test_mutation_onepoint(self, solution):
        """
        Test steps:
        1. Mutacja jednopunktowa na rozwiązaniu
        2. Sprawdź dlugość po mutacji
        3. Sprawdź czy geny po mutacji to 0/1
        4. Sprawdź czy gen po mutacji się róźni
        :return:
        """
        mutated = mutate_onepoint(solution)
        assert len(mutated) == len(solution)
        assert all(gene in [0, 1] for gene in mutated)
        after_mutation = (mutated != solution)
        assert after_mutation

    @pytest.mark.parametrize(
        "solution",
        [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 1],
        ]
    )
    def test_mutation_multiplepoint(self, solution):
        """
        Test steps:
        Mutacja wielopunktowa wykonuje się z podanym 0.2 p.p, jest szansa że nie dojdzie do mutacji!
        1. Mutacja wielopunktowa na rozwiązaniu
        2. Sprawdź dlugość po mutacji
        3. Sprawdź czy geny po mutacji to 0/1
        4. Sprawdź czy gen po mutacji się róźni
        :return:
        """
        mutated = mutate_multiplepoint(solution)
        assert len(mutated) == len(solution)
        assert all(gene in [0, 1] for gene in mutated)
        after_mutation = (mutated != solution)
        assert after_mutation

    @pytest.mark.parametrize(
        "population, edges, k",
        [
            (
                [[0,0,0], [1,0,0], [1,1,0], [1,1,1]],
                [(0,1,2), (1,2,3), (2,3,4)],
                2
            ),
            (
                [[1,0,1,0], [0,1,0,1], [1,1,0,0], [0,0,1,1], [1,1,1,1]],
                [(0,1,1), (1,2,2), (2,3,3), (3,4,4)],
                3
            ),
            (
                [[0,0], [1,1], [0,1], [1,0]],
                [(0,1,5)],
                4
            ),
        ]
    )
    def test_tournament_selection(self, population, edges, k):
        """
        Test steps:
        1. Selekcja turniejowa na podanej populacji
        2. Odtworz krok wybrania losowego grona.
        3. Wybierz najlepszego osobnika z listy.
        4. Sprawdź czy selekcja zwróciła tego samego osobnika.
        :return:
        """
        winner = selection_tournament(population, edges, k)
        selected = random.sample(population, k)
        best = max(selected, key=lambda x: goal_function(edges, x))
        assert winner in selected
        assert winner == best
