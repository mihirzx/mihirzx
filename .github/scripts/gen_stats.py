#!/usr/bin/env python3
"""Render a self-hosted GitHub stats card in the profile's cyberpunk style.

Why this exists: github-readme-stats.vercel.app is frequently rate-limited (it
returned 503 on every attempt while this profile was built), which left a hole
in the page. This queries the GitHub GraphQL API directly and draws the card,
so the profile depends on nothing but GitHub itself.

Usage:  GITHUB_TOKEN=... python3 gen_stats.py <output.svg> [login]
Stdlib only — no pip install step needed in CI.
"""
import collections
import json
import os
import sys
import urllib.request

LOGIN = sys.argv[2] if len(sys.argv) > 2 else "mihirzx"
OUT = sys.argv[1] if len(sys.argv) > 1 else "stats.svg"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

BG, PANEL = "#0A0E14", "#0D1117"
CYAN, MAGENTA, PURPLE = "#00F0FF", "#FF2E97", "#A78BFA"
TEXT, DIM = "#C9D1D9", "#6E7681"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
# neon ramp, so the language bar reads as part of the same system
RAMP = ["#00F0FF", "#FF2E97", "#A78BFA", "#38BDF8", "#F472B6", "#818CF8", "#22D3EE", "#4B5563"]

QUERY = """
{ user(login:"%s") {
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions }
    }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false) {
      totalCount
      nodes { languages(first:10, orderBy:{field:SIZE, direction:DESC}) {
        edges { size node { name } } } }
    }
} }""" % LOGIN


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={"Authorization": f"bearer {TOKEN}",
                 "Content-Type": "application/json",
                 "User-Agent": "mihirzx-profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def build(u):
    c = u["contributionsCollection"]
    contribs = c["contributionCalendar"]["totalContributions"] + c["restrictedContributionsCount"]
    commits = c["totalCommitContributions"]
    repos = u["repositories"]["totalCount"]

    agg = collections.Counter()
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            agg[e["node"]["name"]] += e["size"]
    total = sum(agg.values()) or 1
    langs = agg.most_common(6)
    other = total - sum(s for _, s in langs)
    if other > 0:
        langs.append(("Other", other))

    W, H = 1000, 218
    tiles = [("CONTRIBUTIONS", contribs, CYAN),
             ("COMMITS THIS YEAR", commits, MAGENTA),
             ("PUBLIC REPOS", repos, PURPLE)]

    body = ""
    tw, tx, ty = 300, 34, 56
    for i, (label, val, accent) in enumerate(tiles):
        x = tx + i * (tw + 16)
        body += f"""
  <rect x="{x}" y="{ty}" width="{tw}" height="70" rx="3" fill="{accent}" opacity="0.07"/>
  <rect x="{x}" y="{ty}" width="{tw}" height="70" rx="3" fill="none" stroke="{accent}" stroke-width="1" stroke-opacity="0.4"/>
  <rect x="{x}" y="{ty}" width="3" height="70" fill="{accent}" opacity="0.9"/>
  <text x="{x+20}" y="{ty+31}" font-family="{MONO}" font-size="10.5" fill="{accent}" letter-spacing="2">{label}</text>
  <text x="{x+20}" y="{ty+60}" font-family="{MONO}" font-size="27" font-weight="700" fill="{TEXT}">{val:,}</text>"""

    # language distribution bar
    bar_y, bar_x, bar_w = 158, 34, W - 68
    cursor = 0.0
    legend = ""
    lx = bar_x
    for i, (name, size) in enumerate(langs):
        frac = size / total
        seg = frac * bar_w
        # "Other" always takes the neutral, so it never reads as a real language
        col = RAMP[-1] if name == "Other" else RAMP[i % (len(RAMP) - 1)]
        r_l = "3" if i == 0 else "0"
        body += f"""
  <rect x="{bar_x+cursor:.1f}" y="{bar_y}" width="{max(seg-1.5,1):.1f}" height="11" fill="{col}" opacity="0.85"/>"""
        cursor += seg
        label = f"{name} {frac*100:.1f}%"
        legend += f"""
  <circle cx="{lx+5}" cy="{bar_y+34}" r="4" fill="{col}"/>
  <text x="{lx+16}" y="{bar_y+38}" font-family="{MONO}" font-size="11.5" fill="{DIM}">{label}</text>"""
        lx += len(label) * 7.1 + 34

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{contribs} contributions, {commits} commits this year, {repos} public repos">
  <defs>
    <pattern id="gs" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{CYAN}" stroke-width="0.5" opacity="0.07"/>
    </pattern>
    <pattern id="ss" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="{CYAN}" opacity="0.045"/>
    </pattern>
    <filter id="fs" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="1.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#gs)"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="3" fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.3"/>
  <g stroke="{CYAN}" stroke-width="1.2" fill="none" opacity="0.45">
    <path d="M14 26V14H26"/><path d="M{W-26} 14H{W-14}V26"/>
    <path d="M{W-14} {H-26}V{H-14}H{W-26}"/><path d="M26 {H-14}H14V{H-26}"/>
  </g>
  <text x="34" y="36" font-family="{MONO}" font-size="13" fill="{CYAN}" letter-spacing="3.4" filter="url(#fs)">// SIGNAL</text>
  <text x="{W-34}" y="36" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end" letter-spacing="1.6">AUTO-REFRESHED DAILY</text>
{body}
  <text x="34" y="152" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="2">LANGUAGE DISTRIBUTION</text>
{legend}
  <rect width="{W}" height="{H}" fill="url(#ss)"/>
</svg>"""


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("GITHUB_TOKEN (or GH_TOKEN) must be set")
    svg = build(fetch())
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg):,} bytes)")
