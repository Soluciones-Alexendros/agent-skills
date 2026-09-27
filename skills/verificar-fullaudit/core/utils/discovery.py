#!/usr/bin/env python3
"""Discovery Engine — crawler con máquina de estados y anti-trampas.

Recorre el sitio desde TARGET_URL (mismo dominio), clasifica nodos
(page/modal/drawer/form) y genera site-map.json. Stdlib puro.

Anti-trampas (configs/thresholds.json):
- MAX_DEPTH=12, MAX_PAGES=150
- ignora /logout, /admin, /wp-admin, /wp-login
- paginación ?page= cortada a 5

Uso:
    python3 discovery.py https://ejemplo.com --out site-map.json
    python3 discovery.py --root-dir tests/fixtures/minisite --out site-map.json  # offline

Salida: 0 OK · 2 error de arranque (URL raíz inalcanzable / directorio vacío)
"""
import argparse
import json
import logging
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

logger = logging.getLogger("e2e.discovery")

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "playwright-e2e-audit/2.0 (+discovery)"

# Red acotada: HTTPError se trata aparte (código visible); el resto degrada el nodo.
NETWORK_ERRORS = (urllib.error.URLError, TimeoutError, OSError, ssl.SSLError, ValueError)


def load_thresholds():
    path = os.path.join(HERE, "..", "configs", "thresholds.json")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data["crawler"]
    except OSError as e:
        raise RuntimeError(f"no se pudo leer {path}: {type(e).__name__}: {e}") from e
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise RuntimeError(f"thresholds inválidos en {path}: {type(e).__name__}: {e}") from e


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.forms = 0
        self.buttons = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "form":
            self.forms += 1
        elif tag == "button" or (tag == "input" and a.get("type") in ("submit", "button")):
            self.buttons += 1
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def normalize_url(url):
    """Canoniza: sin fragmento, query ordenada, sin trailing slash (salvo raíz)."""
    p = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qsl(p.query, keep_blank_values=True)
    query.sort()
    path = p.path if p.path == "/" else p.path.rstrip("/")
    return urllib.parse.urlunparse((p.scheme.lower(), p.netloc.lower(), path,
                                    "", urllib.parse.urlencode(query), ""))


def is_trap(url, cfg, base_netloc):
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https", "local") or p.netloc.lower() != base_netloc:
        return True  # fuera de dominio o esquema no web
    path = p.path.lower()
    if any(ig in path for ig in cfg["ignore_paths"]):
        return True
    qs = urllib.parse.parse_qs(p.query)
    if cfg["pagination_param"] in qs:
        try:
            if int(qs[cfg["pagination_param"]][0]) > cfg["pagination_max"]:
                return True
        except ValueError:
            return True
    if re.search(r"\.(png|jpe?g|gif|webp|avif|svg|pdf|zip|mp4|css|js|ico|xml)(\?|$)", path):
        return True  # recursos, no páginas
    return False


def classify(url, parser):
    if parser.forms:
        return "form"
    return "page"


# ---------------------------------------------------------------- online

def crawl_online(start_url, cfg):
    base_netloc = urllib.parse.urlparse(start_url).netloc.lower()
    visited = {}
    queue = [(start_url, 0, None)]
    errors = []

    while queue and len(visited) < cfg["max_pages"]:
        url, depth, parent = queue.pop(0)
        url = normalize_url(url)
        if url in visited or depth > cfg["max_depth"] or is_trap(url, cfg, base_netloc):
            continue
        node = {"url": url, "depth": depth, "parentAction": parent,
                "status": None, "type": "page", "discoveredElements": 0}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            t0 = time.monotonic()
            with urllib.request.urlopen(req, timeout=cfg["timeout_ms"] / 1000) as r:
                node["status"] = r.status
                node["load_ms"] = round((time.monotonic() - t0) * 1000)
                ctype = r.headers.get("content-type", "")
                if "text/html" not in ctype:
                    node["type"] = "resource"
                    visited[url] = node
                    continue
                body = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            node["status"] = e.code
            visited[url] = node
            errors.append({"url": url, "error": f"HTTP {e.code}"})
            continue
        except NETWORK_ERRORS as e:  # red/ssl/timeout/DNS: registrar y seguir
            logger.debug("crawl %s: %s: %s", url, type(e).__name__, e)
            node["status"] = 0
            visited[url] = node
            errors.append({"url": url, "error": f"{type(e).__name__}: {e}"})
            continue

        parser = LinkParser()
        try:
            parser.feed(body)
        except Exception as e:  # HTML mal formado no detiene el crawl
            logger.debug("parse parcial %s: %s: %s", url, type(e).__name__, e)
        node["title"] = parser.title.strip()[:120]
        node["type"] = classify(url, parser)
        node["discoveredElements"] = parser.forms + parser.buttons
        visited[url] = node
        for href in parser.links:
            absu = urllib.parse.urljoin(url, href)
            n = normalize_url(absu)
            if n not in visited and not is_trap(n, cfg, base_netloc):
                queue.append((n, depth + 1, url))

    return list(visited.values()), errors


# ---------------------------------------------------------------- offline

def crawl_offline(root_dir, cfg):
    """Recorre un sitio estático local (para tests y auditorías offline)."""
    visited = {}
    base = "local://site"
    queue = [("/", 0, None)]
    while queue and len(visited) < cfg["max_pages"]:
        path, depth, parent = queue.pop(0)
        path = normalize_url(base + path)[len(base):]
        if path in visited or depth > cfg["max_depth"]:
            continue
        if is_trap(base + path, cfg, "site"):
            continue
        fs_path = os.path.join(root_dir, path.lstrip("/"))
        if os.path.isdir(fs_path):
            fs_path = os.path.join(fs_path, "index.html")
        node = {"url": base + path, "depth": depth, "parentAction": parent,
                "status": None, "type": "page", "discoveredElements": 0}
        if not os.path.isfile(fs_path):
            node["status"] = 404
            visited[path] = node
            continue
        try:
            with open(fs_path, encoding="utf-8", errors="replace") as fh:
                html_text = fh.read()
        except OSError as e:
            logger.warning("offline ilegible %s: %s: %s", fs_path, type(e).__name__, e)
            node["status"] = 0
            visited[path] = node
            continue
        parser = LinkParser()
        try:
            parser.feed(html_text)
        except Exception as e:  # HTML mal formado no detiene el crawl
            logger.debug("parse parcial offline %s: %s: %s", fs_path, type(e).__name__, e)
        node["status"] = 200
        node["title"] = parser.title.strip()[:120]
        node["type"] = classify(path, parser)
        node["discoveredElements"] = parser.forms + parser.buttons
        visited[path] = node
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            absu = urllib.parse.urljoin(path, href)
            queue.append((absu, depth + 1, path))
    return list(visited.values()), []


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Discovery Engine — site-map.json")
    ap.add_argument("url", nargs="?", help="TARGET_URL raíz")
    ap.add_argument("--root-dir", help="Sitio estático local (modo offline/tests)")
    ap.add_argument("--out", default="site-map.json")
    ap.add_argument("--max-pages", type=int, help="Override MAX_PAGES")
    args = ap.parse_args(argv)
    if not args.url and not args.root_dir:
        ap.error("Indica URL o --root-dir")

    try:
        cfg = load_thresholds()
    except RuntimeError as e:
        logger.error("%s", e)
        print(json.dumps({"error": str(e)}))
        return 2
    if args.max_pages:
        cfg["max_pages"] = args.max_pages

    if args.root_dir:
        if not os.path.isdir(args.root_dir):
            logger.error("directorio inexistente: %s", args.root_dir)
            print(json.dumps({"error": f"Directorio inexistente: {args.root_dir}"}))
            return 2
        nodes, errors = crawl_offline(args.root_dir, cfg)
    else:
        nodes, errors = crawl_online(args.url, cfg)
        if not nodes:
            logger.error("URL raíz inalcanzable: %s", args.url)
            print(json.dumps({"error": f"URL raíz inalcanzable: {args.url}"}))
            return 2

    ok = sum(1 for n in nodes if n["status"] == 200)
    result = {
        "target": args.url or args.root_dir,
        "total_pages": len(nodes),
        "pages_ok": ok,
        "pages_error": len(nodes) - ok,
        "forms_found": sum(1 for n in nodes if n["type"] == "form"),
        "truncated": len(nodes) >= cfg["max_pages"],
        "errors": errors,
        "nodes": sorted(nodes, key=lambda n: (n["depth"], n["url"])),
    }
    try:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.error("no se pudo escribir %s: %s: %s", args.out, type(e).__name__, e)
        return 2
    print(json.dumps({k: v for k, v in result.items() if k != "nodes"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
