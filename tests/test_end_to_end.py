"""
End-to-End integration tests for the PoCOptimizer API.
"""

import unittest
from src.optimizer import PoCOptimizer


class TestEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.optimizer = PoCOptimizer(
            pop_size=30,
            generations=30,
            seed=42,
        )

    def test_end_to_end_optimization_jinx(self):
        res = self.optimizer.optimize(
            champion_name="Jinx",
            star_power=3,
            boss_name="Teemo",
            top_k=3,
        )
        self.assertEqual(res.champion, "Jinx")
        self.assertEqual(res.star_power, 3)
        self.assertEqual(res.boss, "Teemo")
        self.assertGreater(len(res.top_k_builds), 0)
        self.assertLessEqual(len(res.top_k_builds), 3)

        best = res.best_build
        self.assertTrue(best.is_valid(self.optimizer.registry.relics))
        self.assertGreater(best.fitness, 0.0)
        self.assertIsNotNone(best.breakdown)

        # Check export to dict
        d = res.to_dict()
        self.assertIn("best_build", d)
        self.assertIn("execution_time_ms", d)

    def test_multi_boss_comparison_adaptation(self):
        # Check adaptation across bosses
        bosses = ["Teemo", "Lissandra"]
        res_map = self.optimizer.compare_bosses(
            champion_name="Jinx",
            star_power=3,
            boss_names=bosses,
        )
        self.assertIn("Teemo", res_map)
        self.assertIn("Lissandra", res_map)
        self.assertIn("Generic (No Boss)", res_map)

        for b_name, build in res_map.items():
            self.assertTrue(build.is_valid(self.optimizer.registry.relics))

    def test_star_power_scaling(self):
        res_1star = self.optimizer.optimize("Jinx", star_power=1)
        res_6star = self.optimizer.optimize("Jinx", star_power=6)

        # 6 star should have higher or equal fitness due to higher power cap
        self.assertGreaterEqual(
            res_6star.best_build.breakdown.star_power_synergy,
            res_1star.best_build.breakdown.star_power_synergy,
        )

    def test_invalid_champion_raises_error(self):
        with self.assertRaises(ValueError):
            self.optimizer.optimize("UnknownChampionX123")

    def test_invalid_boss_raises_error(self):
        with self.assertRaises(ValueError):
            self.optimizer.optimize("Jinx", boss_name="UnknownBossXYZ")

    def test_strategy_e2_fixed_ban_excludes_relic(self):
        banned = "The Loose Cannon's Payload"
        res = self.optimizer.optimize("Jinx", star_power=3, banned_relic=banned, top_k=3)
        for build in res.top_k_builds:
            self.assertNotIn(banned, build.relics)
            self.assertTrue(build.is_valid(self.optimizer.registry.relics))


if __name__ == "__main__":
    unittest.main()
