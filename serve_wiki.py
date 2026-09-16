#!/usr/bin/env python3
"""Simple local server that renders the wiki as browsable HTML.

Usage:

    python3 serve_wiki.py [--host 127.0.0.1] [--port 8000]

Serves the repository root so that relative links between wiki/ and
the repo's own docs (which wiki pages cite as sources) all resolve.
Markdown files are rendered to a small styled HTML page;
everything else (charts, dashboard.html, images) is served as a static
file. Stdlib only - no dependencies.
"""

import argparse
import html
import mimetypes
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parent

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{ font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
       max-width: 840px; margin: 24px auto; padding: 0 20px;
       color: #1a1a1a; line-height: 1.55; }}
nav {{ font-size: 14px; padding-bottom: 8px; border-bottom: 1px solid #eee; }}
nav a {{ margin-right: 16px; text-decoration: none; }}
h1, h2, h3, h4 {{ line-height: 1.25; margin-top: 1.4em; }}
a {{ color: #0b5cad; }}
code {{ background: #f3f3f3; padding: 1px 4px; border-radius: 3px;
        font-size: 0.92em; }}
pre {{ background: #f6f6f6; border: 1px solid #e5e5e5; padding: 10px 12px;
       overflow-x: auto; }}
pre code {{ background: none; padding: 0; }}
blockquote {{ border-left: 3px solid #ccc; margin-left: 0;
              padding: 2px 14px; color: #555; }}
table {{ border-collapse: collapse; }}
th, td {{ border: 1px solid #ddd; padding: 5px 10px; text-align: left; }}
footer {{ margin-top: 40px; font-size: 12px; color: #888;
          border-top: 1px solid #eee; padding-top: 8px; }}
li {{ margin: 3px 0; }}
</style>
</head>
<body>
<nav><a href="/wiki/index.md">Field guide wiki</a>
<a href="{raw_url}">raw markdown</a></nav>
{body}
<footer>Rendered by serve_wiki.py from {src}</footer>
</body>
</html>"""


# --------------------------------------------------------------------------
# minimal markdown renderer (headings, lists, quotes, fenced code, tables,
# links, code spans, bold - enough for this repo's docs, which avoid italics)
# --------------------------------------------------------------------------

CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
UL_ITEM_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
OL_ITEM_RE = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
HR_RE = re.compile(r"^ {0,3}(?:(?:-\s*){3,}|(?:\*\s*){3,})$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}.*\|.*$")


def inline(text):
    out = html.escape(text, quote=False)
    codes = []

    def stash(m):
        codes.append(f"<code>{m.group(1)}</code>")
        return f"\x00{len(codes) - 1}\x00"

    out = CODE_RE.sub(stash, out)

    def link(m):
        url = m.group(2)
        return f'<a href="{html.escape(url, quote=True)}">{m.group(1)}</a>'

    out = LINK_RE.sub(link, out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], out)
    return out


def md_to_html(text):
    lines = text.split("\n")
    out = []
    i = 0
    list_stack = []  # (indent, tag)

    def close_lists(to_indent=None):
        while list_stack and (to_indent is None or list_stack[-1][0] > to_indent):
            out.append(f"</{list_stack.pop()[1]}>")

    while i < len(lines):
        line = lines[i]

        if line.lstrip().startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].lstrip().startswith("```"):
                block.append(lines[i])
                i += 1
            close_lists()
            out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
            i += 1
            continue

        m = HEADING_RE.match(line)
        if m:
            close_lists()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if HR_RE.match(line):
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        if line.lstrip().startswith(">"):
            close_lists()
            quote = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + md_to_html("\n".join(quote)) + "</blockquote>")
            continue

        ul, ol = UL_ITEM_RE.match(line), OL_ITEM_RE.match(line)
        if ul or ol:
            m = ul or ol
            indent, content = len(m.group(1)), m.group(2)
            tag = "ul" if ul else "ol"
            while list_stack and list_stack[-1][0] > indent:
                out.append(f"</{list_stack.pop()[1]}>")
            if list_stack and list_stack[-1][0] < indent:
                list_stack.append((indent, tag))
                out.append(f"<{tag}>")
            elif list_stack and list_stack[-1][1] != tag:
                out.append(f"</{list_stack.pop()[1]}><{tag}>")
                list_stack.append((indent, tag))
            elif not list_stack:
                list_stack.append((indent, tag))
                out.append(f"<{tag}>")
            out.append(f"<li>{inline(content)}</li>")
            i += 1
            continue

        if "|" in line and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            close_lists()

            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]

            header = cells(line)
            i += 2
            body_rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                body_rows.append(cells(lines[i]))
                i += 1
            out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header)
                       + "</tr>")
            for row in body_rows:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            out.append("</table>")
            continue

        if not line.strip():
            close_lists()
            i += 1
            continue

        close_lists()
        para = [line]
        while (i + 1 < len(lines) and lines[i + 1].strip()
               and not HEADING_RE.match(lines[i + 1])
               and not UL_ITEM_RE.match(lines[i + 1])
               and not OL_ITEM_RE.match(lines[i + 1])
               and not lines[i + 1].lstrip().startswith(("```", ">"))
               and not ("|" in lines[i + 1] and i + 2 < len(lines)
                        and TABLE_SEP_RE.match(lines[i + 2]))):
            i += 1
            para.append(lines[i])
        out.append("<p>" + inline(" ".join(p.strip() for p in para)) + "</p>")
        i += 1

    close_lists()
    return "\n".join(out)


# --------------------------------------------------------------------------
# http server
# --------------------------------------------------------------------------

def first_heading(text, fallback):
    for line in text.split("\n"):
        m = HEADING_RE.match(line)
        if m:
            return m.group(2)
    return fallback


class WikiHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):  # quieter console
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        query = parse_qs(parsed.query)
        want_raw = query.get("raw", ["0"])[0] == "1"

        if path in ("", "/"):
            return self.serve_markdown(ROOT / "wiki" / "index.md", want_raw)

        target = (ROOT / path.lstrip("/")).resolve()
        if ROOT not in target.parents and target != ROOT:
            return self.send_error_page(403, "Forbidden")
        if not target.exists():
            return self.send_error_page(404, f"No file at {path}")

        if target.is_dir():
            return self.send_listing(target, path)

        if target.suffix == ".md" and not want_raw:
            return self.serve_markdown(target, want_raw)

        ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_markdown(self, path, want_raw):
        if not path.exists():
            return self.send_error_page(404, f"No file at /{path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        rel = "/" + path.relative_to(ROOT).as_posix()
        title = first_heading(text, path.stem)
        body = ("<pre>" + html.escape(text) + "</pre>") if want_raw \
            else md_to_html(text)
        page = PAGE.format(title=html.escape(title), raw_url=rel + "?raw=1",
                           body=body, src=html.escape(rel))
        self.send_html(page.encode("utf-8"))

    def send_listing(self, target, path):
        entries = sorted(p for p in target.iterdir() if not p.name.startswith("."))
        items = []
        if path.strip("/") not in ("",):
            items.append('<li><a href="../">../</a></li>')
        for p in entries:
            name = p.name + ("/" if p.is_dir() else "")
            href = p.name + ("/" if p.is_dir() else "")
            items.append(f'<li><a href="{href}">{html.escape(name)}</a></li>')
        page = PAGE.format(
            title=html.escape(path or "/"), raw_url="#",
            body=f"<h1>{html.escape(path or '/')}</h1><ul>{''.join(items)}</ul>",
            src="directory listing")
        self.send_html(page.encode("utf-8"))

    def send_error_page(self, code, message):
        page = PAGE.format(title=f"{code}", raw_url="#",
                           body=f"<h1>{code}</h1><p>{html.escape(message)}</p>",
                           src="error")
        self.send_html(page.encode("utf-8"), code=code)

    def send_html(self, body, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    ap = argparse.ArgumentParser(description="Serve the wiki as HTML.")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), WikiHandler)
    print(f"Serving {ROOT}")
    print(f"  wiki:    http://{args.host}:{args.port}/wiki/index.md")
    server.serve_forever()


if __name__ == "__main__":
    main()
