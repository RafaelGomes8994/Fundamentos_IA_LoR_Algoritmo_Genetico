"""
High-Level Orchestrator & API for Path of Champions Build Optimization.
Provides unified interface for single-run optimization, multi-boss analysis,
top-K ranking, and empirical benchmarking.
"""

import time
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from src.data_loader import DatabaseRegistry, load_dataset
from src.fitness import FitnessEvaluator
from src.genetic_algorithm import GeneticAlgorithm
from src.comparison import ExactSearchOptimizer, compare_ga_vs_exact
from src.models import Build, Champion, Boss


@dataclass
class OptimizationResult:
    champion: str
    star_power: int
    boss: Optional[str]
    best_build: Build
    top_k_builds: List[Build]
    execution_time_ms: float
    generations_run: int
    population_size: int
    history_best_fitness: List[float]
    history_avg_fitness: List[float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "champion": self.champion,
            "star_power": self.star_power,
            "boss": self.boss,
            "best_build": self.best_build.to_dict(),
            "top_k_builds": [b.to_dict() for b in self.top_k_builds],
            "execution_time_ms": round(self.execution_time_ms, 2),
            "generations_run": self.generations_run,
            "population_size": self.population_size,
        }


class PoCOptimizer:
    def __init__(
        self,
        registry: Optional[DatabaseRegistry] = None,
        evaluator: Optional[FitnessEvaluator] = None,
        pop_size: int = 30,
        mutation_rate: float = 0.7,
        crossover_rate: float = 0.85,
        generations: int = 100,
        seed: Optional[int] = None,
    ):
        self.registry = registry if registry is not None else load_dataset()
        self.evaluator = (
            evaluator if evaluator is not None else FitnessEvaluator(self.registry)
        )
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.seed = seed

    def optimize(
        self,
        champion_name: str,
        star_power: int = 3,
        boss_name: Optional[str] = None,
        banned_relic: Optional[str] = None,
        top_k: int = 3,
    ) -> OptimizationResult:
        """
        Runs Genetic Algorithm optimization for a given champion, star power,
        optional boss (Strategy E3), and optional banned relic (Strategy E2).
        Returns the optimization result with Top-K distinct builds and history.
        """
        if champion_name not in self.registry.champions:
            available = list(self.registry.champions.keys())[:10]
            raise ValueError(
                f"Champion '{champion_name}' not found. Sample of available champions: {available}"
            )

        if boss_name and boss_name not in self.registry.bosses:
            available_bosses = list(self.registry.bosses.keys())
            raise ValueError(
                f"Boss '{boss_name}' not found. Available bosses: {available_bosses}"
            )

        if banned_relic and banned_relic not in self.registry.relics:
            available_relics = list(self.registry.relics.keys())[:10]
            raise ValueError(
                f"Relic '{banned_relic}' not found. Sample of available relics: {available_relics}"
            )

        ga = GeneticAlgorithm(
            registry=self.registry,
            evaluator=self.evaluator,
            population_size=self.pop_size,
            mutation_rate=self.mutation_rate,
            crossover_rate=self.crossover_rate,
            generations=self.generations,
            banned_relic=banned_relic,
            seed=self.seed,
        )

        start_time = time.perf_counter()
        final_pop = ga.run(
            champion_name=champion_name,
            star_power=star_power,
            boss_name=boss_name,
        )
        elapsed_sec = time.perf_counter() - start_time

        top_builds = ga.get_top_k_distinct(final_pop, k=top_k)
        best = top_builds[0] if top_builds else final_pop[0]

        return OptimizationResult(
            champion=champion_name,
            star_power=star_power,
            boss=boss_name,
            best_build=best,
            top_k_builds=top_builds,
            execution_time_ms=elapsed_sec * 1000.0,
            generations_run=self.generations,
            population_size=self.pop_size,
            history_best_fitness=list(ga.history_best_fitness),
            history_avg_fitness=list(ga.history_avg_fitness),
        )

    def compare_bosses(
        self,
        champion_name: str,
        star_power: int = 3,
        boss_names: Optional[List[str]] = None,
    ) -> Dict[str, Build]:
        """
        Optimizes builds for the same champion across multiple bosses
        to demonstrate adaptation and counter-building (Strategy E3).
        """
        if boss_names is None:
            boss_names = ["Teemo", "Aurelion Sol", "Lissandra", "Swain"]

        results = {}
        # Also include unconstrained / generic (no boss)
        gen_res = self.optimize(champion_name=champion_name, star_power=star_power, boss_name=None)
        results["Generic (No Boss)"] = gen_res.best_build

        for b_name in boss_names:
            if b_name in self.registry.bosses:
                res = self.optimize(
                    champion_name=champion_name,
                    star_power=star_power,
                    boss_name=b_name,
                )
                results[b_name] = res.best_build

        return results

    def benchmark_against_exact(
        self,
        champion_name: str,
        star_power: int = 3,
        boss_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Runs both GA and Exact Search to compute convergence, optimality ratio,
        and speed metrics.
        """
        # 1. Run GA
        ga_res = self.optimize(
            champion_name=champion_name,
            star_power=star_power,
            boss_name=boss_name,
            top_k=1,
        )

        # 2. Run Exact Search
        exact_optimizer = ExactSearchOptimizer(self.registry, self.evaluator)
        exact_builds, exact_time_sec, total_combos = exact_optimizer.find_global_optimum(
            champion_name=champion_name,
            star_power=star_power,
            boss_name=boss_name,
            top_k=1,
        )
        exact_best = exact_builds[0]

        comparison = compare_ga_vs_exact(
            ga_build=ga_res.best_build,
            exact_build=exact_best,
            ga_time_sec=ga_res.execution_time_ms / 1000.0,
            exact_time_sec=exact_time_sec,
        )

        comparison["champion"] = champion_name
        comparison["boss"] = boss_name or "None"
        comparison["total_combinations_checked_by_exact"] = total_combos
        comparison["ga_best_relics"] = list(ga_res.best_build.relics)
        comparison["exact_best_relics"] = list(exact_best.relics)

        return comparison
