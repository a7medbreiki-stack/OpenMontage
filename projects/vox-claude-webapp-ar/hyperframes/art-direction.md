# Art Direction — الحلقة التي لا تراها

Atelier composition. Hand-authored HyperFrames. Nothing here is reusable; the next
piece must look nothing like this one.

## Design read

Arabic newsroom explainer for a sound-off vertical feed: stamped, evidential, unhurried
in the holds and sharp on the cuts. Journalism *about* a tool, never marketing *for* one.
Authority comes from showing the mechanism — never from adjectives.

Dials: `visual_variance` 3 · `motion_intensity` 6 · `information_density` 4.

## Palette

| Token | Value | Rule |
|---|---|---|
| `--ink` | `#0B0B0C` | The ground. Every scene sits on it. |
| `--paper` | `#F4F1EA` | Type and structure. Warm white, never pure #FFF. |
| `--accent` | `#FFD400` | **Only ever on the thing being asserted.** Never decorative. |
| `--dim` | `#4A4A4E` | Removed, superseded, de-emphasised. |
| `--faint` | `#1A1A1D` | Texture read as mass, not as content (the sc4 file tree). |

Red `#E03131` and green `#2FBF5B` appear in exactly one scene (sc6) because a test bar is
the one object whose meaning IS its colour. They appear nowhere else.

Zero gradients. Zero glow. Zero rounded corners. Zero soft shadows.

## Type

- **Arabic** — Cairo, variable axis 200–1000. Display weight 900, body 400. The weight
  jump is the hierarchy; size does the rest.
- **Latin** — JetBrains Mono. Only for code, mechanism names (`grep`, `Esc`) and the
  watermark. Always `dir="ltr"`.
- Reading type never below 32px. Texture may go smaller only with `data-layout-ignore`.
- **No `letter-spacing` on Arabic, at any weight, ever.**

## Motion character

Stepped, not smooth. Every arrival lands on a single step; longer moves use
`ease:"steps(n)"` so motion reads as a series of positions rather than a glide. No motion
blur anywhere. The look is *stamped* — movable type hitting paper — not animated.

Holds are an absence of motion, not slow motion. The deliberate ones carry `data-hold`.

## Signature device

**The ring** — the three-phase cycle (يقرأ · ينفّذ · يتحقّق).

It appears in exactly **two** beats: sc3 (introduction, rotates once in silence) and sc7
(hero, split and filled). It is absent from sc4, sc5, sc6, sc8 and sc9 — those carry their
own subjects, and the current phase is marked by a small mono eyebrow instead.

In sc10 it returns reduced to a letterform-scale mark: punctuation, not a third appearance.

This scarcity is the point. An earlier draft spined the ring through sc3–sc8 as a phase
indicator; that is branded slides, not a film, and it was re-planned out.

## Layout

Two scene families, alternating so no two adjacent beats share one:

1. **Full-frame typographic assertion** — sc1, sc10.
2. **Annotated object** — everything else: one subject, held in the safe area, label above.

Safe area is Instagram Reels: clear band y 14%–65%, x 6%–94% of 1080×1920 — so roughly
x 65–1015, y 269–1248. The bottom third stays empty by design; Instagram's own UI lives
there. sc4 is the only scene whose texture bleeds past it.

**This is laid out for Reels, not for TikTok or YouTube Shorts** — their clear bands are
narrower on the right and top, and `hyperframes check` flags this layout against them.
Re-targeting either platform means a re-layout, not a re-export.

## Arabic text rules (load-bearing — the look breaks without them)

- Reveals split on **spaces only**. Never per glyph — Arabic letters join and change shape
  by position, so glyph-splitting severs them before the animation begins.
- Arabic containers `dir="rtl"`; Latin tokens `dir="ltr"` in the mono face.
- Labels in sc3 and sc7 sit **outside** the rotating group so no Arabic glyph ever rotates.
- During the sc3 spin the labels dim to 0.18 — a static label pointing at a moving node is
  a lie — and restore when the ring lands.

## Anti-patterns for this piece

- Generic AI-purple or corporate-blue gradients
- Smooth eased motion with blur
- Terminal / code-rain cliché as shorthand for "AI coding"
- On-screen labels that merely restate the narration line
- The ring used as scaffolding in a scene that could carry its own subject

## Distinctness check

Could this be any other product's video? No — the ring is the specific claim of this
script, and every other subject (file tree, diff, test bar, tally, controls) is drawn from
one beat of it. Does it reuse a look I've made before? No stock scene-type, no registry
block consumed as a scene, no fixture.
