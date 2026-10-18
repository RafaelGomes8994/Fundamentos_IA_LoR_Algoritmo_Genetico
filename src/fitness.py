"""
Mathematical Fitness Function for Path of Champions Build Optimization.
Formalizes multi-objective fitness calculation combining:
- Base Relic Power
- Champion Synergy
- Star Power Synergy
- Inter-Relic Combos
- Boss Adaptation (Mutator Countering / Strategy E3)
- Game Rules Validation (Stackability Constraints)
"""

from typing import Optional, Dict
from src.models import Build, FitnessBreakdown, Champion, Boss
from src.data_loader import DatabaseRegistry


class FitnessEvaluator:
    """
    Evaluates candidate builds according to game rules, champion synergy,
    star power scaling, and boss mutators.
    """

    def __init__(
        self,
        registry: DatabaseRegistry,
        w_base: float = 0.15,
        w_champ: float = 0.40,
        w_star: float = 0.15,
        w_combo: float = 0.15,
        w_boss: float = 0.15,
    ):
        self.registry = registry
        self.w_base = w_base
        self.w_champ = w_champ
        self.w_star = w_star
        self.w_combo = w_combo
        self.w_boss = w_boss

    def evaluate(
        self,
        build: Build,
        champion_name: str,
        star_power: int = 3,
        boss_name: Optional[str] = None,
    ) -> float:
        """
        Calculates fitness score and populates the build's breakdown object.
        """
        # 1. Validation & Stacking Rules check
        if not build.is_valid(self.registry.relics):
            penalty = -9999.0
            build.fitness = penalty
            build.breakdown = FitnessBreakdown(
                base_score=0.0,
                champion_synergy=0.0,
                star_power_synergy=0.0,
                combo_bonus=0.0,
                boss_adaptation=0.0,
                penalty=penalty,
                total_fitness=penalty,
            )
            return penalty

        # 2. Base Power
        score_base = 0.0
        for relic_name in build.relics:
            relic = self.registry.relics.get(relic_name)
            if relic:
                score_base += relic.base_score

        # 3. Champion Synergy
        score_champ = 0.0
        for relic_name in build.relics:
            score_champ += self.registry.get_synergy(champion_name, relic_name)

        # 4. Star Power Synergy: Scales the champion's core mechanics with star rank (1-6)
        score_star = 0.0
        champ = self.registry.get_champion(champion_name)
        if champ:
            # Base star scaling: Each star rank amplifies synergistic relics
            for relic_name in build.relics:
                champ_syn = self.registry.get_synergy(champion_name, relic_name)
                if champ_syn >= 5.0:
                    score_star += (champ_syn * 0.1) * star_power

                # Specific constellation milestone synergies
                if champ.star_power_synergies:
                    milestone_relics = champ.star_power_synergies.get(star_power, [])
                    if relic_name in milestone_relics:
                        score_star += min(star_power * 1.0, 5.0)

        # 5. Relic Combos
        score_combo = 0.0
        for combo in self.registry.combos:
            combo_relics = combo.relics
            # Check if all combo relics are in the build
            # Handle multi-item combos (e.g. ("Guardian's Orb", "Guardian's Orb"))
            build_list = list(build.relics)
            matched = True
            for cr in combo_relics:
                if cr in build_list:
                    build_list.remove(cr)
                else:
                    matched = False
                    break
            if matched:
                score_combo += combo.bonus

        # 6. Boss Adaptation (Mutator Countering)
        score_boss = 0.0
        if boss_name:
            boss = self.registry.get_boss(boss_name)
            if boss:
                for relic_name in build.relics:
                    relic = self.registry.relics.get(relic_name)
                    if not relic:
                        continue
                    for tag in relic.tags:
                        if tag in boss.counter_tags:
                            score_boss += 3.0
                        if tag in boss.vulnerable_tags:
                            score_boss += 2.0
                        if tag in boss.penalized_tags:
                            score_boss -= 3.5

        # Weighted calculation
        total_fitness = (
            (score_base * self.w_base)
            + (score_champ * self.w_champ)
            + (score_star * self.w_star)
            + (score_combo * self.w_combo)
            + (score_boss * self.w_boss)
        )

        build.fitness = total_fitness
        build.breakdown = FitnessBreakdown(
            base_score=score_base * self.w_base,
            champion_synergy=score_champ * self.w_champ,
            star_power_synergy=score_star * self.w_star,
            combo_bonus=score_combo * self.w_combo,
            boss_adaptation=score_boss * self.w_boss,
            penalty=0.0,
            total_fitness=total_fitness,
        )

        return total_fitness
