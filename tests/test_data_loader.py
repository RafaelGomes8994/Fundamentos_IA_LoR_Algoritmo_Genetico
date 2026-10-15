"""
Unit tests for data loader and dataset registry.
"""

import unittest
import os
from src.data_loader import load_dataset, DatabaseRegistry
from src.models import Rarity, Archetype


class TestDataLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_dataset(base_dir=".")

    def test_database_loads_champions(self):
        self.assertGreater(len(self.registry.champions), 30)
        self.assertIn("Jinx", self.registry.champions)
        self.assertIn("Yasuo", self.registry.champions)
        self.assertIn("Aurelion Sol", self.registry.champions)
        self.assertIn("Nidalee", self.registry.champions)

    def test_database_loads_relics(self):
        self.assertGreater(len(self.registry.relics), 20)
        payload = self.registry.get_relic("The Loose Cannon's Payload")
        self.assertIsNotNone(payload)
        self.assertFalse(payload.stackable)

        ludens = self.registry.get_relic("Luden's Tempest")
        self.assertIsNotNone(ludens)
        self.assertTrue(ludens.stackable)

        chosen = self.registry.get_relic("Chosen by the Stars")
        self.assertIsNotNone(chosen)
        self.assertEqual(chosen.rarity, Rarity.EPIC)
        self.assertFalse(chosen.stackable)

    def test_database_loads_bosses(self):
        self.assertIn("Teemo", self.registry.bosses)
        self.assertIn("Aurelion Sol", self.registry.bosses)
        self.assertIn("Lissandra", self.registry.bosses)
        self.assertIn("Swain", self.registry.bosses)

        liss = self.registry.get_boss("Lissandra")
        self.assertEqual(liss.stars, 5.0)
        self.assertIn("spellshield", liss.counter_tags)
        self.assertIn("spell", liss.penalized_tags)

    def test_synergy_matrix_expert_data(self):
        # Check that expert data from poe_legends_of_runeterra_builds.csv was loaded
        jinx_payload = self.registry.get_synergy("Jinx", "The Loose Cannon's Payload")
        self.assertGreaterEqual(jinx_payload, 10.0)

        yasuo_tempest = self.registry.get_synergy("Yasuo", "Tempest Blade")
        self.assertGreaterEqual(yasuo_tempest, 7.0)

    def test_json_export_and_load(self):
        export_path = os.path.join("data", "test_poc_database.json")
        self.registry.save_json(export_path)
        self.assertTrue(os.path.exists(export_path))
        # Clean up test file
        try:
            os.remove(export_path)
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
