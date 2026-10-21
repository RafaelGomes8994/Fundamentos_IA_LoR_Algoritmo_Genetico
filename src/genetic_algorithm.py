"""
Genetic Algorithm Engine for Path of Champions Build Optimization.
Preserves the evolutionary architecture of Balbinot et al. (SBGames 2024):
- Tournament Selection
- 2-Offspring Positional Crossover with Order Swap (Figure 4 of Balbinot et al., 2024)
  combined with Stackability Constraint Repair
- Single-Locus Random Mutation with probability TM (Figure 4 of Balbinot et al., 2024)
- Elitism and Convergence History Tracking
- Support for Strategies E1 (General), E2 (Fixed Ban/Exclusion), and E3 (Target Boss Counter)
"""

import random
from typing import List, Tuple, Dict, Optional, Set, Callable
from src.models import Build, Relic
from src.data_loader import DatabaseRegistry
from src.fitness import FitnessEvaluator


class GeneticAlgorithm:
    def __init__(
        self,
        registry: DatabaseRegistry,
        evaluator: FitnessEvaluator,
        population_size: int = 30,
        mutation_rate: float = 0.7,
        crossover_rate: float = 0.85,
        generations: int = 100,
        tournament_size: int = 3,
        elitism_count: int = 2,
        banned_relic: Optional[str] = None,
        seed: Optional[int] = None,
    ):
        self.registry = registry
        self.evaluator = evaluator
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.tournament_size = min(tournament_size, population_size)
        self.elitism_count = min(elitism_count, population_size)
        self.banned_relic = banned_relic

        if seed is not None:
            random.seed(seed)

        self.relic_pool: List[str] = [
            r for r in self.registry.relics.keys() if r != self.banned_relic
        ]
        self.history_best_fitness: List[float] = []
        self.history_avg_fitness: List[float] = []

    def _generate_valid_random_build(self) -> Build:
        """
        Generates a valid build respecting stackability constraints.
        """
        chosen: List[str] = []
        attempts = 0
        while len(chosen) < 3 and attempts < 100:
            attempts += 1
            r = random.choice(self.relic_pool)
            relic = self.registry.relics[r]
            if chosen.count(r) > 0 and not relic.stackable:
                continue
            chosen.append(r)

        while len(chosen) < 3:
            # Fallback to distinct common relics
            for r in self.relic_pool:
                if chosen.count(r) == 0:
                    chosen.append(r)
                if len(chosen) == 3:
                    break

        return Build(relics=(chosen[0], chosen[1], chosen[2]))

    def _repair_build(self, relics_list: List[str]) -> Tuple[str, str, str]:
        """
        Repairs an invalid chromosome to satisfy game stackability rules.
        """
        repaired = list(relics_list[:3])
        while len(repaired) < 3:
            repaired.append(random.choice(self.relic_pool))

        counts: Dict[str, int] = {}
        for i, r in enumerate(repaired):
            relic = self.registry.relics.get(r)
            if not relic or r == self.banned_relic:
                available = [
                    cand for cand in self.relic_pool
                    if cand not in repaired or self.registry.relics[cand].stackable
                ]
                repaired[i] = random.choice(available if available else self.relic_pool)
                r = repaired[i]
                relic = self.registry.relics[r]

            counts[r] = counts.get(r, 0) + 1
            if counts[r] > 1 and not relic.stackable:
                # Replace with alternative valid relic
                available = [
                    cand for cand in self.relic_pool
                    if cand not in repaired or self.registry.relics[cand].stackable
                ]
                if available:
                    repaired[i] = random.choice(available)
                else:
                    repaired[i] = random.choice(self.relic_pool)

        return (repaired[0], repaired[1], repaired[2])

    def _tournament_select(self, population: List[Build]) -> Build:
        """
        Performs tournament selection among `tournament_size` randomly sampled individuals.
        """
        candidates = random.sample(population, self.tournament_size)
        return max(candidates, key=lambda b: b.fitness)

    def _crossover(self, parent1: Build, parent2: Build) -> Tuple[Build, Build]:
        """
        Performs positional crossover between two parent builds following Figure 4
        of Balbinot et al. (SBGames 2024):
        Each pair (ap_i, ap_j) enters the crossover twice (swapping order on second pass):
        - Position 1 from first parent (ap_i)
        - Position 2 from second parent (ap_j)
        - Position 3 from either ap_i or ap_j with 50% probability
        Followed by stackability constraint repair.
        """
        if random.random() > self.crossover_rate:
            return Build(relics=self._repair_build(list(parent1.relics))), Build(
                relics=self._repair_build(list(parent2.relics))
            )

        p1 = list(parent1.relics)
        p2 = list(parent2.relics)

        # First pass: (ap_i = p1, ap_j = p2)
        c1 = [
            p1[0],
            p2[1],
            p1[2] if random.random() < 0.5 else p2[2],
        ]
        # Second pass (swapped order): (ap_i = p2, ap_j = p1)
        c2 = [
            p2[0],
            p1[1],
            p2[2] if random.random() < 0.5 else p1[2],
        ]

        repaired1 = self._repair_build(c1)
        repaired2 = self._repair_build(c2)
        return Build(relics=repaired1), Build(relics=repaired2)

    def _mutate(self, build: Build) -> Build:
        """
        Applies mutation operator by swapping a relic gene with probability `mutation_rate`.
        """
        if random.random() < self.mutation_rate:
            relics_list = list(build.relics)
            idx_to_mutate = random.randint(0, 2)
            # Pick candidate that doesn't violate stackability
            available = [
                cand for cand in self.relic_pool
                if cand not in relics_list or self.registry.relics[cand].stackable
            ]
            new_relic = random.choice(available if available else self.relic_pool)
            relics_list[idx_to_mutate] = new_relic
            repaired = self._repair_build(relics_list)
            return Build(relics=repaired)
        return build

    def run(
        self,
        champion_name: str,
        star_power: int = 3,
        boss_name: Optional[str] = None,
        progress_callback: Optional[Callable[[int, float, float], None]] = None,
    ) -> List[Build]:
        """
        Executes the Genetic Algorithm and returns the final population sorted by fitness.
        """
        self.history_best_fitness.clear()
        self.history_avg_fitness.clear()

        # 1. Initialize population
        population: List[Build] = [
            self._generate_valid_random_build() for _ in range(self.pop_size)
        ]

        # Evaluate initial population
        for individual in population:
            self.evaluator.evaluate(individual, champion_name, star_power, boss_name)

        population.sort(key=lambda b: b.fitness, reverse=True)

        for gen in range(self.generations):
            # Elitism: retain top individuals
            new_population: List[Build] = [
                Build(relics=ind.relics, fitness=ind.fitness, breakdown=ind.breakdown)
                for ind in population[: self.elitism_count]
            ]

            # Generate rest of population through Selection, Crossover, and Mutation
            while len(new_population) < self.pop_size:
                parent1 = self._tournament_select(population)
                parent2 = self._tournament_select(population)

                child1, child2 = self._crossover(parent1, parent2)
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)

                self.evaluator.evaluate(child1, champion_name, star_power, boss_name)
                self.evaluator.evaluate(child2, champion_name, star_power, boss_name)

                new_population.append(child1)
                if len(new_population) < self.pop_size:
                    new_population.append(child2)

            population = new_population
            population.sort(key=lambda b: b.fitness, reverse=True)

            best_fit = population[0].fitness
            avg_fit = sum(b.fitness for b in population) / len(population)
            self.history_best_fitness.append(best_fit)
            self.history_avg_fitness.append(avg_fit)

            if progress_callback:
                progress_callback(gen + 1, best_fit, avg_fit)

        return population

    def get_top_k_distinct(
        self,
        population: List[Build],
        k: int = 3,
    ) -> List[Build]:
        """
        Filters and returns the top K unique valid builds.
        Builds are considered identical if they contain the same combination of relics
        regardless of slot order.
        """
        seen: Set[Tuple[str, ...]] = set()
        distinct: List[Build] = []

        for build in population:
            normalized_key = tuple(sorted(build.relics))
            if normalized_key not in seen and build.fitness > -100:
                seen.add(normalized_key)
                distinct.append(build)
                if len(distinct) == k:
                    break

        return distinct
