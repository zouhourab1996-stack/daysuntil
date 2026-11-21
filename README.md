# daysuntil.bond

Live countdown tools and researched event guides: holidays,
eclipses, moon phases, planetary stations, meteor showers, seasons, gaming,
movies and sport.

- **Site source:** `docs/` (served by GitHub Pages from `/docs` on `main`)
- **Generator:** install `python3 -m pip install -r requirements.txt`, then run
  `python3 tools/generate_site.py` (the generator reads `data/` and writes `docs/`)
- **Domain:** daysuntil.bond (CNAME in `docs/CNAME`)
- **Publishing:** pushes to `data/` or `tools/` run the validated GitHub Actions build and publish generated `docs/` updates.

To update an event: edit the data, regenerate, and push the new `docs/`.
