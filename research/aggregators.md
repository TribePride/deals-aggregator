# Aggregator and venue map

Researched 2026-09-18. Full machine-readable table: `aggregators.csv` (51 rows, with an `evidence` column: `fetched`, `search-snippet`, or `background` = my prior knowledge, not re-verified this pass).

The list is grouped by how the price gets set, because that decides what "a deal" means there. See `deal-heuristic.md`.

## 1. Retail with price history (Amazon and friends)

There is no single aggregator to build here. It already exists, and it's good.

| Tool | Job | Cost | Verdict |
|---|---|---|---|
| **Keepa** | Amazon price, Buy Box and Warehouse price history; drop alerts | Free tier; Pro ~€19–29/mo; API from €49/mo | Use. The reference-price source for anything on Amazon |
| **CamelCamelCamel** | Same idea, simpler; email alerts | Free | Use as a second opinion. The two trackers disagree sometimes (PCWorld found highs of $739 vs $570 on one SSD) |
| **Slickdeals** | Humans vote, then paid Deal Editors check price history before Frontpage | Free; keyword alerts; RSS | Use. Frontpage is the closest thing to a pre-scored feed |
| PCPartPicker | Price history for PC parts across retailers | Free | Use for that category |
| Amazon Resale, Woot, Best Buy Open-Box, Back Market, eBay Refurbished, Newegg Open Box | Open-box (typically 10–30% off) and refurb (20–50% off) | n/a | Use, but score against street price, not MSRP |

## 2. Peer-to-peer local (FB Marketplace, Craigslist, OfferUp)

Two different tool types get lumped together as "aggregators":

**Meta-search** (search many sites once): SearchTempest is the one worth keeping. AllCraigslistSearch and Claz duplicate it. These help when you'll drive for something rare. They don't help in NYC for common goods, because the good listings are gone before you search.

**Alert monitors** (tell you within minutes): this is where the value is.

| Tool | Platforms | Alert speed | Price | Verdict |
|---|---|---|---|---|
| FB saved searches (native) | FB | 2–4 hours reported | Free | Baseline. Too slow for contested items |
| Craigslist saved searches (native) | CL | Email, periodic | Free | Use |
| **Flipify** | FB, CL, eBay, OfferUp, Vinted, Kijiji | 1 min (premium) | $5–10 per watchlist/mo | Try first. Newer, unproven |
| Scout | FB (Apple only) | Hourly to instant | $2.99–7.99/mo | Cheap alternative |
| Swoopa | FB, CL, OfferUp, eBay | 5–9 min advertised | $47–352/mo | Skip unless flipping |
| Marketplace Monitor | FB, CL, OfferUp, eBay, Depop, Vinted | 2–5 min | $24.99–169.99/mo | Skip on price |
| CarSnipe | FB, cars | 3–15 min | $9.99–24.99/mo | Cars only |

Caveat: the speed and price table comes from CarSnipe's own blog, a competitor of everything else in it. Treat as directional.

**Reference price source:** eBay sold listings. Every P2P deal gets scored against sold comps, not active asks.

Other venues: Nextdoor, Buy Nothing, Trash Nothing (free stuff, high NYC relevance), EstateSales.net, HiBid/GovDeals/ShopGoodwill (watch the 10–18% buyer premium).

## 3. Tickets (perishable inventory)

**Broadway, cheapest first:** lotteries ($30–60, low odds on hits) → box-office or TodayTix rush ($30–50) → TDF membership ($11–62.50, if eligible) → TKTS (20–50% off, same day) → **Theatr** (at or below what the seller paid) → TickPick/StubHub/SeatGeek all-in.

| Venue | Mechanism | Fees | Notes |
|---|---|---|---|
| **Theatr** | Resale capped at price paid, proof of purchase, escrow until 30 min after curtain | Seller $0. **Buyer fee not published anywhere I could fetch**; one App Store review calls it "very high" | 40% of listings sell inside 10 minutes. Price-point push alerts. Brokers also dump unsold blocks here |
| **CrowdVolt** | Bid/ask exchange, public order book, bid charged only on fill | **Not retrievable** (help centre answers load client-side) | EDM/rave, NYC first. A standing bid is a free option |
| DICE Waitlist, RA resale | Official face-value return queues | Face + original fees | Best price you'll get for sold-out Brooklyn shows; join early |
| CashorTrade | Face value only | Buyer 10% + 3% card; seller $0 | Jam/festival heavy |
| Tixel | Capped at +20% (US) | Unverified | US launch June 2025. Watch |
| TickPick | No added buyer fee | Seller 15% | Use as the honest all-in reference |
| SeatGeek | Deal Score: list price vs modelled fair price | ~37% measured total fee load | Use the score, check all-in elsewhere |
| StubHub / Vivid | Biggest inventory | ~28% / ~31% measured | All-in display required since May 2025 FTC rule; StubHub paid $10M in April 2026 for not complying |
| Gametime | Last-minute, sells until 90 min after start | In price | Its own example: NBA median $127 at T−48h, $40 after tipoff |

## 4. Fashion and gear resale

Aggregators exist and work: **Beni** (50+ partners, claims ~80% of online resale listings, alerts), **Gem**, **Phia**. StockX/GOAT give public sale history, which is a real reference price. Reverb publishes a Price Guide for music gear.

## 5. Other perishables

Too Good To Go (food), HotelTonight (rooms), Going (flights). Same decay logic as tickets.

## What's missing from the market

Nobody scores deals *across* these mechanisms, and nobody covers the NYC-specific ticket venues (Theatr, CrowdVolt, DICE waitlist, RA resale, TKTS board, rush) in one feed. Retail is solved. P2P alerting is solved if you pay. The ticket layer is the open gap.
