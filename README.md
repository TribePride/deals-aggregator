# deals-aggregator

A deals newsletter that rebuilds itself every two hours, plus the research behind how it scores.

**Site:** https://tribepride.github.io/deals-aggregator/

## How it works

`.github/workflows/refresh.yml` runs `scripts/refresh.py` at minute 7 of every second hour (UTC). GitHub's scheduler can run 5–30 minutes late. The script:

1. Reads the Slickdeals Frontpage RSS feed, then each new thread's editor "Price Research" line.
2. Scores each deal: reference = price + "$X lower than the next best available price". Discount is cut by 20% because that reference is weaker than real price history. 20%+ is *act now*, 10–20% is *decent*. List prices are never used. Buyer fees are not counted.
3. Marks a deal **significant** when it is decent or better and saves at least $25.
4. Reads the TKTS live board and works out, per show, the price a resale ticket has to beat (15% under TKTS).
5. Writes `data/current.json` (overwritten each run), appends significant deals to `data/history.json` (deduped, capped at 1,000), and rebuilds `feed.xml`.

If one source fails, its last good data stays up with a stale notice. If both fail, nothing is committed.

Run it by hand: `gh workflow run refresh.yml`, or locally `python3 scripts/refresh.py` (stdlib only).

GitHub pauses scheduled workflows after 60 days without repo activity. The bot's own commits should count as activity; if the site stops updating, re-enable the workflow in the Actions tab.

## Not covered

Facebook Marketplace, Craigslist, Theatr and CrowdVolt. Their terms or design rule out scripted reading. The brief explains what to do there instead (alerts, standing bids). The want-list gate, whether you wanted it before you saw the price, can't be automated either.

## Files

| Path | What it is |
|---|---|
| `index.html` | The newsletter; renders `data/current.json` |
| `history.html` | Archive of significant deals; renders `data/history.json` |
| `feed.xml` | Atom feed of significant deals |
| `brief.html`, `heuristic.html`, `aggregators.html` | The research, generated from `research/` by `scripts/build_pages.py` |
| `research/aggregators.csv` | Aggregator and venue map as data, 51 rows |

## Caveats

- Thresholds are inferred, not measured. Tune them in the constants at the top of `scripts/refresh.py`.
- Prices are parsed from deal titles. Bundles and "from $X" titles can parse wrong; deals with no price research are shown unscored, never guessed.
- Research dated 18 September 2026. Reddit and X were not searched, and some tool pricing came from vendor blogs.
