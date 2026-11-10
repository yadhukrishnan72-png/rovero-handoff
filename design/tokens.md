# Design tokens

Defined at the top of `pages/destination.css` as CSS variables.

## Colour

| Token | Value | Use |
|---|---|---|
| `--rv-brand` | `#6415FE` | primary purple: buttons, selected states, links |
| `--rv-brand-dark` | `#6D00FB` | button hover |
| `--rv-tint` | `#F1EAFF` | pale purple surfaces: notices, chips, price pill when selected |
| `--rv-ink` | `#111827` | body text and headings |
| `--rv-muted` | `#5F6672` | secondary text |
| `--rv-line` | `#E9E9E9` | borders and dividers |
| `--rv-bg` | `#F7F7F7` | page background |
| `--rv-card` | `#FFFFFF` | cards and tiles |

Local-plan badge (gold lightning): tile `#FFF4D9`, bolt `#F0B100` (see `assets/icons/local-plan.svg`).

## Type

- Family: **Plus Jakarta Sans**, weights 400 / 500 / 600 / 700 / 800 (Google Fonts).
- Page title: `clamp(2.25rem, 5vw, 3.5rem)`, weight 800, tight tracking.
- Section titles: `clamp(1.5rem, 3vw, 2rem)`, weight 800.
- Plan size on a tile: 1.75rem, weight 800 (1.25rem on phones).

## Shape and spacing

- Radius: tiles 16px, cards 20 to 28px, buttons and pills fully round.
- Page width: 1120px max, 1.25rem side padding.
- Desktop buying column: 36rem max width so the square plan tiles stay a comfortable size.

## Plan tiles

- Square (`aspect-ratio: 1`), three per row at every width, 0.75rem gap (0.625rem on phones).
- Content order: size, optional extras (voice/SMS or per-day allowance), days, countries link (regions), price pill.
- Selected: purple border, faint purple background, check badge top-right. Local plan: gold badge top-left (on the corner on phones).
- Each tile is one invisible overlay button (the radio) plus a separate countries button above it.

## Notices (callouts)

Soft purple boxes (`--rv-tint`, 14px radius) with an icon: Unlimited allowance, Local plan, and "Install before you fly".

## Countries sheet

Bottom sheet on phones (full width, rounded top), centred 34rem dialog from 700px up. Search field, two-column alphabetical list,
footer button "Choose this plan" (selects that plan) or "Done" (if it is already selected).
