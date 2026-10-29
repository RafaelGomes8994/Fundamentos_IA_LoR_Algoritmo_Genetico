"""
Batch Runner: Generates and catalogs the optimal builds for ALL champions
in the Path of Champions database. Exports the results to Markdown.

Usage:
    python examples/run_all_champions.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Reconfigure stdout for UTF-8 if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.optimizer import PoCOptimizer
from src.data_loader import load_dataset


def main():
    registry = load_dataset()
    optimizer = PoCOptimizer(registry=registry, pop_size=40, generations=60)

    champions = sorted(list(registry.champions.keys()))
    print("=" * 80)
    print(f"  OTIMIZANDO BUILDS PARA TODOS OS {len(champions)} CAMPEÕES DO PATH OF CHAMPIONS")
    print("=" * 80)

    results = []
    start_total = time.perf_counter()

    for i, champ_name in enumerate(champions, 1):
        champ = registry.champions[champ_name]
        res = optimizer.optimize(champ_name, star_power=3)
        b = res.best_build

        relics_str = ", ".join(b.relics)
        print(f"[{i:2d}/{len(champions)}] {champ_name:<20} | Fitness: {b.fitness:6.2f} | Build: {relics_str}")

        results.append({
            "champion": champ_name,
            "archetype": champ.archetype.value,
            "tier": champ.tier,
            "relic_1": b.relics[0],
            "relic_2": b.relics[1],
            "relic_3": b.relics[2],
            "fitness": round(b.fitness, 2),
            "time_ms": round(res.execution_time_ms, 1),
        })

    total_time = time.perf_counter() - start_total
    avg_time = (total_time / len(champions)) * 1000

    print("=" * 80)
    print(f"Concluído com sucesso em {total_time:.2f}s (Média por campeão: {avg_time:.1f}ms)!")

    # Export to Markdown document
    output_md_path = os.path.join("Docs", "ALL_CHAMPIONS_BUILDS.md")
    os.makedirs("Docs", exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("# Catálogo de Builds Ótimas - Path of Champions\n\n")
        f.write(f"Relatório gerado automaticamente pelo **Algoritmo Genético de Otimização**.\n\n")
        f.write(f"- **Total de Campeões Avaliados:** {len(champions)}\n")
        f.write(f"- **Tempo Médio de Otimização:** {avg_time:.1f} ms por campeão\n")
        f.write(f"- **Critério de Avaliação:** Poder Estelar 3*, Fitness Multidimensional\n\n")
        f.write("| # | Campeão | Arquétipo | Tier | Relíquia 1 | Relíquia 2 | Relíquia 3 | Fitness | Tempo (ms) |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")

        for i, row in enumerate(results, 1):
            f.write(
                f"| {i} | **{row['champion']}** | {row['archetype']} | {row['tier']} | "
                f"{row['relic_1']} | {row['relic_2']} | {row['relic_3']} | "
                f"{row['fitness']} | {row['time_ms']} |\n"
            )

    print(f"\nRelatório completo salvo em: {output_md_path}")


if __name__ == "__main__":
    main()
