// Builds index.html by injecting the data files into src/page.html. No dependencies.
import fs from 'fs';
import path from 'path';
import {fileURLToPath} from 'url';
const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = f => fs.readFileSync(path.join(root, f), 'utf8');
const page = read('src/page.html')
  .replace('/*__CRIT__*/', read('src/data/critical.json').trim())
  .replace('/*__GRIDS__*/', read('src/data/grids.json').trim());
fs.writeFileSync(path.join(root, 'index.html'), page);
console.log('Wrote index.html (' + Math.round(page.length / 1024) + ' KB)');
