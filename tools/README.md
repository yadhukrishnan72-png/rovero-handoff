# Scene generator (optional)

These scripts produced the 246 scene illustrations in `../assets/destinations/`. You do not need them to build the pages.
Use them to change the artwork style, fix a scene, or add a destination.

Requirements: Python 3.10+ and `pip install openpyxl`.

| File | What it does |
|---|---|
| `scene-plan.xlsx` | one row per destination: code, name, scene type (dropdown), landmark, notes. Edit this to change what a scene shows |
| `scene_data.py` | motif keys per destination code (which landmarks are drawn) |
| `scene_kit.py` | the library of ~125 landmark and feature drawings |
| `scene_backdrops.py` | the 14 base scenes (tropical island, desert, alpine ...) in 3 moods: day, sunset, golden hour |
| `make_scenes.py`, `destination_art.py` | the hand-made scenes (France, India, Australia, Switzerland, Maldives, Iceland, Greece, Netherlands, Norway, Mongolia, USA, Global, Indonesia, Japan, Kenya, Africa) and shared drawing helpers |
| `build_all_scenes.py` | builds every scene plus preview sheets |

Rebuild everything into a scratch folder (this also writes `index.html` and `sheet-N.html` preview pages):

```
python tools/build_all_scenes.py --plan tools/scene-plan.xlsx --out out/scenes
```

Build just a few: add codes at the end, for example `... --out out/scenes jp nl eu`.

Notes:
- `destination_art.py` can also draw outline-map style art from Natural Earth data, but that style was not chosen; the map data is not included.
- `build_scene_plan.py` regenerates `scene-plan.xlsx`, but it needs the supplier plan file (not included) to check the codes. Edit the spreadsheet directly instead.
- Output is plain SVG, 1000x1250.
