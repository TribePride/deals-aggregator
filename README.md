# deals-aggregator

Research on where good deals actually come from in NYC, and a rule for deciding when one is worth acting on. Covers Amazon, Facebook Marketplace, Craigslist, and ticket resale venues such as Theatr and CrowdVolt.

**Site:** https://tribepride.github.io/deals-aggregator/

Researched 18 September 2026.

## What's here

| File | What it is |
|---|---|
| `index.html` | The brief: the read, evidence map, counterargument, next move, sources |
| `heuristic.html` | When a deal is significant: vetoes, reference price, cost, thresholds, eight worked examples |
| `aggregators.html` | Aggregators and venues grouped by how the price gets set |
| `research/aggregators.csv` | The same map as data, 51 rows, with an `evidence` column |
| `research/*.md`, `research/brief.html` | Source files for the pages above |

## Caveats

- The heuristic's structure follows how SeatGeek Deal Score, Slickdeals editors and resellers already judge deals. The numeric thresholds are inferred, not measured.
- Buyer fees are left out of scoring on purpose. Ticket venues differ a lot on fees, so listed-price comparisons lean slightly toward high-fee sites.
- Reddit and X were not searched. Sentiment claims are thin.
- Some tool pricing comes from vendor blogs comparing themselves with competitors. The CSV marks how each row was sourced.
- Most worked examples use illustrative prices.

No code yet. If this becomes a tool, the brief argues for building only the NYC ticket layer.
