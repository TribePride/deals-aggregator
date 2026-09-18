# When is a deal significant?

One sentence: **a deal is significant when the cost is far enough below a reference price you can trust that it still wins after hassle and the chance it goes wrong, and you wanted the thing before you saw the price.**

The discount a seller shows you is never the reference. Amazon's list price, a ticket's face value, and a Marketplace seller's "retails for $900" are all marketing. PCWorld's example: an SSD shown as 57% off a $1,379 list price had never sold above $739 (Keepa) or $570 (CamelCamelCamel).

Status of this document: the structure is grounded in how SeatGeek Deal Score, Slickdeals editors, Keepa users and flippers already judge deals. **The numeric thresholds are my inference**, tuned against the worked examples below. Adjust them after 20 logged decisions.

## Step 0. Vetoes (any one kills it)

- Payment by Zelle, Cash App, Venmo, PayPal F&F, gift card, wire or crypto to a stranger. Recovery is "very unlikely" (FTC/Meta guidance).
- Any deposit or "holding fee" before you've seen the item.
- Seller moves you off-platform, sends a payment/shipping link, or asks for a verification code.
- Shipped P2P item with no platform buyer protection.
- Ticket sold as a screenshot or PDF outside a platform that escrows payment or does official transfer.
- Price is more than ~60% below comps on a high-theft category (phones, bikes, consoles) with a new seller account. Too cheap is a signal too.

## Step 1. Pick the reference price R

| Mechanism | R is | Where to get it | Never use |
|---|---|---|---|
| Retail (Amazon, open-box) | 90-day median price of the *new* item. Also note the all-time low (ATL). For open-box/refurb, R is the new item's ATL, since that's the alternative you'd wait for | Keepa, CamelCamelCamel | List price, "was" price |
| P2P local (FB, Craigslist, OfferUp) | Lower of: median of recent eBay **sold** comps in the same condition (incl. shipping), or the best current new/refurb price × 0.8 | eBay sold filter, Reverb Price Guide, StockX history | Active asking prices, seller's claimed retail |
| Tickets | Cheapest listed price for a comparable seat you could buy right now elsewhere, including primary box office, rush, TKTS | TickPick, box office, TKTS board, CrowdVolt order book and last sale | Face value, price the seller paid |

The ticket row matters most for Theatr. "Below what they paid" is a ceiling on the price, not proof of a deal. If TKTS has the same show at 40% off tonight, a Theatr ticket at 20% below paid is a bad buy.

## Step 2. Cost C

C = price + shipping + travel + expected fix-up

Buyer fees are left out on purpose. Compare listed prices.

- Travel = round-trip hours × your hourly rate (default $25) + fares/car.
- Fix-up = missing parts, cleaning, battery, etc.

## Step 3. Net discount, adjusted

D = (R − C) / R

Then two haircuts:

**Confidence in R**, multiply D by:
- 1.0: 90+ days of price history, or 8+ sold comps
- 0.8: 3–7 comps, or history under 90 days
- 0.5: 1–2 comps, or only active listings

**Risk**, subtract p × C / R, where p is the chance you lose the money:
- 0–2%: retailer returns, platform escrow (Theatr, CrowdVolt, TickPick)
- 5%: in-person, inspected, cash
- 15%: in-person, can't fully test (electronics without power, sealed box)

## Step 4. Tier by mechanism

| Tier | Retail | P2P local | Tickets |
|---|---|---|---|
| Ignore | D < 10% | D < 25% | D < 15% |
| Decent (buy if already wanted) | 10–20% | 25–40% | 15–30% |
| Act now | ≥ 20% **and** at or below prior ATL | ≥ 40% | ≥ 30%, or any D > 0 on a sold-out show with no rush/lottery |

Why the bars differ. Retail comes with returns and warranty, so a smaller gap is real money. P2P has no returns, no warranty, and costs you a trip, so the bar is higher; flippers use "30% spread minimum" and "resale ≥ 2× cost" (a 50% discount), and a personal buyer sits between those. Tickets are in between: escrowed but non-returnable.

## Step 5. Significance gates

A tier only counts as **significant** if all three hold:

1. **Dollar floor.** R − C ≥ max($25, 2 × hours of hassle × hourly rate). Forty percent off a $12 item isn't worth an alert.
2. **Want-list.** The item or show was on your list before you saw the price. If not, require one tier higher. This is the only defence against deals making you spend more.
3. **Exit floor (bonus, not required).** If you could resell at ≥ C after fees, the downside is near zero. Bump one tier.

## Step 6. Time rules for perishables

- Bottom-quartile-demand events drop ~30% on the day; across all events day-of averages 33% below the mean price. High-demand events hold ~99% of peak on the day. So: **wait on weak shows, don't wait on hot ones.**
- Proxy for demand: primary still on sale, or many listings at or below face = weak. Sold out + thin listings = hot.
- On a bid/ask venue (CrowdVolt), place a bid at your "act now" price as soon as you want the event. It costs nothing unless filled. Raise it toward "decent" inside 48 hours.
- On Theatr, 40% of listings sell within 10 minutes. Decide your price per show in advance and set the price-point alert; you won't have time to research when it fires.
- Same for P2P: run comps when you create the alert, not when it fires.

## Worked examples

Prices marked (hyp.) are illustrative; the rest come from sources.

1. **Amazon SSD, "57% off $1,379"** → price ≈ $593. Trackers show it never sold above $570–739; say 90-day median $600 (hyp.). D = 1%. **Ignore.** The rule correctly rejects a fake discount.
2. **Amazon headphones** (hyp.): 90-day median $278, ATL $228, now $219. D = 21%, below ATL, history > 90 days. Savings $59 ≥ $25. **Act now** if on the want-list, otherwise decent.
3. **Best Buy open-box TV** (hyp.): $640 vs $800 street. D = 20%. But open-box normally runs 10–30% off, and ATL for new was $699, so gap to the real alternative is 8%. **Ignore to decent.** Score open-box against the new item's ATL, not its median.
4. **FB Marketplace Aeron chair, Queens** (hyp.): ask $250. Eight eBay sold comps, median $520. Travel 1.5 h × $25 + $40 car = $77.50. C = $327.50. D = 37%; risk 5% × 327.5/520 = 3%. Net 34%. Savings $192 ≥ $75. **Decent.** Offer $200: C = $277.50, net 44%. **Act now.**
5. **Craigslist iPhone, 65% under comps, "will ship, Zelle only."** **Veto.** Never scored.
6. **Theatr, show with seats at TKTS** (hyp.): seller paid $189, asks $120. TKTS same section tonight at 30% off = $132. R = $132. D = 9%. **Ignore**, despite being 37% "below face."
7. **Theatr, sold-out show** (hyp.): same $120 ask; cheapest comparable on TickPick $260. D = 54%, escrowed. **Act now**, and you have about ten minutes.
8. **CrowdVolt, Brooklyn show 9 days out** (hyp.): primary still selling at $70. Lowest ask $95, last sale $80. R = $70. Buying the ask is D = −36%: **ignore**. Bid $55: D = 21% if filled. **Place the bid**; if primary sells out, R resets to the lowest ask elsewhere and you re-score.

## What to log (so the thresholds can be tuned)

Per decision: date, venue, item, R and its source, C, D, tier, bought y/n, and one week later: regret y/n. Twenty rows is enough to see if a bar is too high or too low.
