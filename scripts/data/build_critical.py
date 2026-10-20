"""Rebuild src/data/critical.json: moribund, nearly extinct and extinct languages with coordinates.

Inputs:
  pip install languages-of-the-world   (endangerment status, speaker counts, families)
  Glottolog CLDF languages.csv         (coordinates, last year of documentation)
    from https://github.com/glottolog/glottolog-cldf/blob/master/cldf/languages.csv

Usage: python scripts/data/build_critical.py path/to/languages.csv
Each row: [name, lat, lon, status (2 moribund, 3 nearly extinct, 4 extinct), speakers, last_year, family]
"""
import csv, json, os, sys
import low

DB = os.path.join(os.path.dirname(low.__file__), 'data', 'low_db.json')
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'data', 'critical.json')
LEVEL = {'moribund': 2, 'nearly_extinct': 3, 'extinct': 4}

d = json.load(open(DB))
geo = {r['Glottocode']: r for r in csv.DictReader(open(sys.argv[1]))}
fam = {f['glottocode']: f['label'] for f in d['families']}
out = []
for l in d['languages']:
    if l['endangerment'] not in LEVEL:
        continue
    g = geo.get(l['glottocode'] or '')
    if not g or not g['Latitude']:
        continue
    y = g['Last_Year_Of_Documentation']
    out.append([l['label'], round(float(g['Latitude']), 2), round(float(g['Longitude']), 2), LEVEL[l['endangerment']],
                l['speaker_count'] or 0, int(y) if y else None, fam.get(l['family_glottocode'], '')])
json.dump(out, open(OUT, 'w'), separators=(',', ':'), ensure_ascii=False)
print(len(out), 'languages written')
