"""
Запускает небольшой HTTP-сервер для статической папки `site/`. Тесты работают
с настоящими http://-адресами, поскольку браузеры сильнее ограничивают iframe
и cookie на file://-страницах.

Пример:
    server = LocalSiteServer()
    server.start()
    driver.get(server.url("login.html"))
    ...
    server.stop()
"""

import http.server
import socketserver
import threading
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent.parent / "site"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE_DIR), **kwargs)

    def log_message(self, format, *args):  # noqa: A002 - matches base signature
        pass  # keep pytest output clean


class LocalSiteServer:
    def __init__(self, port: int = 0):
        self._server = socketserver.TCPServer(("127.0.0.1", port), _QuietHandler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def port(self) -> int:
        return self._server.server_address[1]

    def start(self) -> "LocalSiteServer":
        self._thread.start()
        return self

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()

    def url(self, path: str = "") -> str:
        return f"http://127.0.0.1:{self.port}/{path.lstrip('/')}"
