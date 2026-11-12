# daysuntil.bond

Live countdowns to the events the world is waiting for — 280 pages: holidays,
eclipses, moon phases, planetary stations, meteor showers, seasons, gaming,
movies and sport.

- **Site source:** `docs/` (served by GitHub Pages from `/docs` on `main`)
- **Generator:** install `python3 -m pip install -r requirements.txt`, then run
  `python3 tools/generate_site.py` (the generator reads `data/` and writes `docs/`)
- **Domain:** daysuntil.bond (CNAME in `docs/CNAME`)

To update an event: edit the data, regenerate, and push the new `docs/`.
