"""
Vercel Serverless Function: POST /api/optimize
Executes the Genetic Algorithm via PoCOptimizer and returns Top-K builds + CLI output.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_dataset
from src.optimizer import PoCOptimizer
from web_app import format_cli_output

REGISTRY = load_dataset(ROOT_DIR)


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, status: int = 200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = (
                self.rfile.read(content_length).decode("utf-8")
                if content_length > 0
                else "{}"
            )
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

            relic_catalog_subset = {}
            for b in res.top_k_builds:
                for r_name in b.relics:
                    if r_name in REGISTRY.relics and r_name not in relic_catalog_subset:
                        relic_catalog_subset[r_name] = REGISTRY.relics[r_name].to_dict()

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
            response_payload["relic_details"] = relic_catalog_subset
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

