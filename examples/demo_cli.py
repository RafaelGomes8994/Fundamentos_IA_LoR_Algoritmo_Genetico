"""
Interactive Command-Line Interface (CLI) for Path of Champions Build Optimizer.
Allows selecting any champion, star power level (1-6), target boss, and displays
the Top-K recommended builds with full mathematical fitness breakdown.

Usage:
    python examples/demo_cli.py --champion Jinx --stars 3 --boss Lissandra --top_k 3
    python examples/demo_cli.py --champion Yasuo --compare-bosses
    python examples/demo_cli.py --champion "Aurelion Sol" --benchmark
    python examples/demo_cli.py --list-champions
    python examples/demo_cli.py --list-bosses
"""

import sys
import os
import argparse
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Reconfigure stdout for UTF-8 if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.optimizer import PoCOptimizer
from src.data_loader import load_dataset


def format_header(title: str) -> str:
    line = "=" * 70
    return f"\n{line}\n  {title}\n{line}"


def format_sub_header(title: str) -> str:
    line = "-" * 70
    return f"\n{line}\n  {title}\n{line}"


def print_build_details(rank: int, build, show_breakdown: bool = True):
    print(f"\n[Rank #{rank}] Fitness Total: {build.fitness:.4f}")
    print(f"  Slot 1: {build.relics[0]}")
    print(f"  Slot 2: {build.relics[1]}")
    print(f"  Slot 3: {build.relics[2]}")

    if show_breakdown and build.breakdown:
        bd = build.breakdown
        print("  Detalhes do Fitness:")
        print(f"    - Poder Base Relíquias:     +{bd.base_score:.2f}")
        print(f"    - Sinergia Campeão:         +{bd.champion_synergy:.2f}")
        print(f"    - Sinergia Poder Estelar:   +{bd.star_power_synergy:.2f}")
        print(f"    - Bônus Combos de Relíquia: +{bd.combo_bonus:.2f}")
        if bd.boss_adaptation != 0:
            sign = "+" if bd.boss_adaptation > 0 else ""
            print(f"    - Adaptação ao Chefe:       {sign}{bd.boss_adaptation:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="LoR Path of Champions - Otimizador de Builds via Algoritmo Genético"
    )
    parser.add_argument(
        "--champion",
        "-c",
        type=str,
        default="Jinx",
        help="Nome do campeão (ex: Jinx, Yasuo, 'Aurelion Sol', Nidalee, Swain)",
    )
    parser.add_argument(
        "--stars",
        "-s",
        type=int,
        default=3,
        choices=[1, 2, 3, 4, 5, 6],
        help="Nível de Poder Estelar do campeão (1 a 6 estrelas)",
    )
    parser.add_argument(
        "--boss",
        "-b",
        type=str,
        default=None,
        help="Nome do Chefe / Aventura (Estratégia E3 - ex: Teemo, Aurelion Sol, Lissandra, Swain)",
    )
    parser.add_argument(
        "--ban-relic",
        type=str,
        default=None,
        help="Relíquia excluída/indisponível da busca (Estratégia E2 - Banimento Fixo)",
    )
    parser.add_argument(
        "--top_k",
        "-k",
        type=int,
        default=3,
        help="Número de builds distintas a elencar (padrão: 3)",
    )
    parser.add_argument(
        "--compare-bosses",
        action="store_true",
        help="Compara a melhor build contra diferentes chefes (Estratégia E3 / Contra-meta)",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Executa Busca Exaustiva para verificar a taxa de otimalidade da IA",
    )
    parser.add_argument(
        "--list-champions",
        action="store_true",
        help="Lista todos os campeões disponíveis no banco de dados",
    )
    parser.add_argument(
        "--list-bosses",
        action="store_true",
        help="Lista todos os chefes disponíveis no banco de dados",
    )
    parser.add_argument(
        "--pop-size",
        type=int,
        default=30,
        help="Tamanho da população do Algoritmo Genético (padrão conf3: 30)",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=100,
        help="Número de gerações do Algoritmo Genético (padrão conf3: 100)",
    )

    args = parser.parse_args()

    registry = load_dataset()
    optimizer = PoCOptimizer(
        registry=registry,
        pop_size=args.pop_size,
        generations=args.generations,
    )

    if args.list_champions:
        print(format_header("CAMPEÕES DISPONÍVEIS NO BANCO DE DADOS"))
        champs = sorted(list(registry.champions.keys()))
        for i, name in enumerate(champs, 1):
            c = registry.champions[name]
            print(f"{i:2d}. {name:<22} | Arquétipo: {c.archetype.value:<14} | Tier: {c.tier}")
        print(f"\nTotal: {len(champs)} campeões carregados.")
        return

    if args.list_bosses:
        print(format_header("CHEFES / AVENTURAS DISPONÍVEIS"))
        bosses = sorted(list(registry.bosses.keys()), key=lambda x: registry.bosses[x].stars)
        for b_name in bosses:
            b = registry.bosses[b_name]
            print(f"• {b.name} ({b.stars}*) - {b.map_type}")
            print(f"  Mecânica: {b.threat_description}")
            print(f"  Tags de Contra-ataque: {', '.join(b.counter_tags) if b.counter_tags else 'N/A'}")
            print(f"  Tags Penalizadas:      {', '.join(b.penalized_tags) if b.penalized_tags else 'N/A'}\n")
        return

    champion_name = args.champion
    # Case-insensitive matching for champion
    matched_champ = None
    for name in registry.champions:
        if name.lower() == champion_name.lower():
            matched_champ = name
            break

    if not matched_champ:
        print(f"[ERRO] Campeão '{champion_name}' não encontrado.")
        print("Use --list-champions para ver os nomes válidos.")
        return

    # Case-insensitive matching for boss
    matched_boss = None
    if args.boss:
        for b_name in registry.bosses:
            if b_name.lower() == args.boss.lower():
                matched_boss = b_name
                break
        if not matched_boss:
            print(f"[ERRO] Chefe '{args.boss}' não encontrado.")
            print("Use --list-bosses para ver os chefes válidos.")
            return

    # Case-insensitive matching for banned relic (Strategy E2)
    matched_ban = None
    if args.ban_relic:
        for r_name in registry.relics:
            if r_name.lower() == args.ban_relic.lower():
                matched_ban = r_name
                break
        if not matched_ban:
            print(f"[ERRO] Relíquia '{args.ban_relic}' não encontrada.")
            return

    champ_obj = registry.champions[matched_champ]

    if args.compare_bosses:
        print(format_header(f"COMPARAÇÃO MULTI-CHEFE (CONTRA-META) - {matched_champ.upper()}"))
        print(f"Arquétipo: {champ_obj.archetype.value} | Mecânica: {champ_obj.core_mechanic}")
        print(f"Poder Estelar: {args.stars}*")

        multi_res = optimizer.compare_bosses(
            champion_name=matched_champ,
            star_power=args.stars,
            boss_names=["Teemo", "Aurelion Sol", "Lissandra", "Swain"],
        )

        for boss_label, build in multi_res.items():
            print(format_sub_header(f"Chefe: {boss_label}"))
            print_build_details(rank=1, build=build, show_breakdown=True)
        return

    if args.benchmark:
        print(format_header(f"BENCHMARK CIENTÍFICO: AG vs BUSCA EXAUSTIVA - {matched_champ.upper()}"))
        print("Executando Algoritmo Genético e Busca Completa em todas as combinações válidas...")
        bm_res = optimizer.benchmark_against_exact(
            champion_name=matched_champ,
            star_power=args.stars,
            boss_name=matched_boss,
        )

        print(f"\nCampeão:             {bm_res['champion']}")
        print(f"Chefe Alvo:          {bm_res['boss']}")
        print(f"Combinações Totais:  {bm_res['total_combinations_checked_by_exact']}")
        print(f"Fitness AG:          {bm_res['ga_fitness']}")
        print(f"Fitness Ótimo Real:  {bm_res['exact_fitness']}")
        print(f"Taxa de Otimalidade: {bm_res['optimality_percentage']}%")
        print(f"Tempo AG:            {bm_res['ga_time_ms']:.2f} ms")
        print(f"Tempo Busca Exata:   {bm_res['exact_time_ms']:.2f} ms")
        print(f"\nBuild AG:            {bm_res['ga_best_relics']}")
        print(f"Build Ótima Exata:   {bm_res['exact_best_relics']}")
        return

    # Standard Optimization Run
    print(format_header(f"OTIMIZACAO DE BUILDS: {matched_champ.upper()} ({args.stars}*)"))
    print(f"Arquetipo:           {champ_obj.archetype.value}")
    print(f"Estrategia Base:     {champ_obj.core_mechanic}")
    if matched_boss:
        b_obj = registry.bosses[matched_boss]
        print(f"Chefe Selecionado:   {matched_boss} ({b_obj.stars}*) - {b_obj.threat_description}")
    else:
        print("Cenário:             Geral (Estratégia E1 - Sem chefe específico)")
    if matched_ban:
        print(f"Relíquia Restrita:   {matched_ban} (Estratégia E2 - Banimento Fixo)")

    print("\nExecutando Algoritmo Genético...")
    res = optimizer.optimize(
        champion_name=matched_champ,
        star_power=args.stars,
        boss_name=matched_boss,
        banned_relic=matched_ban,
        top_k=args.top_k,
    )

    print(f"Tempo de Execução:   {res.execution_time_ms:.2f} ms")
    print(f"Gerações Evoluídas:  {res.generations_run}")
    print(f"Tamanho População:   {res.population_size}")

    print(format_sub_header(f"TOP {len(res.top_k_builds)} MELHORES BUILDS ENCONTRADAS"))
    for i, b in enumerate(res.top_k_builds, 1):
        print_build_details(rank=i, build=b, show_breakdown=True)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
