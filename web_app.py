"""
Interactive Web Application for Legends of Runeterra: Path of Champions Build Optimizer.
Uses Python's built-in HTTP server (zero external web dependencies) to serve an
interactive Hextech-styled frontend connected directly to PoCOptimizer.

Usage:
    python web_app.py
    python web_app.py --port 8080 --no-browser
"""

import argparse
import json
import mimetypes
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# Ensure project root is in sys.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_dataset
from src.optimizer import PoCOptimizer

REGISTRY = load_dataset(ROOT_DIR)
WEB_DIR = os.path.join(ROOT_DIR, "web")


def format_cli_output(
    champ_obj,
    stars: int,
    boss_obj,
    banned_relic: str | None,
    res,
) -> str:
    """Generates the exact terminal-style text output matching examples/demo_cli.py."""
    lines = []
    sep_eq = "=" * 70
    sep_dash = "-" * 70

    lines.append(sep_eq)
    lines.append(f"  OTIMIZACAO DE BUILDS: {champ_obj.name.upper()} ({stars}*)")
    lines.append(sep_eq)
    lines.append(f"Arquetipo:           {champ_obj.archetype.value}")
    lines.append(f"Estrategia Base:     {champ_obj.core_mechanic}")
    if boss_obj:
        lines.append(
            f"Chefe Selecionado:   {boss_obj.name} ({boss_obj.stars}*) - {boss_obj.threat_description}"
        )
    else:
        lines.append("Cenário:             Geral (Estratégia E1 - Sem chefe específico)")

    if banned_relic:
        lines.append(f"Relíquia Restrita:   {banned_relic} (Estratégia E2 - Banimento Fixo)")

    lines.append("\nExecutando Algoritmo Genético...")
    lines.append(f"Tempo de Execução:   {res.execution_time_ms:.2f} ms")
    lines.append(f"Gerações Evoluídas:  {res.generations_run}")
    lines.append(f"Tamanho População:   {res.population_size}")

    lines.append(f"\n{sep_dash}")
    lines.append(f"  TOP {len(res.top_k_builds)} MELHORES BUILDS ENCONTRADAS")
    lines.append(sep_dash)

    for rank, build in enumerate(res.top_k_builds, 1):
        lines.append(f"\n[Rank #{rank}] Fitness Total: {build.fitness:.4f}")
        lines.append(f"  Slot 1: {build.relics[0]}")
        lines.append(f"  Slot 2: {build.relics[1]}")
        lines.append(f"  Slot 3: {build.relics[2]}")
        if build.breakdown:
            bd = build.breakdown
            lines.append("  Detalhes do Fitness:")
            lines.append(f"    - Poder Base Relíquias:     +{bd.base_score:.2f}")
            lines.append(f"    - Sinergia Campeão:         +{bd.champion_synergy:.2f}")
            lines.append(f"    - Sinergia Poder Estelar:   +{bd.star_power_synergy:.2f}")
            lines.append(f"    - Bônus Combos de Relíquia: +{bd.combo_bonus:.2f}")
            if bd.boss_adaptation != 0:
                sign = "+" if bd.boss_adaptation > 0 else ""
                lines.append(f"    - Adaptação ao Chefe:       {sign}{bd.boss_adaptation:.2f}")

    lines.append("\n" + sep_eq)
    return "\n".join(lines)


class OptimizerRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args):
        # Clean console logging
        sys.stdout.write(f"[WEB] {self.address_string()} - {format % args}\n")

    def _send_json(self, data: dict, status: int = 200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _serve_static_file(self, rel_path: str):
        if rel_path in ("", "/"):
            rel_path = "index.html"
        else:
            rel_path = rel_path.lstrip("/")

        full_path = os.path.abspath(os.path.join(WEB_DIR, rel_path))
        if not full_path.startswith(os.path.abspath(WEB_DIR)) or not os.path.isfile(full_path):
            self.send_error(404, "File not found")
            return

        content_type, _ = mimetypes.guess_type(full_path)
        if not content_type:
            content_type = "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type += "; charset=utf-8"

        with open(full_path, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/metadata":
            champions = [
                REGISTRY.champions[name].to_dict()
                for name in sorted(REGISTRY.champions.keys())
            ]
            bosses = [
                REGISTRY.bosses[name].to_dict()
                for name in sorted(
                    REGISTRY.bosses.keys(), key=lambda x: REGISTRY.bosses[x].stars
                )
            ]
            relics = [
                REGISTRY.relics[name].to_dict()
                for name in sorted(REGISTRY.relics.keys())
            ]
            self._send_json(
                {
                    "champions": champions,
                    "bosses": bosses,
                    "relics": relics,
                }
            )
            return

        self._serve_static_file(parsed.path)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/optimize":
            self._send_json({"error": "Endpoint não encontrado."}, status=404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            body = json.loads(raw_body)

            champion_name = body.get("champion", "Jinx")
            stars = int(body.get("stars", 3))
            boss_name = body.get("boss") or None
            ban_relic = body.get("ban_relic") or None
            top_k = max(1, min(10, int(body.get("top_k", 3))))
            pop_size = max(10, min(300, int(body.get("pop_size", 30))))
            generations = max(10, min(500, int(body.get("generations", 100))))

            optimizer = PoCOptimizer(
                registry=REGISTRY,
                pop_size=pop_size,
                generations=generations,
            )

            res = optimizer.optimize(
                champion_name=champion_name,
                star_power=stars,
                boss_name=boss_name,
                banned_relic=ban_relic,
                top_k=top_k,
            )

            champ_obj = REGISTRY.champions[champion_name]
            boss_obj = REGISTRY.bosses.get(boss_name) if boss_name else None

            relic_Catalog_subset = {}
            for b in res.top_k_builds:
                for r_name in b.relics:
                    if r_name in REGISTRY.relics and r_name not in relic_Catalog_subset:
                        relic_Catalog_subset[r_name] = REGISTRY.relics[r_name].to_dict()

            cli_text = format_cli_output(
                champ_obj=champ_obj,
                stars=stars,
                boss_obj=boss_obj,
                banned_relic=ban_relic,
                res=res,
            )

            response_payload = res.to_dict()
            response_payload["champion_info"] = champ_obj.to_dict()
            response_payload["boss_info"] = boss_obj.to_dict() if boss_obj else None
            response_payload["banned_relic"] = ban_relic
            response_payload["relic_details"] = relic_Catalog_subset
            response_payload["history_best_fitness"] = [
                round(v, 4) for v in res.history_best_fitness
            ]
            response_payload["history_avg_fitness"] = [
                round(v, 4) for v in res.history_avg_fitness
            ]
            response_payload["cli_output"] = cli_text

            self._send_json(response_payload)

        except Exception as exc:
            self._send_json({"error": str(exc)}, status=400)


def main():
    parser = argparse.ArgumentParser(
        description="Servidor Web Interativo - Otimizador de Builds LoR (Algoritmo Genético)"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Porta HTTP para rodar o servidor (padrão: 8000)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host de escuta (padrão: 127.0.0.1)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Não abrir o navegador automaticamente ao iniciar",
    )
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}"
    server = ThreadingHTTPServer((args.host, args.port), OptimizerRequestHandler)

    print("=" * 70)
    print("  LoR: Path of Champions - Otimizador Web (Algoritmo Genético)")
    print("=" * 70)
    print(f"  Servidor ativo em: {url}")
    print(f"  Campeões carregados: {len(REGISTRY.champions)}")
    print(f"  Relíquias carregadas: {len(REGISTRY.relics)}")
    print(f"  Chefes carregados: {len(REGISTRY.bosses)}")
    print("  Pressione Ctrl+C para encerrar.")
    print("=" * 70)

    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando servidor web...")
        server.server_close()


if __name__ == "__main__":
    main()

