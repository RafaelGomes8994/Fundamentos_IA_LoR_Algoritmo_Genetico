"""
Scientific Benchmark Module (Replicating SBGames 2024 Experimental Study).
Tests configurations conf1, conf2, conf3 across multiple test runs (RQ1, RQ2),
comparing against Exact Exhaustive Search ground truth.

Usage:
    python examples/benchmark_vs_exact.py
"""

import sys
import os
import time
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Reconfigure stdout for UTF-8 if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.data_loader import load_dataset
from src.fitness import FitnessEvaluator
from src.genetic_algorithm import GeneticAlgorithm
from src.comparison import ExactSearchOptimizer


def run_benchmark():
    registry = load_dataset()
    evaluator = FitnessEvaluator(registry)
    exact_optimizer = ExactSearchOptimizer(registry, evaluator)

    # 3 Experimental Configurations from SBGames 2024 (Table 2)
    configurations = {
        "conf1": {"P": 10, "TM": 0.3, "G": 10},
        "conf2": {"P": 20, "TM": 0.5, "G": 50},
        "conf3": {"P": 30, "TM": 0.7, "G": 100},
    }

    test_champions = ["Jinx", "Yasuo", "Aurelion Sol", "Swain"]
    reps = 30  # 30 repetitions per configuration as specified in Section 5.1 of Balbinot et al. (2024)

    print("=" * 80)
    print("  ESTUDO EXPERIMENTAL: AVALIACAO DE EFETIVIDADE (RQ1) E EFICIENCIA (RQ2)")
    print("  Metodologia SBGames 2024 / GQM (Goal-Question-Metric)")
    print("=" * 80)

    summary_rows = []

    for champ in test_champions:
        print(f"\n[Calculando Otimo Global Exato para {champ} via Busca Exaustiva...]")
        exact_builds, exact_time_sec, total_combos = exact_optimizer.find_global_optimum(
            champion_name=champ, star_power=3, top_k=1
        )
        exact_best = exact_builds[0]
        exact_fitness = exact_best.fitness
        print(f"  -> Otimo Global Exato: {exact_fitness:.4f} | Tempo: {exact_time_sec*1000:.2f} ms ({total_combos} combinacoes)")

        for conf_name, params in configurations.items():
            fitness_list = []
            time_list = []

            for _ in range(reps):
                ga = GeneticAlgorithm(
                    registry=registry,
                    evaluator=evaluator,
                    population_size=params["P"],
                    mutation_rate=params["TM"],
                    generations=params["G"],
                )
                t0 = time.perf_counter()
                pop = ga.run(champion_name=champ, star_power=3)
                t1 = time.perf_counter()

                best_b = pop[0]
                fitness_list.append(best_b.fitness)
                time_list.append((t1 - t0) * 1000.0)

            avg_fit = sum(fitness_list) / len(fitness_list)
            max_fit = max(fitness_list)
            avg_time = sum(time_list) / len(time_list)
            optimality_pct = (avg_fit / exact_fitness) * 100.0 if exact_fitness > 0 else 100.0

            summary_rows.append({
                "champion": champ,
                "config": conf_name,
                "P": params["P"],
                "TM": params["TM"],
                "G": params["G"],
                "exact_fitness": round(exact_fitness, 2),
                "avg_fitness": round(avg_fit, 2),
                "max_fitness": round(max_fit, 2),
                "optimality_pct": round(min(optimality_pct, 100.0), 2),
                "avg_time_ms": round(avg_time, 2),
            })

            print(
                f"  {conf_name} (P={params['P']}, TM={params['TM']}, G={params['G']}): "
                f"Fitness Medio: {avg_fit:.2f} ({optimality_pct:.1f}% do otimo) | "
                f"Tempo Medio: {avg_time:.2f} ms"
            )

    print("\n" + "=" * 80)
    print("  TABELA FINAL DE RESULTADOS EXPERIMENTAIS")
    print("=" * 80)
    print(f"{'Campeao':<14} | {'Config':<6} | {'P':<3} | {'TM':<4} | {'G':<3} | {'Otimo':<7} | {'Fitness Med':<11} | {'Otimalidade':<11} | {'Tempo (ms)':<10}")
    print("-" * 88)
    for r in summary_rows:
        print(
            f"{r['champion']:<14} | {r['config']:<6} | {r['P']:<3} | {r['TM']:<4} | {r['G']:<3} | "
            f"{r['exact_fitness']:<7} | {r['avg_fitness']:<11} | {r['optimality_pct']:>9.1f}% | {r['avg_time_ms']:>8.2f} ms"
        )
    print("=" * 88)


if __name__ == "__main__":
    run_benchmark()
