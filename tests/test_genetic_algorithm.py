"""
Unit tests for Genetic Algorithm operators, convergence, and constraints preservation.
"""

import unittest
from src.data_loader import load_dataset
from src.fitness import FitnessEvaluator
from src.genetic_algorithm import GeneticAlgorithm
from src.models import Build


class TestGeneticAlgorithm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_dataset(base_dir=".")
        cls.evaluator = FitnessEvaluator(cls.registry)

    def setUp(self):
        self.ga = GeneticAlgorithm(
            registry=self.registry,
            evaluator=self.evaluator,
            population_size=30,
            mutation_rate=0.7,
            generations=25,
            seed=42,
        )

    def test_random_build_generation_is_always_valid(self):
        for _ in range(50):
            build = self.ga._generate_valid_random_build()
            self.assertTrue(build.is_valid(self.registry.relics))

    def test_repair_operator_fixes_invalid_chromosomes(self):
        # Unstackable relic repeated 3 times
        invalid_genes = [
            "The Loose Cannon's Payload",
            "The Loose Cannon's Payload",
            "The Loose Cannon's Payload",
        ]
        repaired = self.ga._repair_build(invalid_genes)
        repaired_build = Build(relics=repaired)
        self.assertTrue(repaired_build.is_valid(self.registry.relics))

    def test_crossover_produces_valid_offspring(self):
        parent1 = Build(
            relics=(
                "The Loose Cannon's Payload",
                "Luden's Tempest",
                "The Scourge Stash",
            )
        )
        parent2 = Build(
            relics=(
                "The Loose Cannon's Payload",
                "Chosen by the Stars",
                "Lost Chapter",
            )
        )
        # Even though both parents have Payload (unstackable), crossover should repair
        for _ in range(20):
            c1, c2 = self.ga._crossover(parent1, parent2)
            self.assertTrue(c1.is_valid(self.registry.relics))
            self.assertTrue(c2.is_valid(self.registry.relics))

    def test_mutation_preserves_validity(self):
        build = Build(
            relics=(
                "The Loose Cannon's Payload",
                "Luden's Tempest",
                "Lost Chapter",
            )
        )
        for _ in range(30):
            mutated = self.ga._mutate(build)
            self.assertTrue(mutated.is_valid(self.registry.relics))

    def test_ga_runs_and_converges(self):
        pop = self.ga.run(champion_name="Jinx", star_power=3)
        self.assertEqual(len(pop), 30)

        # Check that fitness improved or remained high
        initial_best = self.ga.history_best_fitness[0]
        final_best = self.ga.history_best_fitness[-1]
        self.assertGreaterEqual(final_best, initial_best)

        # Best individual must be valid
        best_build = pop[0]
        self.assertTrue(best_build.is_valid(self.registry.relics))
        self.assertGreater(best_build.fitness, 0.0)

    def test_top_k_distinct_filters_duplicates(self):
        pop = self.ga.run(champion_name="Yasuo", star_power=3)
        top_k = self.ga.get_top_k_distinct(pop, k=3)

        self.assertLessEqual(len(top_k), 3)
        seen_keys = set()
        for b in top_k:
            key = tuple(sorted(b.relics))
            self.assertNotIn(key, seen_keys)
            seen_keys.add(key)


if __name__ == "__main__":
    unittest.main()
