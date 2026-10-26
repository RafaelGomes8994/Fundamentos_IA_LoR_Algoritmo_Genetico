"""
Unit tests for the Exact Search benchmark and GA comparison.
"""

import unittest
from src.data_loader import load_dataset
from src.fitness import FitnessEvaluator
from src.comparison import ExactSearchOptimizer, compare_ga_vs_exact
from src.genetic_algorithm import GeneticAlgorithm
from src.models import Build


class TestComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_dataset(base_dir=".")
        cls.evaluator = FitnessEvaluator(cls.registry)
        cls.exact_optimizer = ExactSearchOptimizer(cls.registry, cls.evaluator)

    def test_exact_combinations_are_all_valid(self):
        combos = self.exact_optimizer.generate_all_valid_combinations()
        self.assertGreater(len(combos), 1000)

        # Check random sample of combinations for validity
        for combo in combos[:100]:
            b = Build(relics=combo)
            self.assertTrue(b.is_valid(self.registry.relics))

    def test_exact_search_finds_optimum(self):
        best_builds, elapsed, count = self.exact_optimizer.find_global_optimum(
            champion_name="Jinx", star_power=3, top_k=1
        )
        self.assertEqual(len(best_builds), 1)
        self.assertGreater(best_builds[0].fitness, 0.0)
        self.assertGreater(count, 1000)
        self.assertGreater(elapsed, 0.0)

    def test_ga_near_optimality_compared_to_exact(self):
        # Run exact
        exact_builds, exact_time, _ = self.exact_optimizer.find_global_optimum(
            champion_name="Yasuo", star_power=3, top_k=1
        )
        exact_best = exact_builds[0]

        # Run GA
        ga = GeneticAlgorithm(
            registry=self.registry,
            evaluator=self.evaluator,
            population_size=40,
            generations=50,
            seed=123,
        )
        pop = ga.run("Yasuo", star_power=3)
        ga_best = pop[0]

        comparison = compare_ga_vs_exact(
            ga_build=ga_best,
            exact_build=exact_best,
            ga_time_sec=0.05,
            exact_time_sec=exact_time,
        )

        # GA should reach at least 85% of exact global optimum, usually 95-100%
        self.assertGreaterEqual(comparison["optimality_percentage"], 85.0)


if __name__ == "__main__":
    unittest.main()
