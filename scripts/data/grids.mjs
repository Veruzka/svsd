// Rebuild src/data/grids.json. Needs: npm i topojson-client world-atlas; run: node scripts/data/grids.mjs node_modules/world-atlas
import {feature} from 'topojson-client';
import fs from 'fs';
const polysOf = f => {
  const t = JSON.parse(fs.readFileSync(process.argv[2] + '/' + f));
  const g = feature(t, t.objects.land);
  const geom = g.geometry || g.features[0].geometry;
  return (geom.type === 'Polygon' ? [geom.coordinates] : geom.coordinates).map(p => {
    let a = 1e9, b = -1e9, c = 1e9, d = -1e9;
    for (const [x, y] of p[0]) { a = Math.min(a, x); b = Math.max(b, x); c = Math.min(c, y); d = Math.max(d, y); }
    return {p, bb: [a, b, c, d]};
  });
};
const ring = (r, x, y) => {
  let ins = false;
  for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i], [xj, yj] = r[j];
    if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) ins = !ins;
  }
  return ins;
};
const inside = (P, x, y) => P.some(({p, bb}) => x >= bb[0] && x <= bb[1] && y >= bb[2] && y <= bb[3] && ring(p[0], x, y) && !p.slice(1).some(h => ring(h, x, y)));
const P110 = polysOf('land-110m.json'), P10 = polysOf('land-10m.json');
const r2 = v => Math.round(v * 100) / 100, r3 = v => Math.round(v * 1000) / 1000;
const world = []; let row = 0; const step = 1.7;
for (let la = -58; la <= 83; la += step, row++) {
  const ls = step / Math.max(.2, Math.cos(la * Math.PI / 180)); const off = row % 2 ? ls / 2 : 0;
  for (let lo = -180 + off; lo < 180; lo += ls) if (inside(P110, lo, la)) world.push(r2(lo), r2(la));
}
const flat = (la, lo, s) => {
  const P = P10.filter(({bb}) => bb[1] >= lo[0] && bb[0] <= lo[1] && bb[3] >= la[0] && bb[2] <= la[1]);
  const out = []; let row = 0; const sx = s * 1.3;
  for (let y = la[0]; y <= la[1]; y += s, row++)
    for (let x = lo[0] + (row % 2 ? sx / 2 : 0); x <= lo[1]; x += sx) if (inside(P, x, y)) out.push(r3(x), r3(y));
  return out;
};
const ireland = flat([49.9, 58.7], [-11.2, 1.8], 0.1);
const hawaii = flat([18.85, 22.3], [-160.35, -154.75], 0.03);
fs.writeFileSync(new URL('../../src/data/grids.json', import.meta.url), JSON.stringify({world, ireland, hawaii}));
console.log(world.length / 2, ireland.length / 2, hawaii.length / 2);
