# Plotter Art Converter

Turn album-cover images into multi-color line art drawn by a pen plotter — built around a **broken Ender 3 Pro 3D printer converted into a pen plotter**.

The tool takes a raster image (JPG/PNG) and produces plotter-ready vector output: it reduces the image to a small palette, fills each color region with hatching (parallel lines), and exports layered SVG plus G-code for a servo-actuated pen.

> ⚠️ **Status: work in progress.** Phase 1 (image → SVG) is under active development. See the roadmap below.

## How it works

```
Input image (JPG/PNG)
      │
      ▼
Color quantization     K-means reduces the image to 4–6 dominant colors
      │
      ▼
Per-color masks        A binary mask is extracted for each color
      │
      ▼
Hatch fill             Each region is filled with parallel-line hatching
      │
      ▼
SVG export             One layer per color (ready for pen-swap workflows)
      │
      ▼
G-code export          Scaled to a 220×220 mm work area, servo pen lift (M280)
```

## Tech stack

- **Python** — CLI-first, with a Streamlit UI planned
- **Pillow** — image loading and manipulation
- **scikit-learn** — K-means color quantization
- **NumPy** — array/mask operations
- **svgwrite** — layered SVG output

## The hardware

A retired Ender 3 Pro repurposed as a pen plotter:

- Heated bed disabled (held at 0 °C in the G-code start script)
- Spring-steel sheet removed; paper clipped directly to the bare PCB bed
- ~220 × 220 mm usable work area
- Servo-driven pen lift controlled via `M280`

## Roadmap

- [ ] **Phase 1 — Image → SVG** (color quantization + hatching) *(in progress)*
- [ ] **Phase 2 — G-code export**
- [ ] **Phase 3 — Streamlit UI** with per-layer preview
- [ ] **Phase 4 — Pen-swap / layer ordering** (pen swap = `M0` pause in G-code)
- [ ] **Phase 5 — Pen library** (JSON) + color matching via Delta-E distance

## About this repository

This is a personal portfolio project, shared publicly to showcase the work. It is
not intended as a template or starter kit, and setup/usage instructions are
intentionally omitted.

**Sample image.** The repo ships with a generated, copyright-free
`images/test_pattern.png` so the pipeline can run without any third-party
artwork. Album covers are copyrighted and are kept local (git-ignored), never
committed.

**© Emil. All rights reserved.** This code is provided for viewing only. It may
not be copied, reused, or redistributed without permission.
