"""
Benchmark and Exact Search Module.
Provides exhaustive combinatorial search to empirically validate the
optimality, convergence rate, and speedup of the Genetic Algorithm.
Directly aligns with the scientific methodology of SBGames 2024 (RQ1, RQ2).
"""

import time
import itertools
from typing import List, Tuple, Dict, Optional
from src.models import Build
from src.data_loader import DatabaseRegistry
from src.fitness import FitnessEvaluator


class ExactSearchOptimizer:
    """
    Exhaustively searches all valid 3-relic combinations to find the true global optimum.
    Serves as the ground-truth benchmark for evaluating Genetic Algorithm quality.
    """

    def __init__(self, registry: DatabaseRegistry, evaluator: FitnessEvaluator):
        self.registry = registry
        self.evaluator = evaluator
        self.relic_pool = list(self.registry.relics.keys())

    def generate_all_valid_combinations(
        self, banned_relic: Optional[str] = None
    ) -> List[Tuple[str, str, str]]:
        """
        Generates all strictly valid 3-relic combinations taking stackability
        and optional fixed ban (Strategy E2) into account.
        """
        valid_combos: List[Tuple[str, str, str]] = []
        pool = [r for r in self.relic_pool if r != banned_relic]

        # Combinations with replacement (to allow stackable duplicates)
        for combo in itertools.combinations_with_replacement(pool, 3):
            # Check stackability
            counts: Dict[str, int] = {}
            for r in combo:
                counts[r] = counts.get(r, 0) + 1

            is_valid = True
            for r, count in counts.items():
                if count > 1 and not self.registry.relics[r].stackable:
                    is_valid = False
                    break

            if is_valid:
                valid_combos.append(combo)

        return valid_combos

    def find_global_optimum(
        self,
        champion_name: str,
        star_power: int = 3,
        boss_name: Optional[str] = None,
        banned_relic: Optional[str] = None,
        top_k: int = 3,
    ) -> Tuple[List[Build], float, int]:
        """
        Runs exhaustive evaluation over all valid combinations.
        Returns (top_k_builds, elapsed_time_seconds, total_combinations_evaluated).
        """
        combos = self.generate_all_valid_combinations(banned_relic=banned_relic)
        builds: List[Build] = []

        start_time = time.perf_counter()
        for combo in combos:
            b = Build(relics=combo)
            self.evaluator.evaluate(b, champion_name, star_power, boss_name)
            builds.append(b)

        builds.sort(key=lambda b: b.fitness, reverse=True)
        elapsed = time.perf_counter() - start_time

        # Extract top-K distinct builds
        seen = set()
        top_builds: List[Build] = []
        for b in builds:
            key = tuple(sorted(b.relics))
            if key not in seen:
                seen.add(key)
                top_builds.append(b)
                if len(top_builds) == top_k:
                    break

        return top_builds, elapsed, len(combos)


def compare_ga_vs_exact(
    ga_build: Build,
    exact_build: Build,
    ga_time_sec: float,
    exact_time_sec: float,
) -> Dict[str, float]:
    """
    Computes comparative metrics between GA and Exact Search.
    """
    optimality_ratio = (
        (ga_build.fitness / exact_build.fitness) if exact_build.fitness > 0 else 1.0
    )
    return {
        "ga_fitness": round(ga_build.fitness, 4),
        "exact_fitness": round(exact_build.fitness, 4),
        "optimality_percentage": round(min(optimality_ratio, 1.0) * 100, 2),
        "ga_time_ms": round(ga_time_sec * 1000, 2),
        "exact_time_ms": round(exact_time_sec * 1000, 2),
        "speedup_factor": round(exact_time_sec / max(ga_time_sec, 1e-6), 2),
    }
