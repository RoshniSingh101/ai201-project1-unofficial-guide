# Scraping (Milestone 3 — ingestion)

`scrape.py` pulls raw text from the sources in `planning.md` and writes one
`.txt` file per source to `documents/raw/`.

```bash
pip install -r requirements.txt
playwright install chromium      # one-time: downloads the headless browser
python scripts/scrape.py         # default: --out documents/raw --delay 2
```

Each output file starts with a `SOURCE:` / `URL:` header so attribution
survives into chunking and embedding.

## How each source is scraped

| Source type | Method |
|-------------|--------|
| gatech.edu specialization pages (8–13) | static HTML → BeautifulSoup text |
| omscs.rocks Google Sheet (2) | `/pub?output=csv` export |
| Reddit threads (3–6) | static `/.json` API, then headless-browser fallback |
| omscentral (1), omshub (7) | headless-browser fallback (JS single-page apps) |

The script tries the cheap static method first. If a page comes back empty
(Reddit IP blocks) or suspiciously short (< 600 chars, i.e. a JS shell), it
automatically retries that URL through a headless Chromium browser, which
renders the JavaScript and passes real-browser checks. All 13 sources are
collected in one run with no manual steps.

Pass `--no-browser` to skip the fallback (static sources only), or `--delay N`
to change the politeness pause between requests.

## Notes

- `omscentral` (1) saves the course catalog table from the landing page
  (ratings / difficulty / workload per course). Individual per-course review
  text lives on sub-pages and is not crawled.
- The run never aborts on a single failure — it reports per-source status in a
  summary table and saves everything it can.
