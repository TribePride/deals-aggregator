#!/usr/bin/env python3
"""Fetch deals, score them with the heuristic in research/deal-heuristic.md,
and write data/current.json, data/history.json and feed.xml.

Stdlib only. Sources: Slickdeals Frontpage RSS (+ each thread's editor
"Price Research" line) and the TKTS live board.
"""
import html
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = "https://tribepride.github.io/deals-aggregator/"
UA = "deals-aggregator/1.0 (+https://github.com/TribePride/deals-aggregator)"

SD_RSS_URL = os.environ.get(
    "SD_RSS_URL",
    "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1",
)
TKTS_URL = os.environ.get(
    "TKTS_URL", "https://www.tdf.org/discount-ticket-programs/tkts-by-tdf/tkts-live/"
)
THREAD_DELAY = float(os.environ.get("THREAD_DELAY", "2"))

# Heuristic constants (retail column of research/deal-heuristic.md)
CONFIDENCE = 0.8  # next-best-price reference is weaker than 90-day history
DECENT, ACT_NOW = 0.10, 0.20
DOLLAR_FLOOR = 25
TICKET_BEAT_BY = 0.15
HISTORY_CAP = 1000


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def blurb(desc, limit=170):
    """Short plain description from the RSS summary: no URLs, no markup."""
    t = re.sub(r"https?://\S+", "", desc).replace("*", "")
    t = re.sub(r"\s*\[[^\]]*\]", "", t)  # "[walmart.com]"
    t = re.sub(r"^.{2,60}? (?:has|have|is offering|offers) ", "", t)  # store is shown separately
    t = t[:1].upper() + t[1:]
    t = re.sub(r"\s+", " ", t).strip(" .")
    if len(t) > limit:
        t = t[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return t or None


def money(s):
    return float(s.replace(",", ""))


# ---------- Slickdeals ----------

def parse_rss(xml_text):
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    items = []
    for it in ET.fromstring(xml_text).iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").split("?")[0]
        guid = (it.findtext("guid") or "").strip()
        m = re.search(r"(\d+)", guid) or re.search(r"/f/(\d+)", link)
        if not m:
            continue
        desc = strip_tags(it.findtext("description") or "")
        body = it.findtext("content:encoded", default="", namespaces=ns)
        img = re.search(r'<img[^>]+src="(https://[^"]+)"', body)
        thumbs = re.search(r"Thumb Score:\s*\+?(-?\d+)", body)
        # "$49+" is a free-shipping threshold, not the price
        prices = re.findall(r"\$\s?(\d[\d,]*(?:\.\d+)?)(?!\+|[\d,.]*\d\+)", title)
        store = re.match(r"^(.{2,60}?) (?:has|have|is offering|offers)\b", desc)
        try:
            posted = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc).isoformat()
        except Exception:
            posted = None
        items.append({
            "id": m.group(1),
            "title": title,
            "url": f"https://slickdeals.net/f/{m.group(1)}",
            "price": money(prices[-1]) if prices else None,
            "store": re.sub(r"\s*\[[^\]]*\]", "", store.group(1)).strip() if store else None,
            "thumbs": int(thumbs.group(1)) if thumbs else None,
            "posted": posted,
            "image": img.group(1) if img else None,
            "blurb": blurb(desc),
        })
    return items


RESEARCH_RE = re.compile(
    r"\$\s?(\d[\d,]*(?:\.\d+)?)\s+(?:lower|less)\b[^$]{0,80}?next best available price", re.I
)
NOTE_RE = re.compile(r"(This (?:price|offer) (?:is \$[\d.,]+ lower than|matches) the (?:previous|recent|last) Frontpage [Dd]eal)", re.I)


def parse_thread(page):
    text = strip_tags(page)
    out = {"savings": None, "note": None}
    m = RESEARCH_RE.search(text)
    if m:
        out["savings"] = money(m.group(1))
    n = NOTE_RE.search(text)
    if n:
        out["note"] = n.group(1)
    return out


def score(item):
    price, savings = item.get("price"), item.get("savings")
    if not price or not savings:
        item.update(reference=None, discount=None, tier="unscored", significant=False)
        return item
    ref = round(price + savings, 2)
    d = (ref - price) / ref * CONFIDENCE
    tier = "act_now" if d >= ACT_NOW else "decent" if d >= DECENT else "ignore"
    item.update(
        reference=ref,
        discount=round(d, 4),
        tier=tier,
        significant=tier != "ignore" and savings >= DOLLAR_FLOOR,
    )
    return item


def slickdeals(previous):
    cache = {d["id"]: d for d in previous.get("deals", [])}
    items = parse_rss(fetch(SD_RSS_URL))
    first = True
    for it in items:
        old = cache.get(it["id"])
        if old and old.get("savings") is not None and old.get("price") == it["price"]:  # unscored threads get re-checked
            it["savings"], it["note"] = old.get("savings"), old.get("note")
        else:
            if not first:
                time.sleep(THREAD_DELAY)
            first = False
            try:
                it.update(parse_thread(fetch(it["url"])))
            except Exception as e:  # one bad thread shouldn't sink the issue
                print(f"thread {it['id']} failed: {e}", file=sys.stderr)
                it.update(savings=None, note=None)
        score(it)
    order = {"act_now": 0, "decent": 1, "ignore": 2, "unscored": 3}
    items.sort(key=lambda d: (order[d["tier"]], not d["significant"], -(d.get("discount") or 0)))
    return items


# ---------- TKTS ----------

TOKEN_RE = re.compile(
    r'<h2[^>]*>(?P<booth>.*?)</h2>'
    r'|class="tkts__board tkts__board--(?P<board>[a-z\-]+)"'
    r'|class="tkts__notice tkts__notice--(?P<status>open|closed)"[^>]*>(?P<notice>.*?)</div>'
    r'|<li class="tkts__grid-list-item">(?P<item>.*?)</li>',
    re.S,
)
BOARDS = {
    "broadway": ("Broadway", "today"),
    "off": ("Off-Broadway", "today"),
    "tomorrow-broadway": ("Broadway", "tomorrow matinee"),
    "tomorrow-off": ("Off-Broadway", "tomorrow matinee"),
}


def field(chunk, name):
    m = re.search(rf'class="tkts__grid-list-item__{name}"[^>]*>(.*?)</div>', chunk, re.S)
    return strip_tags(m.group(1)) if m else None


def tkts():
    page = fetch(TKTS_URL)
    booths, shows = [], []
    booth = board = None
    for m in TOKEN_RE.finditer(page):
        if m.group("booth") is not None:
            name = strip_tags(m.group("booth"))
            booth = name if re.match(r"TKTS\s+(Times Square|Lincoln Center)", name) else None
            board = None
            if booth:
                booth = re.sub(r"\s+", " ", booth)
                booths.append({"name": booth, "status": None, "notice": None})
        elif m.group("status") and booth:
            booths[-1].update(status=m.group("status"), notice=strip_tags(m.group("notice")))
        elif m.group("board"):
            board = m.group("board")
        elif m.group("item") and booth and board in BOARDS:
            chunk = m.group("item")
            link = re.search(r'href="([^"]+)"', chunk)
            prices = [money(p) for p in re.findall(r"\$\s?(\d[\d,]*(?:\.\d+)?)", field(chunk, "discount") or "")]
            kind, when = BOARDS[board]
            shows.append({
                "booth": booth,
                "kind": kind,
                "when": when,
                "show": field(chunk, "title"),
                "url": link.group(1) if link else None,
                "percent_off": field(chunk, "percent"),
                "price_low": min(prices) if prices else None,
                "price_high": max(prices) if prices else None,
                "time": field(chunk, "time"),
                "beat_price": round(min(prices) * (1 - TICKET_BEAT_BY)) if prices else None,
            })
    if not booths:
        raise RuntimeError("TKTS page parsed to zero booths; markup may have changed")
    return {"booths": booths, "shows": shows}


# ---------- outputs ----------

def load(path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def update_history(history, deals, now):
    by_id = {h["id"]: h for h in history}
    for d in deals:
        if not d["significant"]:
            continue
        keep = {k: d[k] for k in ("id", "title", "url", "store", "price", "reference", "savings", "discount", "tier", "thumbs", "image", "blurb")}
        if d["id"] in by_id:
            by_id[d["id"]].update(keep, last_seen=now)
        else:
            by_id[d["id"]] = dict(keep, first_seen=now, last_seen=now)
    out = sorted(by_id.values(), key=lambda h: h["first_seen"], reverse=True)
    return out[:HISTORY_CAP]


def atom(history, now):
    esc = lambda s: html.escape(str(s), quote=True)
    entries = []
    for h in history[:50]:
        summary = (
            f"${h['price']:g} vs ${h['reference']:g} next-best price. "
            f"Saves ${h['savings']:g}, adjusted discount {h['discount'] * 100:.0f}%. "
            f"{'Act now' if h['tier'] == 'act_now' else 'Decent'}."
        )
        entries.append(
            f"<entry><id>{esc(h['url'])}</id><title>{esc(h['title'])}</title>"
            f"<link href=\"{esc(h['url'])}\"/><updated>{h['first_seen']}</updated>"
            f"<summary>{esc(summary)}</summary></entry>"
        )
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">'
        f"<title>Significant deals</title><id>{SITE}</id><link href=\"{SITE}\"/>"
        f"<link rel=\"self\" href=\"{SITE}feed.xml\"/><updated>{now}</updated>"
        "<author><name>deals-aggregator</name></author>" + "".join(entries) + "</feed>\n"
    )


def main():
    DATA.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    previous = load(DATA / "current.json", {})
    sources = dict(previous.get("sources", {}))
    current = {"deals": previous.get("deals", []), "tkts": previous.get("tkts", {"booths": [], "shows": []})}
    failures = 0

    for name, key, fn in (("slickdeals", "deals", lambda: slickdeals(previous)), ("tkts", "tkts", tkts)):
        try:
            current[key] = fn()
            sources[name] = {"ok": True, "fetched": now}
        except Exception as e:
            failures += 1
            print(f"{name} failed: {e}", file=sys.stderr)
            sources[name] = {"ok": False, "fetched": sources.get(name, {}).get("fetched"), "error": str(e)[:200]}

    if failures == 2:
        print("both sources failed; nothing written", file=sys.stderr)
        return 1

    history = load(DATA / "history.json", [])
    if sources["slickdeals"]["ok"]:
        history = update_history(history, current["deals"], now)

    out = {"generated": now, "refresh_hours": 2, "sources": sources, **current}
    (DATA / "current.json").write_text(json.dumps(out, indent=1) + "\n")
    (DATA / "history.json").write_text(json.dumps(history, indent=1) + "\n")
    (ROOT / "feed.xml").write_text(atom(history, now))

    tiers = {}
    for d in current["deals"]:
        tiers[d["tier"]] = tiers.get(d["tier"], 0) + 1
    print(f"{now} deals={tiers} significant={sum(d['significant'] for d in current['deals'])} "
          f"tkts_shows={len(current['tkts']['shows'])} history={len(history)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
