"""
Unit tests for the Fitness Function and its subcomponents.
"""

import unittest
from src.data_loader import load_dataset
from src.fitness import FitnessEvaluator
from src.models import Build


class TestFitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_dataset(base_dir=".")
        cls.evaluator = FitnessEvaluator(cls.registry)

    def test_invalid_build_receives_heavy_penalty(self):
        # 2 copies of non-stackable Payload
        build = Build(
            relics=(
                "The Loose Cannon's Payload",
                "The Loose Cannon's Payload",
                "Luden's Tempest",
            )
        )
        fitness = self.evaluator.evaluate(build, "Jinx")
        self.assertEqual(fitness, -9999.0)
        self.assertEqual(build.breakdown.penalty, -9999.0)

    def test_champion_synergy_impact(self):
        # Jinx BiS build
        jinx_build = Build(
            relics=(
                "The Loose Cannon's Payload",
                "Luden's Tempest",
                "The Scourge Stash",
            )
        )
        fit_jinx = self.evaluator.evaluate(jinx_build, "Jinx", star_power=3)

        # Same build on a champion with no discard synergy (e.g. Garen)
        garen_build = Build(
            relics=(
                "The Loose Cannon's Payload",
                "Luden's Tempest",
                "The Scourge Stash",
            )
        )
        fit_garen = self.evaluator.evaluate(garen_build, "Garen", star_power=3)

        self.assertGreater(fit_jinx, fit_garen)
        self.assertGreater(
            jinx_build.breakdown.champion_synergy,
            garen_build.breakdown.champion_synergy,
        )

    def test_relic_combo_triggers(self):
        # Build with combo: Payload + Luden's
        combo_build = Build(
            relics=(
                "The Loose Cannon's Payload",
                "Luden's Tempest",
                "Lost Chapter",
            )
        )
        self.evaluator.evaluate(combo_build, "Jinx")
        self.assertGreater(combo_build.breakdown.combo_bonus, 0.0)

        # Build with no known combo
        no_combo_build = Build(
            relics=(
                "Z-Drive Prototype",
                "Warmog's Armor",
                "Banshee's Veil",
            )
        )
        self.evaluator.evaluate(no_combo_build, "Garen")
        self.assertEqual(no_combo_build.breakdown.combo_bonus, 0.0)

    def test_boss_adaptation_lissandra_vs_teemo(self):
        # Build with SpellShield (Banshee's Veil) and raw stats (Chosen by the Stars)
        resilient_build = Build(
            relics=(
                "Banshee's Veil",
                "Chosen by the Stars",
                "The Beast Within",
            )
        )

        # Build relying heavily on cheap spell spam
        spell_heavy_build = Build(
            relics=(
                "Luden's Tempest",
                "Lost Chapter",
                "Archangel's Staff",
            )
        )

        fit_resilient_liss = self.evaluator.evaluate(
            resilient_build, "Jinx", boss_name="Lissandra"
        )
        fit_spell_liss = self.evaluator.evaluate(
            spell_heavy_build, "Jinx", boss_name="Lissandra"
        )

        # Against Lissandra (punishes spells, rewards spellshield & overwhelm),
        # resilient build should have a much higher boss adaptation component
        self.assertGreater(
            resilient_build.breakdown.boss_adaptation,
            spell_heavy_build.breakdown.boss_adaptation,
        )


if __name__ == "__main__":
    unittest.main()
