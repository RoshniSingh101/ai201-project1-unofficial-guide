"""Scrape raw text from the document sources listed in planning.md.

This is the document-ingestion step (Milestone 3). It pulls the raw text from
each source URL and writes one .txt file per source into documents/raw/.

The sources fall into a few categories that need different handling:
  * Reddit threads      -> use Reddit's public JSON API (HTML is JS-rendered)
  * Google Sheets       -> the /pubhtml export is static HTML tables
  * gatech.edu specs    -> static server-rendered HTML
  * omscentral / omshub -> JavaScript single-page apps; a plain HTTP fetch only
                           returns the shell. We still save what we can and warn
                           so they can be collected another way if needed.

Usage:
    python scripts/scrape.py
    python scripts/scrape.py --out documents/raw --delay 2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Pretend to be a normal browser; several sites reject the default UA.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# (slug, human name, url). slug becomes the output filename.
SOURCES = [
    ("01_omscentral", "OMS Reviews (omscentral)", "https://www.omscentral.com"),
    ("02_omscs_rocks", "omscs.rocks capacity sheet",
     "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyHrRhH2V52bsYFEtm-8oJDaFOlyGYz6AKXm8WwsthN3fNP3KGkEx7O7D9ZHV3j2iKnzU2XHqoh4pQ/pubhtml"),
    ("03_reddit_course_specs_megathread", "Course & Specs Megathread",
     "https://www.reddit.com/r/OMSCS/comments/1pyef5z/course_specs_megathread_selection_choices/"),
    ("04_reddit_difficulty_spring_fall_2025", "Courses Ranked by Difficulty Spring/Fall 2025",
     "https://www.reddit.com/r/OMSCS/comments/1hsbc76/all_courses_ranked_by_difficulty_2025_springfall/"),
    ("05_reddit_difficulty_summer_2025", "Courses Ranked by Difficulty Summer 2025",
     "https://www.reddit.com/r/OMSCS/comments/1k5k7av/all_courses_ranked_by_difficulty_2025_summer/"),
    ("06_reddit_workload_distributions", "Workload Distributions",
     "https://www.reddit.com/r/OMSCS/comments/1dd0snd/all_courses_workload_distributions_table/"),
    ("07_omshub", "OMSHub", "https://www.omshub.org"),
    ("08_spec_machine_learning", "Specialization in Machine Learning",
     "https://omscs.gatech.edu/specialization-machine-learning"),
    ("09_spec_artificial_intelligence", "Specialization in Artificial Intelligence",
     "https://omscs.gatech.edu/specialization-artificial-intelligence-formerly-interactive-intelligence"),
    ("10_spec_hci", "Specialization in Human-Computer Interaction",
     "https://omscs.gatech.edu/specialization-human-computer-interaction"),
    ("11_spec_cpr", "Specialization in Computational Perception and Robotics",
     "https://omscs.gatech.edu/specialization-computational-perception-and-robotics"),
    ("12_spec_computing_systems", "Specialization in Computing Systems",
     "https://omscs.gatech.edu/specialization-computing-systems"),
    ("13_spec_computer_graphics", "Specialization in Computer Graphics",
     "https://omscs.gatech.edu/specialization-computer-graphics"),
]


def clean_text(text: str) -> str:
    """Collapse runs of blank lines and trailing whitespace."""
    lines = [line.rstrip() for line in text.splitlines()]
    out: list[str] = []
    blank = 0
    for line in lines:
        if line.strip():
            blank = 0
            out.append(line)
        else:
            blank += 1
            if blank <= 1:
                out.append("")
    return "\n".join(out).strip()


def html_to_text(html: str) -> str:
    """Strip scripts/styles and return visible text from an HTML page."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return clean_text(soup.get_text("\n"))


def scrape_reddit(url: str, session: requests.Session) -> str:
    """Pull the post body plus all comments via Reddit's JSON API."""
    json_url = url.rstrip("/") + "/.json"
    # Reddit requires a unique, descriptive User-Agent and rate-limits hard.
    reddit_headers = {"User-Agent": "script:omscs-unofficial-guide:v1.0 (educational RAG project)"}
    params = {"limit": 500, "raw_json": 1}

    resp = None
    for attempt in range(3):
        resp = session.get(json_url, params=params, headers=reddit_headers, timeout=30)
        if resp.status_code == 429:  # rate limited — back off and retry
            time.sleep(5 * (attempt + 1))
            continue
        break
    resp.raise_for_status()
    data = resp.json()

    parts: list[str] = []

    # data[0] is the post (link) listing; data[1] is the comment tree.
    post = data[0]["data"]["children"][0]["data"]
    parts.append(f"TITLE: {post.get('title', '')}")
    if post.get("selftext"):
        parts.append(post["selftext"])

    def walk(children: list, depth: int = 0) -> None:
        for child in children:
            if child.get("kind") != "t1":
                continue
            cdata = child["data"]
            body = (cdata.get("body") or "").strip()
            if body:
                indent = "  " * depth
                author = cdata.get("author", "unknown")
                parts.append(f"{indent}[{author}]: {body}")
            replies = cdata.get("replies")
            if isinstance(replies, dict):
                walk(replies["data"]["children"], depth + 1)

    if len(data) > 1:
        walk(data[1]["data"]["children"])

    return clean_text("\n\n".join(parts))


def scrape_google_sheet(url: str, session: requests.Session) -> str:
    """A published Google Sheet (/pubhtml) exposes a clean CSV at /pub?output=csv."""
    csv_url = re.sub(r"/pubhtml.*$", "/pub", url) + "?output=csv"
    resp = session.get(csv_url, timeout=30)
    resp.raise_for_status()
    return clean_text(resp.text)


def scrape_generic(url: str, session: requests.Session) -> str:
    """Fetch a URL and extract visible text from the HTML."""
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    return html_to_text(resp.text)


def scrape_source(slug: str, name: str, url: str, session: requests.Session) -> str:
    host = urlparse(url).netloc
    if "reddit.com" in host:
        return scrape_reddit(url, session)
    if "docs.google.com" in host:
        return scrape_google_sheet(url, session)
    return scrape_generic(url, session)


class BrowserScraper:
    """Lazy headless-browser fallback for JS-rendered pages and IP-blocked APIs.

    Created on first use so a fully-static run never pays the browser startup
    cost. Reused across sources, then closed via .close().
    """

    def __init__(self) -> None:
        self._pw = None
        self._browser = None

    def _ensure(self) -> None:
        if self._browser is not None:
            return
        from playwright.sync_api import sync_playwright  # local import: optional dep

        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()

    def fetch(self, url: str) -> str:
        self._ensure()
        page = self._browser.new_page(user_agent=HEADERS["User-Agent"])
        try:
            page.goto(url, wait_until="networkidle", timeout=45000)
            # Reddit lazy-loads comments; give late content a moment to paint.
            page.wait_for_timeout(3000)
            return clean_text(page.inner_text("body"))
        finally:
            page.close()

    def close(self) -> None:
        if self._browser is not None:
            self._browser.close()
        if self._pw is not None:
            self._pw.stop()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", default="documents/raw",
        help="Directory to write raw .txt files (default: documents/raw)",
    )
    parser.add_argument(
        "--delay", type=float, default=2.0,
        help="Seconds to wait between requests to be polite (default: 2)",
    )
    parser.add_argument(
        "--no-browser", action="store_true",
        help="Disable the headless-browser fallback for JS-rendered/blocked pages",
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(HEADERS)

    # Below this, a static fetch almost certainly only returned the page shell
    # (JS-rendered SPA), so we retry through a real browser.
    THIN_TEXT_CHARS = 600

    browser = None if args.no_browser else BrowserScraper()

    summary: list[tuple[str, str, int]] = []
    for slug, name, url in SOURCES:
        print(f"-> {name}\n   {url}")
        status = "ok"
        text = ""
        try:
            text = scrape_source(slug, name, url, session)
        except Exception as exc:  # noqa: BLE001 - report and keep going
            print(f"   .. static fetch failed: {exc}")

        # Fall back to a headless browser when static scraping came up empty/thin
        # (Reddit IP blocks, omscentral/omshub single-page apps).
        if len(text) < THIN_TEXT_CHARS and browser is not None:
            print("   .. retrying with headless browser")
            try:
                text = browser.fetch(url)
            except Exception as exc:  # noqa: BLE001
                print(f"   !! browser fetch failed: {exc}", file=sys.stderr)

        if not text:
            status = "FAILED"
            print("   !! FAILED (no content)", file=sys.stderr)
            summary.append((name, status, 0))
            time.sleep(args.delay)
            continue

        if len(text) < THIN_TEXT_CHARS:
            status = "THIN (verify manually)"

        header = f"SOURCE: {name}\nURL: {url}\n{'=' * 60}\n\n"
        path = out_dir / f"{slug}.txt"
        path.write_text(header + text, encoding="utf-8")
        print(f"   saved {len(text):,} chars -> {path} [{status}]")
        summary.append((name, status, len(text)))
        time.sleep(args.delay)

    if browser is not None:
        browser.close()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, status, n in summary:
        print(f"  {n:>8,} chars  {status:<22}  {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
