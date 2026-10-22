#!/usr/bin/env python3
"""Read-only HTTP/provenance check for the Odoo skill's source manifest."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


class RefreshParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.target = None

    def handle_starttag(self, tag, attrs):
        attrs = {key.lower(): value for key, value in attrs}
        if tag.lower() == "meta" and (attrs.get("http-equiv") or "").lower() == "refresh":
            match = re.search(r"(?:^|;)\s*url\s*=\s*(.+)$", attrs.get("content") or "", re.I)
            if match:
                self.target = match.group(1).strip().strip("\"'")


def check_source(source, timeout=20):
    """Return evidence, keeping HTTP and HTML redirects distinct from body content."""
    result = {"url": source["url"], "category": source["category"]}
    current = source["url"]
    seen = set()
    refreshes = []
    try:
        for _ in range(6):
            if urlsplit(current).scheme not in ("https", "http"):
                raise ValueError("Redirect uses an unsupported URL scheme")
            if current in seen:
                raise ValueError("HTML refresh loop")
            seen.add(current)
            request = Request(current, headers={"User-Agent": "OdooSkillSourceCheck/1.0"})
            with urlopen(request, timeout=timeout) as response:
                body = response.read()
                resolved = response.geturl()
                content_type = response.headers.get("Content-Type", "")
                status = response.status
            parser = RefreshParser()
            if "html" in content_type.lower() or body.lstrip().lower().startswith(b"<html"):
                parser.feed(body.decode("utf-8", errors="replace"))
            if parser.target:
                current = urljoin(resolved, parser.target)
                refreshes.append({"from": resolved, "to": current})
                continue
            digest = hashlib.sha256(body).hexdigest()
            result.update(http_status=status, resolved_url=resolved, content_type=content_type,
                          sha256=digest, html_refreshes=refreshes)
            # Only compare bodies representing the same resource, not a redirect stub.
            previous = source.get("sha256")
            if previous and not source.get("redirect_target"):
                result["content_changed"] = digest != previous
            else:
                result["content_changed"] = None
            return result
        raise ValueError("More than five HTML refreshes")
    except HTTPError as error:
        result.update(http_status=error.code, error=str(error))
    except (URLError, OSError, ValueError) as error:
        result["error"] = str(error)
    result["html_refreshes"] = refreshes
    return result


def positive_int(value):
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=Path(__file__).resolve().parents[1] / "references/source-manifest.json")
    parser.add_argument("--category", help="Check one category, e.g. developer, legal, white-papers")
    parser.add_argument("--limit", type=positive_int, default=20, help="Maximum sources (default: 20)")
    parser.add_argument("--timeout", type=positive_int, default=20, help="Per-request timeout seconds")
    parser.add_argument("--workers", type=positive_int, default=4, help="Concurrent requests (maximum: 6)")
    args = parser.parse_args(argv)
    if args.workers > 6:
        parser.error("--workers must be at most 6")
    try:
        sources = json.loads(args.manifest.read_text())["sources"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(f"Cannot read source manifest: {error}")
    categories = sorted({source["category"] for source in sources})
    if args.category and args.category not in categories:
        parser.error("Unknown category; choose " + ", ".join(categories))
    selected = [source for source in sources if not args.category or source["category"] == args.category]
    selected = selected[:args.limit]
    failures = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for result in executor.map(lambda source: check_source(source, args.timeout), selected):
            print(json.dumps(result, ensure_ascii=False), flush=True)
            failures += int("error" in result)
    print(f"Checked {len(selected)} source(s); {failures} retrieval failure(s). "
          "Changed hashes require review and may reflect dynamic HTML.", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
