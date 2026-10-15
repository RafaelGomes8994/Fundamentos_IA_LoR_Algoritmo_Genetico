"""
Unit tests for Domain Models and Build validity checks.
"""

import unittest
from src.models import Relic, Champion, Boss, Build, Rarity, Archetype


class TestModels(unittest.TestCase):
    def setUp(self):
        self.stackable_relic = Relic(
            name="Luden's Tempest",
            rarity=Rarity.RARE,
            base_score=5.0,
            stackable=True,
            tags=("spell", "burn"),
        )
        self.non_stackable_relic = Relic(
            name="The Loose Cannon's Payload",
            rarity=Rarity.RARE,
            base_score=2.0,
            stackable=False,
            tags=("discard", "burn"),
        )
        self.epic_relic = Relic(
            name="Chosen by the Stars",
            rarity=Rarity.EPIC,
            base_score=8.5,
            stackable=False,
            tags=("stat_buff", "fated"),
        )
        self.relics_registry = {
            self.stackable_relic.name: self.stackable_relic,
            self.non_stackable_relic.name: self.non_stackable_relic,
            self.epic_relic.name: self.epic_relic,
        }

    def test_valid_build_distinct(self):
        build = Build(
            relics=(
                "The Loose Cannon's Payload",
                "Luden's Tempest",
                "Chosen by the Stars",
            )
        )
        self.assertTrue(build.is_valid(self.relics_registry))

    def test_valid_build_with_stackable_relics(self):
        # 3 copies of stackable relic is valid
        build = Build(
            relics=(
                "Luden's Tempest",
                "Luden's Tempest",
                "Luden's Tempest",
            )
        )
        self.assertTrue(build.is_valid(self.relics_registry))

    def test_invalid_build_with_duplicate_non_stackable(self):
        # 2 copies of Payload is invalid
        build = Build(
            relics=(
                "The Loose Cannon's Payload",
                "The Loose Cannon's Payload",
                "Luden's Tempest",
            )
        )
        self.assertFalse(build.is_valid(self.relics_registry))

    def test_invalid_build_with_duplicate_epic(self):
        # 2 copies of Epic relic is invalid
        build = Build(
            relics=(
                "Chosen by the Stars",
                "Chosen by the Stars",
                "Luden's Tempest",
            )
        )
        self.assertFalse(build.is_valid(self.relics_registry))

    def test_invalid_build_with_unknown_relic(self):
        build = Build(
            relics=(
                "Luden's Tempest",
                "NonExistentRelic",
                "Chosen by the Stars",
            )
        )
        self.assertFalse(build.is_valid(self.relics_registry))

    def test_invalid_build_wrong_size(self):
        build = Build(relics=("Luden's Tempest", "Chosen by the Stars"))  # Only 2
        self.assertFalse(build.is_valid(self.relics_registry))

    def test_champion_model_properties(self):
        champ = Champion(
            name="Jinx",
            archetype=Archetype.DISCARD_BURN,
            difficulty="Easy",
            core_mechanic="Discards hand to burn nexus",
            tier="S+",
            bis_relics=["The Loose Cannon's Payload", "Luden's Tempest"],
        )
        d = champ.to_dict()
        self.assertEqual(d["name"], "Jinx")
        self.assertEqual(d["tier"], "S+")
        self.assertEqual(len(d["bis_relics"]), 2)


if __name__ == "__main__":
    unittest.main()
