# svsd
Silicon Valley School of Design Challenge - October 2026

## Mother Tongues

An atlas of languages at risk, for diaspora families and people working to keep their language alive. Built for the SVSD "Search for Top Young Design Talent" brief (theme: storytelling).

- **Globe:** 1,495 languages Glottolog rates moribund, nearly extinct or extinct. Extinct languages turn into hollow rings in the year they were last recorded.
- **Timeline:** measured counts (dots), events (diamonds) and gaps in the record (hatched spans).
- **Stories:** scroll-driven map stories for Irish and Hawaiian, with full-bleed photos, document close-ups and the unexplained gaps.
- **Contribute:** families add text, photos and voice to a year or a gap, and confirm or correct AI-suggested causes.

Live demo with shared stories and AI suggestions: https://claude.ai/artifact/8zmPTcLA78NZFVrBjR1ezX (ask Veruzka for access).

### Run it locally
```
node scripts/build.mjs   # writes index.html from src/
open index.html          # or double-click it
```
No install needed. Outside claude.ai, stories you add are saved in your own browser only, and the "Suggest more possible reasons" button is hidden.

### Where to edit
| What | Where |
|---|---|
| Layout, styles, all code | `src/page.html` (design tokens at the top of `<style>`) |
| Language facts, speaker counts, events, AI hypotheses, "what fades" words | `LANGS` in `src/page.html` |
| Story steps (map camera, photos, chapters, documents, gaps) | `STORIES` in `src/page.html` |
| Map data | `src/data/*.json` (regenerate with `scripts/data/`) |
| Images to find | `shot-list.md` |

Always edit `src/`, then run `node scripts/build.mjs` and commit both `src/` and `index.html`. Don't edit `index.html` by hand; the next build overwrites it.

### GitHub Pages
Settings → Pages → Deploy from a branch → `main`, folder `/ (root)`.

### Data sources and caveats
- Status, families, speaker counts: [`languages-of-the-world`](https://pypi.org/project/languages-of-the-world/) (Glottolog endangerment).
- Coordinates and last-recorded years: [Glottolog CLDF](https://github.com/glottolog/glottolog-cldf).
- Irish counts: Census of Ireland 1851–1911, Irish Free State and CSO censuses 1926–2022.
- Hawaiian counts: Kingdom census 1853 and 1896 (speakers estimated from population), 1983 figure reported by ʻAha Pūnana Leo, US Census 1990, ACS 2009–13. **Verify the Hawaiian figures and the AI-hypothesis sources against primary sources before submitting.**
- The dots in the Ireland and Hawaiʻi maps are a model of speaker share, not survey locations.
