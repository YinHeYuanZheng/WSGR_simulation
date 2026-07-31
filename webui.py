# -*- coding: utf-8 -*-
# Author:银河远征(AI supported)
"""Run the WSGR browser interface and its local simulation API."""

from __future__ import annotations

import argparse
import json
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from src.webui.service import SimulationBusyError, WebUIService


STATIC_ROOT = Path(__file__).resolve().parent / "src" / "webui" / "static"


class WebUIRequestHandler(SimpleHTTPRequestHandler):
    service: WebUIService

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, directory=str(STATIC_ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self) -> None:  # noqa: N802 - inherited HTTP method name
        path = urlparse(self.path).path
        if path == "/api/bootstrap":
            self._send_json(self.service.bootstrap())
            return
        if path == "/api/simulation/status":
            self._send_json(self.service.simulations.snapshot())
            return
        if path == "/api/map-simulation/status":
            self._send_json(self.service.map_simulations.snapshot())
            return
        if path == "/api/environment/settings":
            try:
                self._send_json(self.service.environment_settings())
            except (TypeError, ValueError) as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except Exception as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if path == "/api/map/effects":
            try:
                self._send_json(self.service.map_effects())
            except (TypeError, ValueError) as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except Exception as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802 - inherited HTTP method name
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/ship/health-limit":
                self._send_json(self.service.friend_health_limit(payload["ship"]))
                return
            if path == "/api/map/fleet-summary":
                self._send_json(self.service.map_enemy_fleet_summary(payload["fleet"]))
                return
            if path == "/api/environment/settings":
                self._send_json(
                    self.service.update_environment_settings(payload["settings"])
                )
                return
            if path == "/api/map/exists":
                self._send_json(self.service.map_exists(payload["mapid"]))
                return
            if path == "/api/map/load":
                self._send_json(self.service.load_map_document(payload["mapid"]))
                return
            if path == "/api/map/import":
                self._send_json(self.service.load_uploaded_map_document(payload["content"]))
                return
            if path == "/api/map/save":
                self._send_json(
                    self.service.save_map_document(
                        payload["map"],
                        overwrite=bool(payload.get("overwrite", False)),
                    )
                )
                return
            if path == "/api/simulation/start":
                config = self.service.prepare_simulation_config(payload["config"])
                state = self.service.simulations.start(
                    config, payload.get("epoch", 5000), payload.get("battle_num", 1)
                )
                self._send_json(state, HTTPStatus.ACCEPTED)
                return
            if path == "/api/simulation/stop":
                self._send_json(self.service.simulations.stop())
                return
            if path == "/api/simulation/reset":
                self._send_json(self.service.simulations.reset())
                return
            if path == "/api/map-simulation/start":
                config = self.service.prepare_simulation_config(payload["config"])
                map_document = payload.get("map")
                if not isinstance(map_document, dict):
                    raise ValueError("缺少当前地图内容")
                config["_map_document"] = map_document
                state = self.service.map_simulations.start(
                    config, payload.get("epoch", 5000), 1
                )
                self._send_json(state, HTTPStatus.ACCEPTED)
                return
            if path == "/api/map-simulation/stop":
                self._send_json(self.service.map_simulations.stop())
                return
            if path == "/api/map-simulation/reset":
                self._send_json(self.service.map_simulations.reset())
                return
            if path == "/api/config/import":
                config = self.service.load_uploaded_config(payload["filename"], payload["content"])
                self._send_json({"config": config})
                return
            if path == "/api/config/export":
                content = self.service.dump_config(payload["config"]).encode("utf-8")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/yaml; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="wsgr_config.yaml"')
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            self._send_json({"error": "接口不存在"}, HTTPStatus.NOT_FOUND)
        except SimulationBusyError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.CONFLICT)
        except (KeyError, TypeError, ValueError) as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except Exception as exc:  # keep local server failures visible to the UI
            self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _read_json(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            return {}
        if content_length > 10 * 1024 * 1024:
            raise ValueError("请求内容超过 10 MB")
        data = json.loads(self.rfile.read(content_length).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("请求内容必须为 JSON 对象")
        return data

    def _send_json(self, data: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="启动 WSGR WebUI")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址，默认仅允许本机访问")
    parser.add_argument("--port", type=int, default=8760, help="监听端口")
    parser.add_argument("--open", action="store_true", help="启动后自动在默认浏览器中打开")
    args = parser.parse_args()

    if not STATIC_ROOT.is_dir():
        raise FileNotFoundError(f"WebUI 静态资源目录不存在：{STATIC_ROOT}")

    WebUIRequestHandler.service = WebUIService()
    server = ThreadingHTTPServer((args.host, args.port), WebUIRequestHandler)
    url = f"http://{args.host}:{args.port}"
    print(f"WSGR WebUI: {url}")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
