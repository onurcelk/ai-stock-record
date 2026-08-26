# Obsidian — Design Manifesto

A dark-only, full-animation, minimal design language for the AI Stock project's
future frontends. This document is the ground truth. Any new UI in this project
either follows it or amends it explicitly — it is not decoration to be
reinterpreted per page.

Status: adopted 2026-08-21. Applies to new frontend work only. Does not touch
`Stock-Prediction-Models/app` (Streamlit, incompatible with these libraries) or
`placely` (separate project, its own light-theme rule stands untouched).

## Premise

Three source libraries, cloned into `design-system/references/` for study —
never imported as a dependency tree wholesale, always read and re-authored:

- **[motion](references/motion)** (npm package `motion`, import from
  `motion/react`) — the animation engine. Every transition, gesture, and
  scroll-linked effect in this system reduces to `motion`'s primitives:
  `motion.*` components, `AnimatePresence`, `useScroll`/`useTransform`,
  spring physics. Nothing here hand-rolls easing curves or requestAnimationFrame
  loops motion already solves.
- **[kokonutui](references/kokonutui)** — the interaction/effect vocabulary.
  Source for text and background treatments (`shimmer-text`, `glitch-text`,
  `type-writer`, `beams-background`, `background-paths`, `flow-field`),
  structural blocks (`bento-grid`, `morphic-navbar`, `spotlight-cards`,
  `liquid-glass-card`), and controls (`gradient-button`, `hold-button`,
  `attract-button`, `smooth-tab`, `toolbar`). Copy-paste registry, not an npm
  dependency — components get pulled in, stripped down, and re-skinned to this
  manifesto's tokens, not used as-is with their default theme.
- **[bklit-ui](references/bklit-ui)** — the data-density vocabulary, for when
  this system meets an actual dashboard. Full chart family already built for
  financial-shaped data: `candlestick-chart`, `live-line-chart`, `area-chart`,
  `bar-chart`, `gauge-chart`, `ring-chart`, `funnel-chart`, `heatmap-chart`,
  plus `stat-card-*` blocks. This is what a future scorecard/leaderboard/
  price-history page is built from — not reinvented.

Division of labor: **motion drives, kokonutui dresses, bklit-ui measures.**
If a component needs to move, it's motion. If it needs a look, start from
kokonutui. If it needs to plot numbers, start from bklit-ui.

## Why dark-only (no toggle)

A light mode is a second design system — every surface, shadow, and contrast
ratio gets re-derived, and animation timing that reads as "smooth" on black
often reads as "laggy" on white because perceived contrast changes with
luminance. Committing to one mode is what makes "full animational" affordable:
every motion spec below is tuned against a single background value. Do not
add `prefers-color-scheme: light` support or a theme switch. `color-scheme:
dark` is set at the root and that is the only mode that exists.

## Color

Near-black, not pure black — pure black plus white text causes halation and
looks harsh once things start moving. One accent. Financial semantics get
their own reserved pair, separate from the accent, because up/down has to
stay legible even for a user who is colorblind to the accent hue.

| Token | Value | Use |
|---|---|---|
| `--bg` | `#0a0a0c` | page background |
| `--surface` | `#111114` | cards, panels |
| `--surface-raised` | `#18181c` | popovers, modals, hovered surface |
| `--border` | `#232328` | hairlines, 1px only |
| `--border-hover` | `#33333a` | interactive edge on hover |
| `--text` | `#f2f2f4` | primary text — never pure `#fff` |
| `--text-muted` | `#8b8b93` | secondary text, labels |
| `--text-faint` | `#54545c` | disabled, placeholder |
| `--accent` | `#7c5cff` | one brand accent — links, focus rings, active states |
| `--accent-dim` | `#7c5cff` at 14% alpha | accent-tinted surfaces |
| `--up` | `#3ecf7e` | positive price/return delta only |
| `--down` | `#ff5c5c` | negative price/return delta only |

Rules:
- No gradients as filler. A gradient earns its place only inside a named
  kokonutui effect (`beams-background`, `shimmer-text`) doing actual motion
  work — never as static hero-section decoration.
- `--up`/`--down` are reserved. Never repurpose green/red for anything that
  isn't a signed financial delta — that ambiguity is how a chart gets
  misread at a glance, which is the one failure mode this palette cannot
  afford.
- Every color is a CSS variable in `:root`. No inline hex in components.

## Typography

Two families, both variable, both loaded once:

- **Display / headings** — a geometric sans with a tall x-height (Geist,
  or Inter as fallback). Used at weight 500–600 only. Never bold-700+ for
  body copy; weight is a signal, save it for one or two elements per screen.
- **Numeric / data** — a tabular-figure monospace (Geist Mono, or JetBrains
  Mono) for every price, percentage, ticker, and timestamp. Financial numbers
  in a proportional font drift and misalign in a table; this is non-negotiable
  wherever numbers appear in a column.

Scale is a 4-step type ramp, not a 9-step one: `text-sm` (13px, labels),
`text-base` (15px, body), `text-lg` (19px, section headers), `text-display`
(clamp 32–56px, hero only). Minimalism means resisting the urge to add a
fifth size for one component.

## Motion

This is the system's actual subject matter, so it gets rules, not vibes.

**Timing tokens** (CSS custom properties and a matching `motion` transition
object — keep them identical, never let JS and CSS timing drift apart):

| Token | Duration | Easing | Use |
|---|---|---|---|
| `--ease-out` | 180ms | `cubic-bezier(.16,1,.3,1)` | hover, focus, small state flips |
| `--ease-in-out` | 320ms | `cubic-bezier(.65,0,.35,1)` | layout shifts, tab/panel switches |
| `--spring-snappy` | — | `motion` spring, stiffness 400, damping 30 | drag, press, anything gesture-driven |
| `--spring-soft` | — | `motion` spring, stiffness 120, damping 20 | entrance of large surfaces (modals, page transitions) |

**Choreography rules:**
1. **Entrance is staggered, never simultaneous.** A list, grid, or nav that
   appears does so with 20–40ms stagger per item via `motion`'s
   `staggerChildren`. A wall of elements fading in at once reads as a slide
   deck, not a product.
2. **Exit is faster than enter.** Enter sells the interface; exit should get
   out of the way. Exit duration is roughly 60% of the matching enter duration.
3. **Nothing animates on scroll just because it can.** Scroll-linked motion
   (`useScroll` + `useTransform`) is reserved for signal, not wallpaper: a
   sticky header compressing, a chart line drawing in as it enters view, a
   number counting up once. If removing a scroll effect changes nothing about
   what the user understands, remove it.
4. **Hover states are always motion, never just color.** A button/card hover
   moves (scale 1.00→1.02, or a border-color transition with a subtle
   translateY(-1px)) in addition to any color shift, using `--ease-out`.
   A static color-only hover is treated as unfinished, not minimal.
5. **One idle/ambient animation per screen, maximum.** Flow fields, particle
   backgrounds, beams — pick at most one ambient kokonutui background effect
   per screen and mute its amplitude until it's barely perceptible in
   peripheral vision. Two ambient effects on one screen is visual noise, not
   "full animational."
6. **`prefers-reduced-motion: reduce` is honored everywhere**, not just on
   the ambient backgrounds. Every `motion` transition drops to a 1ms/no-op
   duration behind this media query — respected globally via a single
   `MotionConfig reducedMotion="user"` wrapper at the app root, not
   per-component opt-outs.

## Layout & minimalism discipline

- **8px base unit.** All spacing is a multiple of 8 (4 permitted only for
  icon-to-label gaps). No arbitrary padding values.
- **1px borders, no drop shadows for elevation.** Elevation is communicated
  by `--surface` → `--surface-raised` background steps plus a 1px border,
  not `box-shadow` blur. Reserve shadow for genuinely floating elements
  (dropdowns, toasts) at a single shared shadow token, not one per component.
- **Radius: 8px for controls, 12px for cards, 999px for pills/avatars.**
  Three radii total, system-wide.
- **Whitespace is the primary layout tool.** If a screen feels empty, the
  fix is better typographic hierarchy and motion timing, not more chrome,
  dividers, or background texture.
- **One accent color on screen at a time.** Multiple simultaneous accent-
  colored elements competing for attention violates minimalism even if each
  one is individually restrained.

## Component grounding (what to pull from where)

| Need | Source | Component/pattern |
|---|---|---|
| Hero heading treatment | kokonutui | `shimmer-text` or `dynamic-text`, restrained to headline only |
| Ambient hero background | kokonutui | `beams-background` or `flow-field`, amplitude muted per rule 5 |
| Primary CTA | kokonutui | `gradient-button`, recolored to `--accent` |
| Feature grid | kokonutui | `bento-grid` |
| Nav | kokonutui | `morphic-navbar`, recolored |
| Stat/metric card | bklit-ui | `stat-card-line-01` / `stat-card-area-01` |
| Price chart | bklit-ui | `candlestick-chart`, `live-line-chart` |
| Score/hit-rate gauge | bklit-ui | `gauge-chart` or `ring-chart` |
| Page/section transitions | motion | `AnimatePresence` + `--spring-soft` |
| Any hover/press state | motion | `whileHover` / `whileTap` + `--ease-out` / `--spring-snappy` |

## Anti-patterns — explicitly rejected

- Light mode, theme toggles, or `prefers-color-scheme` branching.
- Pure `#000`/`#fff` anywhere.
- More than one ambient background animation per screen.
- Animating for its own sake on elements the user's eye never rests on
  (e.g., a spinner-style loop on a static icon with no state change).
- Drop-shadow-based elevation.
- Green/red used for anything other than signed financial deltas.
- A fifth or sixth type size "just for this one spot."
- Importing kokonutui/bklit-ui components unmodified with their stock theme —
  every borrowed component gets re-tokenized to this palette before it ships.

## Reference paths

- `design-system/references/motion` — animation engine source, cloned shallow.
- `design-system/references/kokonutui` — effect/interaction component source.
- `design-system/references/bklit-ui` — chart component source.
- `design-system/shell` — the landing shell implementing this manifesto.
