"""
Domain Models for Path of Champions (PoC) Build Optimization.
Provides strongly typed dataclasses for Champions, Relics, Bosses, Star Powers,
and Build representations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Set, Tuple


class Rarity(str, Enum):
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"


class Archetype(str, Enum):
    AGGRESSIVE = "Aggressive"
    CONTROL = "Control"
    COMBO = "Combo"
    DEFENSIVE = "Defensive"
    TITANIC = "Titanic"
    SPELL_SPAM = "Spell_Spam"
    TRANSFORM = "Transform"
    DISCARD_BURN = "Discard_Burn"
    STUN_FREEZE = "Stun_Freeze"
    SLAY = "Slay"
    KEYWORD_STACK = "Keyword_Stack"


@dataclass(frozen=True)
class Relic:
    name: str
    rarity: Rarity
    base_score: float
    stackable: bool
    description: str = ""
    tags: Tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "rarity": self.rarity.value,
            "base_score": self.base_score,
            "stackable": self.stackable,
            "description": self.description,
            "tags": list(self.tags),
        }


@dataclass
class Champion:
    name: str
    archetype: Archetype
    difficulty: str
    core_mechanic: str
    tier: str = "A"
    bis_relics: List[str] = field(default_factory=list)
    star_power_synergies: Dict[int, List[str]] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "archetype": self.archetype.value,
            "difficulty": self.difficulty,
            "core_mechanic": self.core_mechanic,
            "tier": self.tier,
            "bis_relics": self.bis_relics,
            "star_power_synergies": {str(k): v for k, v in self.star_power_synergies.items()},
            "tags": list(self.tags),
        }


@dataclass
class Boss:
    name: str
    stars: float
    map_type: str
    threat_description: str
    counter_tags: Set[str] = field(default_factory=set)
    vulnerable_tags: Set[str] = field(default_factory=set)
    penalized_tags: Set[str] = field(default_factory=set)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "stars": self.stars,
            "map_type": self.map_type,
            "threat_description": self.threat_description,
            "counter_tags": list(self.counter_tags),
            "vulnerable_tags": list(self.vulnerable_tags),
            "penalized_tags": list(self.penalized_tags),
        }


@dataclass
class RelicCombo:
    relics: Tuple[str, ...]
    bonus: float
    description: str = ""


@dataclass
class FitnessBreakdown:
    base_score: float
    champion_synergy: float
    star_power_synergy: float
    combo_bonus: float
    boss_adaptation: float
    penalty: float
    total_fitness: float

    def to_dict(self) -> dict:
        return {
            "base_score": round(self.base_score, 4),
            "champion_synergy": round(self.champion_synergy, 4),
            "star_power_synergy": round(self.star_power_synergy, 4),
            "combo_bonus": round(self.combo_bonus, 4),
            "boss_adaptation": round(self.boss_adaptation, 4),
            "penalty": round(self.penalty, 4),
            "total_fitness": round(self.total_fitness, 4),
        }


@dataclass
class Build:
    relics: Tuple[str, str, str]
    fitness: float = 0.0
    breakdown: Optional[FitnessBreakdown] = None

    def is_valid(self, relics_registry: Dict[str, Relic]) -> bool:
        """
        Validates if the 3 relics conform to game stacking rules.
        """
        if len(self.relics) != 3:
            return False

        counts: Dict[str, int] = {}
        for r in self.relics:
            if r not in relics_registry:
                return False
            counts[r] = counts.get(r, 0) + 1

        for r, count in counts.items():
            if count > 1 and not relics_registry[r].stackable:
                return False

        return True

    def to_dict(self) -> dict:
        res = {
            "relics": list(self.relics),
            "fitness": round(self.fitness, 4),
        }
        if self.breakdown:
            res["breakdown"] = self.breakdown.to_dict()
        return res
