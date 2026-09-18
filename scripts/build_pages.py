"""Regenerate brief.html, heuristic.html and aggregators.html from research/."""
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
brief = (ROOT / "research/brief.html").read_text()
style = re.search(r"<style>.*?</style>", brief, re.S).group(0)
style = style.replace("</style>", "  nav { font: .85rem -apple-system, sans-serif; margin-bottom: 1.5rem; }\n  nav a { margin-right: 1rem; }\n  h3 { font-size: 1.1rem; margin: 1.75rem 0 .5rem; }\n</style>")

NAV = '<nav><a href="./">Deals</a><a href="history.html">History</a><a href="brief.html">Brief</a><a href="heuristic.html">Heuristic</a><a href="aggregators.html">Aggregators</a><a href="research/aggregators.csv">CSV</a></nav>'


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def convert(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("#"):
            n = len(ln) - len(ln.lstrip("#"))
            out.append(f"<h{n}>{inline(ln[n:].strip())}</h{n}>")
            i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="wrap"><table>')
            out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>")
            for r in rows[2:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</table></div>")
        elif re.match(r"^(\d+\.|-) ", ln):
            tag = "ol" if ln[0].isdigit() else "ul"
            items = []
            while i < len(lines) and (re.match(r"^(\d+\.|-) ", lines[i]) or lines[i].startswith("  ")):
                if re.match(r"^(\d+\.|-) ", lines[i]):
                    items.append(re.sub(r"^(\d+\.|-) ", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||\d+\. |- )", lines[i]):
                para.append(lines[i])
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


def page(title, body, raw):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{style}
</head>
<body>
<main>
{NAV}
{body}
<p class="meta">Raw file: <a href="{raw}">{raw}</a></p>
</main>
</body>
</html>
"""


for src, dst, title in [
    ("research/deal-heuristic.md", "heuristic.html", "When is a deal significant?"),
    ("research/aggregators.md", "aggregators.html", "Aggregator and venue map"),
]:
    body = convert((ROOT / src).read_text())
    body = body.replace("<code>aggregators.csv</code>", '<a href="research/aggregators.csv"><code>aggregators.csv</code></a>')
    body = body.replace("<code>deal-heuristic.md</code>", '<a href="heuristic.html"><code>deal-heuristic.md</code></a>')
    (ROOT / dst).write_text(page(title, body, src))

idx = brief.replace("<main>\n", "<main>\n" + NAV + "\n", 1)
idx = idx.replace("</style>", "  nav { font: .85rem -apple-system, sans-serif; margin-bottom: 1.5rem; }\n  nav a { margin-right: 1rem; }\n</style>", 1)
idx = idx.replace("<code>aggregators.md</code>", '<a href="aggregators.html"><code>aggregators.md</code></a>')
idx = idx.replace("<code>aggregators.csv</code>", '<a href="research/aggregators.csv"><code>aggregators.csv</code></a>')
idx = idx.replace("<code>deal-heuristic.md</code>", '<a href="heuristic.html"><code>deal-heuristic.md</code></a>')
(ROOT / "brief.html").write_text(idx)
print("built")
