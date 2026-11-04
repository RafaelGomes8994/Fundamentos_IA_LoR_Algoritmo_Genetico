"""
Vercel Serverless Function: GET /api/metadata
Returns all Champions, Bosses, and Relics from the Path of Champions dataset.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_dataset

REGISTRY = load_dataset(ROOT_DIR)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
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

        payload = json.dumps(
            {
                "champions": champions,
                "bosses": bosses,
                "relics": relics,
            },
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "public, max-age=60")
        self.end_headers()
        self.wfile.write(payload)

