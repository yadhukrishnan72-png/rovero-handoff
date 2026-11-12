# Rovero destination pages: developer handoff

One page template for every **country** and **region** eSIM page, the artwork for all 246 destinations, and the data
format that drives them. No build step: it is plain HTML, CSS and JavaScript.

## Try it (30 seconds)

Open `pages/destination.html` in a browser with a destination code, for example:

| Page | Open |
|---|---|
| Indonesia (country) | `pages/destination.html?d=id` |
| Japan (country) | `pages/destination.html?d=jp` |
| Netherlands (country) | `pages/destination.html?d=nl` |
| Europe (region, with a countries sheet) | `pages/destination.html?d=eu` |
| Africa (region) | `pages/destination.html?d=af-21` |

Double-clicking the file works. If your browser blocks local scripts, run `python -m http.server` in this folder and open
`http://localhost:8000/pages/destination.html?d=eu`.

## What is in the folder

```
pages/
  destination.html     the single template (country AND region)
  destination.css      all styles (brand tokens at the top)
  destination.js       fills the template from data, runs the plan picker, tabs and countries sheet
data/
  pages/<code>.js      example page data (id, jp, nl, eu, af-21). This is the format to produce from your real data
  destinations.csv     all 246 destinations: code, kind, name, scene file, scene type, landmark, notes
assets/
  destinations/        246 scene illustrations, one SVG per destination, named by lower-case code (id.svg, af-21.svg ...)
  icons/local-plan.svg the gold lightning badge
design/tokens.md       colours, type, spacing, component notes
tools/                 optional: the generator that made the scenes (see tools/README.md)
```

## How a page is built

`destination.html` contains the full markup. Anything that differs per destination is one of:

- a token: `{name}` (for example "Netherlands") and `{the}` (for example "the Netherlands", used mid-sentence);
- a block marked `data-for="country"` or `data-for="region"`, shown only for that kind;
- a section filled from data: hero image, networks row, related-destinations card, plan tiles, notices, countries sheet.

`destination.js` reads `window.ROVERO_PAGE` and does the rest. The demo loader at the bottom of `destination.html` reads
`?d=<code>` and loads `data/pages/<code>.js`. **In production, render the same markup from your own data and remove that loader.**

### Page data format (`window.ROVERO_PAGE`)

```js
{
  code: 'eu',                       // lower-case destination code, matches the asset file name
  kind: 'region',                   // 'country' | 'region'
  name: 'Europe',                   // shown in titles and the breadcrumb
  the: 'Europe',                    // name for mid-sentence use ('the Netherlands')
  image: '../assets/destinations/eu.svg',
  alt: 'Illustration: ...',
  networks: [{ name: '...', tech: '4G / 5G' }],     // countries only; omit or [] to hide the row
  plans: { data: [ ...plan ], voice: [ ...plan ], unlimited: [ ...plan ] },
  coverage: { 'eu-42': ['Austria', 'Belgium', ...] },   // regions only: country names per coverage group
  unlimitedNote: { strong: '2 GB of high-speed data every day.', text: ' After that, speed reduces to 1 MB/s.' },
  related: [{ label: 'Global', href: '/destinations/gl-120', image: '../assets/destinations/gl-120.svg' }],
  relatedTitle: 'Explore more eSIM plans',      // optional
  relatedText: '...'                            // optional
}
```

A **plan**:

| Field | Meaning |
|---|---|
| `gb`, `days`, `price` | required. `gb` is shown as is ('5 GB', 'Unlimited'); `price` is a number in USD |
| `coverage` | regions: key into `coverage`. The tile shows "N countries ›", which opens the countries sheet |
| `voice`, `sms` | Data + Voice plans: '200 min', '50 SMS' |
| `perDay` | Unlimited plans: shown on the tile ('2 GB/day') |
| `tag` | pill on the tile ('Most popular'). The first tagged plan is preselected on each tab |
| `local` | `true` shows the gold lightning badge and the "Local plan" notice on that tab |
| `global` | `true` shows the blue globe badge on the tile. While that plan is selected, a "Global plan" notice appears with a "See all countries" link that opens a searchable popup of `globalCountries` (a top-level array in the page data; the count is taken from it). Without `globalCountries` the notice stays hidden |
| `number` | `{ country: 'France', code: '+33' }` on a global Data + Voice plan: says which country's phone number the plan includes. Shown in the Global notice ("Includes a France phone number (+33).", replacing the speeds line). Plans without it keep "Speeds depend on the partner network." |
| `more` | `true` hides the plan until the **"More plans"** link under the tiles is pressed (used for the 100 MB plan). It is never the preselected plan |

Rules that follow from the data (nothing is hardcoded to sizes, counts or countries):
- The tab bar shows only the plan kinds that exist (Data / Data + Voice / Unlimited). One kind means no tab bar.
- Any number of tiles works (three per row, always square). Countries and regions can have different plans.
- The Unlimited notice shows on the Unlimited tab; the Local-plan notice shows on any tab with a `local` plan.

### Hooks for checkout

`destination.js` fires events on `document`:
- `rovero:select`: `{ kind, plan }` whenever the selected plan changes;
- `rovero:pay`: `{ kind, plan, page }` when "Pay now" is pressed. **Nothing is wired to checkout yet.**

## Which plans to show (supplier: eSIM Access)

Only import these plans from the eSIM Access API and skip everything else:

- **Data:** 1 GB (7 days), 3 GB (15 days), 5 GB, 10 GB, 20 GB and 50 GB (all 30 days).
  The **100 MB (7 days)** plan is not shown in the main list: flag it `more: true` so it sits under "More plans".
- **Unlimited:** only the "Unlimited, 2 GB per day" plan (speed reduces after the daily limit).
- **Duplicates:** if two plans have the same GB, validity and price, one is probably roaming and the other uses a local network.
  Keep the **local** plan and mark it `local: true` (gold lightning badge).
- **Networks row** (country pages): get the supported network(s) and their speed (4G / 5G) from the API.

(1 GB validity was assumed to be 7 days; confirm.)

## Adding a destination

1. Make sure `assets/destinations/<code>.svg` exists (all 246 do).
2. Add `data/pages/<code>.js` in the format above (copy `jp.js` for a country or `eu.js` for a region).
3. Open `pages/destination.html?d=<code>`.

## Scene artwork

- 246 static SVGs, 1000x1250 (4:5), 3 to 35 KB each. Own artwork: **no photographer credit is needed**.
- Used as the hero image. On desktop the slot is 4:5; on phones it is wide (`object-fit: cover` crops from the middle, and every
  subject sits in the middle band so it stays visible).
- Contested places (for example Israel, Taiwan, Kosovo, Armenia) use neutral scenes with no flags or contested symbols.
- `data/destinations.csv` lists each destination's scene type and landmark. The generator in `tools/` can rebuild or restyle them.

## Placeholders and open items (please read)

All sample data is **placeholder**. Replace before launch:

- [ ] **Plans**: sizes, prices, validity, Data + Voice minutes/SMS, Unlimited allowance and the 1 MB/s throttle wording.
- [ ] **Local-plan flags** (`local: true`) and the claim "Connects to local networks for faster speeds": confirm the wording.
- [ ] **Networks** (country pages): carrier names per country. The examples use a neutral "Local partner networks" chip.
- [ ] **Region country lists**: Europe's lists come from the coverage groups of the supplier plan file (EU-30 / EU-33 / EU-42); which retail plan uses which group is a guess.
  Africa's 21 countries are placeholder names.
- [ ] **Links**: header, footer and related-destination paths (`/destinations`, `/what-is-an-esim`, ...) are guesses; confirm against the real site.
- [ ] **Checkout**: connect `rovero:pay` to payment.
- [ ] **Site-wide copy** (FAQ, "How it works", "Which traveller are you?", Plan details) is generic; adjust to the real policy.
- [ ] **SEO**: titles, meta descriptions and structured data are filled client-side in this demo; render them server-side in production.

## Browser notes

Uses the native `<dialog>` element for the countries sheet (all current browsers), `aspect-ratio`, and CSS `:has()`
(scroll lock while the sheet is open). Respects `prefers-reduced-motion`. Tile selection is keyboard accessible
(arrow keys move between tiles); each tile is one radio button with a separate "countries" button.

## Credits and licences

- Scene illustrations: created for Rovero (no third-party artwork or photographs in this folder).
- Font: Plus Jakarta Sans via Google Fonts (SIL Open Font License).
- No supplier price data, competitor data or third-party photographs are included.
