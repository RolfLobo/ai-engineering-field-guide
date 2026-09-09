#!/usr/bin/env python3
"""Generate the job-description market wiki from job-market/data_structured/.

Deterministic and rerunnable: every run re-reads all scrape months present in
data_structured/ and rewrites pages/ and charts/ in full. This script is the
update path - when a new monthly scrape lands, run:

    job-market/.venv/bin/python market-wiki/generate.py

Stdlib + PyYAML only. Charts are hand-rolled SVG (no matplotlib) so output is
stable and dependency-free.
"""

import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "job-market" / "data_structured"
OUT = Path(__file__).resolve().parent
PAGES = OUT / "pages"
CHARTS = OUT / "charts"

MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

SKILL_CATS = ["genai", "languages", "cloud", "ml", "databases", "ops", "data",
              "web", "domains", "other"]

USE_CASE_THEMES = [
    ("workflow automation", r"automat|workflow|manual (task|process|work)|streamlin|productivity"),
    ("agents and copilots", r"\bagentic?\b|copilot|tool[- ](use|calling)|multi[- ]agent|orchestrat"),
    ("RAG and knowledge access", r"\brag\b|retrieval|knowledge (base|management)|document (qa|q&a|understanding|analysis)|enterprise search"),
    ("conversational AI", r"chatbot|conversational|virtual assistant|\bchat\b|voice assistant"),
    ("content and marketing", r"content (creation|generation|production)|marketing|copy(-| )?writing|seo|social media"),
    ("code and developer tools", r"cod(e|ing) (review|generation|assistant)|developer productivity|engineering productivity|pull request|\bPR\b review"),
    ("search and recommendation", r"recommend(ation|er)|personaliz|ranking|search (results|relevance|engine)"),
    ("document processing", r"document processing|extract(ion)? (of )?(data|information|fields)|ocr|invoice|resume|contract (analysis|review)"),
    ("data and analytics", r"analytic|insight(s)? generation|business intelligence|forecast|report(ing)? generation"),
    ("customer support", r"customer (support|service)|help ?desk|ticket (routing|triage)"),
    ("security and fraud", r"fraud|cybersecurity|threat (detection|intelligence)|security operations|phishing"),
]

INDUSTRIES = [
    ("finance", r"\bbank\b|financial|fintech|insuranc|invest(ment|ing)?|payment|trading|lending|credit|asset management|mortgage|capital markets|wealth"),
    ("healthcare", r"health(care)?|medical|clinic|pharma|biotech|patient|therapeut|dental|life sciences"),
    ("legal", r"\blegal\b|law firm|attorney|litigation|e-?discovery"),
    ("cybersecurity", r"cybersecurity|cyber ?security|threat intelligence|security (operations|platform|company)"),
    ("e-commerce and retail", r"e-?commerce|retail|marketplace|shopping|grocery|fashion"),
    ("education", r"education|edtech|e-?learning|university|student|course"),
    ("media and advertising", r"\bmedia\b|entertainment|streaming|gaming|news|publish(ing|er)|advertis|\bads?\b|marketing (platform|tech|agency)"),
    ("telecom", r"telecom|telecommunication"),
    ("travel and hospitality", r"travel|hospitality|booking|hotel|airline|lodging"),
    ("logistics and mobility", r"logistic|supply chain|shipping|transport|delivery|mobility|automotive|vehicle|autonomous driving"),
    ("energy and utilities", r"\benergy\b|utilit(y|ies)|solar|renewable|oil and gas|power grid"),
    ("real estate", r"real estate|proptech|property"),
    ("hr and recruiting", r"recruiting|human resources|\bhr\b|talent (acquisition|management|platform)"),
    ("government and defense", r"government|public sector|defense|defence"),
    ("software and SaaS", r"software|saas|developer tools|\bapi\b|cloud|devtools|\btech\b|technology|platform|ai company|data (platform|infrastructure)"),
]

PALETTE = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
           "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac",
           "#86bcb6", "#d37295", "#fabfd2", "#b6992d"]


def pct(count, total):
    return f"{count / total * 100:.1f}%"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def load_corpus():
    """Return (records, months). Each record is a flat dict."""
    records = []
    months = sorted(d.name for d in DATA.iterdir() if d.is_dir())
    for month in months:
        for path in sorted((DATA / month).glob("*.yaml")):
            try:
                doc = yaml.safe_load(path.read_text())
            except Exception as e:
                print(f"skip unreadable {path}: {e}", file=sys.stderr)
                continue
            if not isinstance(doc, dict):
                continue
            pos = doc.get("position") or {}
            comp = doc.get("company") or {}
            meta = doc.get("meta") or {}
            rec = {
                "month": month,
                "title": (pos.get("title") or "").strip(),
                "ai_type": ((pos.get("ai_type") or {}).get("type") or "unknown").strip(),
                "use_cases": pos.get("use_cases") or [],
                "skills": pos.get("skills") or {},
                "company": (comp.get("name") or "").strip(),
                "focus": (comp.get("focus") or "").strip(),
                "location": (meta.get("location") or "").strip(),
            }
            records.append(rec)
    return records, months


COUNTRY_NAMES = {"IND": "India", "USA": "USA", "GBR": "UK", "DEU": "Germany",
                 "NLD": "Netherlands", "CAN": "Canada", "PRT": "Portugal",
                 "ITA": "Italy", "CZE": "Czechia", "CHE": "Switzerland",
                 "IRL": "Ireland", "SGP": "Singapore", "ESP": "Spain",
                 "FRA": "France", "GRC": "Greece", "BGR": "Bulgaria",
                 "ARE": "UAE", "TJK": "Tajikistan", "MEX": "Mexico",
                 "ARG": "Argentina", "ARM": "Armenia", "AUS": "Australia",
                 "AUT": "Austria", "BEL": "Belgium", "BRA": "Brazil",
                 "CHL": "Chile", "CYP": "Cyprus", "DNK": "Denmark",
                 "EGY": "Egypt", "EUR": "Europe (remote)", "HKG": "Hong Kong",
                 "HRV": "Croatia", "HUN": "Hungary", "IDN": "Indonesia",
                 "ISR": "Israel", "JEY": "Jersey", "JOR": "Jordan",
                 "LTU": "Lithuania", "LUX": "Luxembourg", "MAR": "Morocco",
                 "MOZ": "Mozambique", "MYS": "Malaysia", "NGA": "Nigeria",
                 "NOR": "Norway", "OMN": "Oman", "PAK": "Pakistan",
                 "PER": "Peru", "POL": "Poland", "QAT": "Qatar",
                 "ROU": "Romania", "SVK": "Slovakia", "SWE": "Sweden",
                 "UKR": "Ukraine", "VNM": "Vietnam"}


def month_label(m):
    y, mo, d = m.split("-")
    return f"{MONTH_NAMES[int(mo)]} {int(d)}, {y}"


def month_short(m):
    _, mo, d = m.split("-")
    return f"{MONTH_NAMES[int(mo)]} {int(d)}"


# ---------------------------------------------------------------- aggregation

def aggregate(records, months):
    agg = {}
    n = len(records)
    agg["n_jobs"] = n
    agg["months"] = months
    agg["window"] = f"{month_label(months[0])} to {month_label(months[-1])}" if months else "n/a"

    per_month = {m: [r for r in records if r["month"] == m] for m in months}
    agg["per_month_n"] = {m: len(v) for m, v in per_month.items()}

    ai = Counter(r["ai_type"] for r in records)
    agg["ai_types"] = ai
    agg["ai_by_month"] = {
        m: Counter(r["ai_type"] for r in per_month[m]) for m in months
    }

    skills = defaultdict(Counter)
    for r in records:
        for cat in SKILL_CATS:
            for s in r["skills"].get(cat) or []:
                s = str(s).strip()
                if s:
                    skills[cat][s] += 1
    agg["skills"] = skills

    skill_month = defaultdict(lambda: defaultdict(Counter))
    for m in months:
        for r in per_month[m]:
            for cat in SKILL_CATS:
                for s in r["skills"].get(cat) or []:
                    s = str(s).strip()
                    if s:
                        skill_month[cat][s][m] += 1
    agg["skill_month"] = skill_month

    themes = Counter()
    theme_month = {t: Counter() for t, _ in USE_CASE_THEMES}
    theme_examples = defaultdict(list)
    n_with_uc = 0
    for r in records:
        text = " | ".join(r["use_cases"]).lower()
        if r["use_cases"]:
            n_with_uc += 1
        for theme, pat in USE_CASE_THEMES:
            if re.search(pat, text):
                themes[theme] += 1
                theme_month[theme][r["month"]] += 1
                if len(theme_examples[theme]) < 3:
                    theme_examples[theme].append(r["use_cases"][0][:110])
    agg["themes"] = themes
    agg["theme_month"] = theme_month
    agg["theme_examples"] = theme_examples
    agg["n_with_uc"] = n_with_uc

    industries = Counter()
    industry_month = {i: Counter() for i, _ in INDUSTRIES}
    unclassified = 0
    for r in records:
        hay = " ".join([r["focus"], r["company"], r["title"]]).lower()
        hit = None
        for name, pat in INDUSTRIES:
            if re.search(pat, hay):
                hit = name
                break
        if hit:
            industries[hit] += 1
            industry_month[hit][r["month"]] += 1
        else:
            unclassified += 1
    agg["industries"] = industries
    agg["industry_month"] = industry_month
    agg["n_unclassified"] = unclassified

    agg["companies"] = Counter(r["company"] for r in records if r["company"])
    countries = Counter()
    cities = Counter()
    for r in records:
        loc = r["location"]
        if not loc:
            continue
        parts = [p.strip() for p in loc.split(",")]
        if len(parts) >= 2:
            cities[parts[0]] += 1
            countries[parts[-1]] += 1
        else:
            # single-part locations in this dataset are bare country codes (USA, IND, ...)
            countries[loc] += 1
    agg["countries"] = countries
    agg["cities"] = cities

    levels = Counter()
    level_month = defaultdict(Counter)
    level_pats = [
        ("junior", r"\b(junior|jr\.?|entry[- ]level|graduate|intern)\b"),
        ("senior", r"\b(senior|sr\.?)\b"),
        ("staff", r"\bstaff\b"),
        ("principal", r"\bprincipal\b"),
        ("lead", r"\blead\b"),
        ("manager/director/head", r"\b(manager|director|head of|vp\b|chief)\b"),
        ("distinguished/fellow", r"\b(distinguished|fellow)\b"),
    ]
    for r in records:
        t = r["title"].lower()
        matched = False
        for lvl, pat in level_pats:
            if re.search(pat, t):
                levels[lvl] += 1
                level_month[lvl][r["month"]] += 1
                matched = True
                break
        if not matched:
            levels["no level in title"] += 1
            level_month["no level in title"][r["month"]] += 1
    agg["levels"] = levels
    agg["level_month"] = level_month

    return agg


# ------------------------------------------------------------- svg generators

def svg_open(w, h, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">',
            f'<text x="12" y="22" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="15" fill="#1a1a1a">{esc(title)}</text>']


def svg_close():
    return ["</svg>"]


def chart_hbar(name, title, items, unit="%"):
    """items: list of (label, float_value, value_label)."""
    bar_h, gap, top, left = 20, 8, 40, 250
    w = 760
    h = top + len(items) * (bar_h + gap) + 16
    maxv = max(v for _, v, _ in items) or 1.0
    out = svg_open(w, h, title)
    for i, (label, v, vlab) in enumerate(items):
        y = top + i * (bar_h + gap)
        bw = max(2, (w - left - 100) * v / maxv)
        out.append(f'<text x="{left - 8}" y="{y + 15}" text-anchor="end" '
                   f'font-family="Helvetica,Arial,sans-serif" font-size="12" '
                   f'fill="#333">{esc(label[:38])}</text>')
        out.append(f'<rect x="{left}" y="{y}" width="{bw:.1f}" height="{bar_h}" '
                   f'fill="{PALETTE[i % len(PALETTE)]}" rx="2"/>')
        out.append(f'<text x="{left + bw + 6:.1f}" y="{y + 15}" '
                   f'font-family="Helvetica,Arial,sans-serif" font-size="12" '
                   f'fill="#333">{esc(vlab)}</text>')
    out += svg_close()
    (CHARTS / f"{name}.svg").write_text("\n".join(out))


def chart_lines(name, title, series, labels, ylabel="% of postings"):
    w, h, left, right, top, bottom = 820, 340, 60, 200, 40, 46
    plot_w, plot_h = w - left - right, h - top - bottom
    all_vals = [v for pts in series.values() for _, v in pts]
    ymax = max(all_vals) * 1.15 if all_vals else 1.0
    n = len(labels)
    out = svg_open(w, h, title)

    def xpos(i):
        return left + plot_w * i / max(1, n - 1)

    def ypos(v):
        return top + plot_h * (1 - v / ymax)

    for frac in (0, 0.25, 0.5, 0.75, 1.0):
        v = ymax * frac
        y = ypos(v)
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" '
                   f'stroke="#ddd" stroke-width="1"/>')
        out.append(f'<text x="{left - 6}" y="{y + 4:.1f}" text-anchor="end" '
                   f'font-family="Helvetica,Arial,sans-serif" font-size="10" '
                   f'fill="#666">{v:.0f}</text>')
    for i, lab in enumerate(labels):
        out.append(f'<text x="{xpos(i):.1f}" y="{h - 24}" text-anchor="middle" '
                   f'font-family="Helvetica,Arial,sans-serif" font-size="10" '
                   f'fill="#666">{esc(lab)}</text>')
    out.append(f'<text x="12" y="{h - 8}" font-family="Helvetica,Arial,sans-serif" '
               f'font-size="10" fill="#666">{esc(ylabel)} (share within each month)</text>')
    labels_out = []
    for k, (sname, pts) in enumerate(series.items()):
        color = PALETTE[k % len(PALETTE)]
        d = " ".join(f"{'M' if j == 0 else 'L'}{xpos(i):.1f},{ypos(v):.1f}"
                     for j, (i, v) in enumerate(pts))
        out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"/>')
        lx, ly = xpos(pts[-1][0]), ypos(pts[-1][1])
        out.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3" fill="{color}"/>')
        labels_out.append([ly, sname, color])
    # stagger end-of-line labels so they never overlap
    labels_out.sort(key=lambda x: x[0])
    prev = -100.0
    for entry in labels_out:
        entry[0] = max(entry[0], prev + 13)
        prev = entry[0]
    if labels_out and labels_out[-1][0] > h - bottom + 20:
        pass  # overflowing past the axis is acceptable; it stays inside the svg
    for ly, sname, color in labels_out:
        out.append(f'<text x="{xpos(n - 1) + 8:.1f}" y="{ly + 4:.1f}" '
                   f'font-family="Helvetica,Arial,sans-serif" font-size="11" '
                   f'fill="{color}">{esc(sname[:24])}</text>')
    out += svg_close()
    (CHARTS / f"{name}.svg").write_text("\n".join(out))


# ---------------------------------------------------------------- page writers

def ul(lines, items):
    lines.append("")
    lines.extend(f"- {it}" for it in items)
    lines.append("")


def write_index(agg, pages):
    n, months = agg["n_jobs"], agg["months"]
    ai = agg["ai_types"]
    L = ["# AI Engineering Job Market Wiki", "",
         f"Generated from the job-market dataset: {n:,} job descriptions scraped "
         f"from builtin.com in {len(months)} monthly scrapes, {agg['window']}. "
         f"Each month is an independent cross-section (no job overlaps between "
         f"scrapes). Source: [job-market/data_structured/](../../job-market/data_structured/), "
         f"methodology in [job-market/_internal/](../../job-market/_internal/PIPELINE.md). "
         "This directory is regenerated in full by [generate.py](../generate.py); "
         "see [README.md](../README.md) for the update workflow.", ""]
    countries = agg["countries"]
    top_countries = countries.most_common(6)
    other = sum(v for _, v in countries.most_common()[6:])
    geo = ", ".join(f"{COUNTRY_NAMES.get(c, c)}: {pct(v, n)}"
                    for c, v in top_countries)
    if other:
        geo += f", other ({len(countries) - 6} countries): {pct(other, n)}"
    L.append("## At a glance")
    ul(L, [
        f"AI-First: {ai.get('ai-first', 0):,} ({pct(ai.get('ai-first', 0), n)}) - "
        f"AI-Support: {ai.get('ai-support', 0):,} ({pct(ai.get('ai-support', 0), n)}) - "
        f"ML-First: {ai.get('ml-first', 0):,} ({pct(ai.get('ml-first', 0), n)}) - "
        f"Unclassified: {ai.get('unknown', 0):,} ({pct(ai.get('unknown', 0), n)})",
        f"Postings per scrape: {', '.join(f'{month_short(m)}: {agg['per_month_n'][m]:,}' for m in months)}",
        f"Geography: {geo}",
    ])
    L.append("## Pages")
    ul(L, [f"[{t}]({f}) - {d}" for f, t, d in pages])
    L.append("## Visual")
    ul(L, [
        "Charts as standalone SVG files in [charts/](../charts/)",
        "[charts/dashboard.html](../charts/dashboard.html) - all charts on one page",
    ])
    (PAGES / "index.md").write_text("\n".join(L))


def write_skills(agg, months):
    n = agg["n_jobs"]
    L = ["# Skills", "",
         f"Skill mentions across {n:,} postings, per the categories produced by the "
         "extraction pipeline. A skill is counted only when the description spells "
         "it out, so shares are a floor, not a ceiling (method: "
         "[extract_process.md](../../job-market/_internal/extract_process.md)). "
         "Scrape window: " + agg["window"] + ".", ""]
    for cat in SKILL_CATS:
        counter = agg["skills"].get(cat)
        if not counter:
            continue
        L.append(f"## {cat}")
        ul(L, [f"{s} - {c:,} ({pct(c, n)})" for s, c in counter.most_common(20)])
    top_genai = agg["skills"]["genai"].most_common(15)
    chart_hbar("skills-genai", "Top GenAI skills - share of all postings",
               [(s, c / n * 100, f"{pct(c, n)} ({c:,})") for s, c in top_genai])
    chart_hbar("skills-languages", "Languages - share of all postings",
               [(s, c / n * 100, f"{pct(c, n)} ({c:,})") for s, c in
                agg["skills"]["languages"].most_common(10)])
    trend_names = [s for s, _ in agg["skills"]["genai"].most_common(7)]
    for extra in ["PyTorch", "Fine-Tuning", "Evaluation"]:
        for cat in ("ml", "genai", "ops", "other"):
            match = next((s for s in agg["skills"][cat]
                          if s.lower() == extra.lower()), None)
            if match and match not in trend_names:
                trend_names.append(match)
                break
    series = {}
    for s in trend_names[:9]:
        per_cat = None
        for cat in SKILL_CATS:
            if s in agg["skill_month"][cat]:
                per_cat = agg["skill_month"][cat][s]
                break
        if per_cat is None:
            continue
        pts = []
        for i, m in enumerate(months):
            share = per_cat.get(m, 0) / agg["per_month_n"][m] * 100
            pts.append((i, share))
        series[s] = pts
    chart_lines("skills-trends", "Skill trends by scrape - share of that scrape's postings",
                series, [month_short(m) for m in months])
    L.append("## Charts")
    ul(L, [
        "[skills-genai.svg](../charts/skills-genai.svg) - top GenAI skills",
        "[skills-languages.svg](../charts/skills-languages.svg) - languages",
        "[skills-trends.svg](../charts/skills-trends.svg) - monthly trend lines for the top skills",
    ])
    (PAGES / "skills.md").write_text("\n".join(L))


def write_use_cases(agg, months):
    n = agg["n_jobs"]
    L = ["# Use Cases", "",
         f"Keyword-classified themes over the use-case text extracted from "
         f"{n:,} postings ({agg['n_with_uc']:,} have at least one use case). "
         "Classification is keyword matching over the extracted use-case sentences, "
         "so one posting can carry several themes and borderline phrasings are "
         "missed - treat this as an approximate view; the exact sentences live in "
         "the [dataset](../../job-market/data_structured/).", ""]
    L.append("## Themes")
    ul(L, [f"{t} - {c:,} ({pct(c, n)})" for t, c in agg["themes"].most_common()])
    top = agg["themes"].most_common(10)
    chart_hbar("use-cases", "Use-case themes - share of all postings",
               [(t, c / n * 100, f"{pct(c, n)} ({c:,})") for t, c in top])
    L.append("## Example extracted use cases per theme")
    for t, _ in agg["themes"].most_common():
        L.append(f"### {t}")
        ul(L, agg["theme_examples"].get(t, ["(none)"]))
    L.append("## Chart")
    ul(L, ["[use-cases.svg](../charts/use-cases.svg)"])
    (PAGES / "use-cases.md").write_text("\n".join(L))


def write_industries(agg, months):
    n = agg["n_jobs"]
    L = ["# Industries", "",
         f"Keyword-classified industry per posting, matched in order against the "
         f"company focus text, then company name, then job title. First match "
         f"wins; {agg['n_unclassified']:,} postings ({pct(agg['n_unclassified'], n)}) "
         "match no keyword and are left unclassified. This is an approximation "
         "(the dataset has no industry field) - share values are indicative, not "
         "exact. Scrape window: " + agg["window"] + ".", ""]
    L.append("## Industries by postings")
    ul(L, [f"{name} - {c:,} ({pct(c, n)})" for name, c in agg["industries"].most_common()])
    top = agg["industries"].most_common(12)
    chart_hbar("industries", "Industries - share of all postings (keyword-classified)",
               [(t, c / n * 100, f"{pct(c, n)} ({c:,})") for t, c in top])
    first, last = months[0], months[-1]
    movers = []
    for name, _ in agg["industries"].most_common(15):
        f_share = agg["industry_month"][name].get(first, 0) / agg["per_month_n"][first] * 100
        l_share = agg["industry_month"][name].get(last, 0) / agg["per_month_n"][last] * 100
        movers.append((name, l_share - f_share, f_share, l_share))
    movers.sort(key=lambda x: -abs(x[1]))
    L.append(f"## Movement, {month_label(first)} to {month_label(last)}")
    ul(L, [f"{name}: {f_share:.1f}% to {l_share:.1f}% ({delta:+.1f} points)"
           for name, delta, f_share, l_share in movers[:8]])
    L.append("## Chart")
    ul(L, ["[industries.svg](../charts/industries.svg)"])
    (PAGES / "industries.md").write_text("\n".join(L))


def write_companies_locations(agg):
    n = agg["n_jobs"]
    L = ["# Companies and Locations", "",
         f"Employers and geographies across {n:,} postings, {agg['window']}.", ""]
    L.append("## Top companies")
    ul(L, [f"{c} - {v:,} ({pct(v, n)})" for c, v in agg["companies"].most_common(25)])
    chart_hbar("companies", "Top companies by number of postings",
               [(c, v, f"{v:,}") for c, v in agg["companies"].most_common(15)])
    L.append("## By country")
    ul(L, [f"{c} - {v:,} ({pct(v, n)})" for c, v in agg["countries"].most_common()])
    L.append("## Top cities")
    ul(L, [f"{c} - {v:,} ({pct(v, n)})" for c, v in agg["cities"].most_common(15)])
    chart_hbar("locations", "Postings by location (city level, top 15)",
               [(c, v, f"{v:,}") for c, v in agg["cities"].most_common(15)])
    L.append("## Charts")
    ul(L, [
        "[companies.svg](../charts/companies.svg)",
        "[locations.svg](../charts/locations.svg)",
    ])
    (PAGES / "companies-locations.md").write_text("\n".join(L))


def write_trends(agg, months):
    n = agg["n_jobs"]
    L = ["# Trends", "",
         f"Month-over-month shares across the {len(months)} scrapes "
         f"({agg['window']}). Every month is an independent cross-section of "
         "builtin.com listings, so a share is the fraction of that month's "
         "postings - not headcount and not hiring volume.", ""]
    L.append("## AI type by scrape")
    ai_rows = []
    for m in months:
        c = agg["ai_by_month"][m]
        tot = agg["per_month_n"][m]
        ai_rows.append(f"{month_label(m)}: AI-First {pct(c.get('ai-first', 0), tot)}, "
                       f"AI-Support {pct(c.get('ai-support', 0), tot)}, "
                       f"ML-First {pct(c.get('ml-first', 0), tot)}, "
                       f"Unclassified {pct(c.get('unknown', 0), tot)} (n={tot:,})")
    ul(L, ai_rows)
    series = {}
    for k in ("ai-first", "ai-support", "ml-first"):
        series[k] = [(i, agg["ai_by_month"][m].get(k, 0) / agg["per_month_n"][m] * 100)
                     for i, m in enumerate(months)]
    chart_lines("trend-ai-types", "AI type share by scrape", series,
                [month_short(m) for m in months])

    L.append("## Seniority in titles")
    lvl_rows = []
    tracked = ["junior", "senior", "staff", "principal", "manager/director/head"]
    for m in months:
        tot = agg["per_month_n"][m]
        parts = ", ".join(f"{lvl} {pct(agg['level_month'][lvl].get(m, 0), tot)}"
                          for lvl in tracked)
        lvl_rows.append(f"{month_label(m)}: {parts}")
    ul(L, lvl_rows)
    series = {lvl: [(i, agg["level_month"][lvl].get(m, 0) / agg["per_month_n"][m] * 100)
                    for i, m in enumerate(months)] for lvl in tracked}
    chart_lines("trend-levels", "Seniority share by scrape (title keywords)", series,
                [month_short(m) for m in months])

    first, last = months[0], months[-1]
    movers = []
    seen = set()
    for cat in SKILL_CATS:
        for s, total in agg["skills"][cat].most_common(200):
            if s.lower() in seen:
                continue
            seen.add(s.lower())
            per_cat = agg["skill_month"][cat][s]
            f_share = per_cat.get(first, 0) / agg["per_month_n"][first] * 100
            l_share = per_cat.get(last, 0) / agg["per_month_n"][last] * 100
            movers.append((s, l_share - f_share, f_share, l_share, total))
    risers = sorted(movers, key=lambda x: -x[1])[:8]
    fallers = sorted(movers, key=lambda x: x[1])[:8]
    L.append(f"## Skill movers, {month_label(first)} to {month_label(last)}")
    L.append("")
    L.append("Risers (share of that month's postings):")
    ul(L, [f"{s} - {f:.1f}% to {l:.1f}% ({d:+.1f} points, {t:,} total)"
           for s, d, f, l, t in risers])
    L.append("Fallers:")
    ul(L, [f"{s} - {f:.1f}% to {l:.1f}% ({d:+.1f} points, {t:,} total)"
           for s, d, f, l, t in fallers])
    L.append("## Charts")
    ul(L, [
        "[trend-ai-types.svg](../charts/trend-ai-types.svg)",
        "[trend-levels.svg](../charts/trend-levels.svg)",
        "[skills-trends.svg](../charts/skills-trends.svg)",
    ])
    (PAGES / "trends.md").write_text("\n".join(L))


def write_dashboard(page_titles):
    parts = ["<!DOCTYPE html><html><head><meta charset='utf-8'>",
             "<title>AI Engineering Job Market - Charts</title><style>",
             "body{font-family:Helvetica,Arial,sans-serif;max-width:900px;margin:"
             "24px auto;padding:0 16px;color:#1a1a1a}",
             "h1{font-size:22px}h2{font-size:16px;margin-top:28px}",
             "nav a{margin-right:14px;font-size:14px}",
             "svg{max-width:100%;height:auto;border:1px solid #eee;margin:8px 0}",
             "</style></head><body>",
             "<h1>AI Engineering Job Market - Charts</h1>",
             "<nav>" + " ".join(f"<a href='../pages/{f}'>{t}</a>"
                                for f, t, _ in page_titles) + "</nav>",
             "<p>Generated from job-market/data_structured/ by market-wiki/generate.py."
             " Shares are within-month fractions of postings.</p>"]
    for svg in sorted(CHARTS.glob("*.svg")):
        name = svg.stem.replace("-", " ")
        parts.append(f"<h2>{esc(name)}</h2>")
        parts.append(svg.read_text())
    parts.append("</body></html>")
    (CHARTS / "dashboard.html").write_text("\n".join(parts))


def append_log(agg):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (f"## [{stamp}] regenerate | {agg['n_jobs']:,} postings, "
             f"{len(agg['months'])} scrapes ({agg['window']})\n\n"
             "- pages/ and charts/ rewritten from job-market/data_structured/\n")
    log = OUT / "log.md"
    if log.exists() and stamp.split()[0] in log.read_text().split("## [")[-1]:
        return  # one entry per day; reruns same day update nothing
    with log.open("a") as f:
        f.write("\n" + entry)


def main():
    PAGES.mkdir(exist_ok=True)
    CHARTS.mkdir(exist_ok=True)
    records, months = load_corpus()
    if not records:
        print("no records found under", DATA, file=sys.stderr)
        sys.exit(1)
    agg = aggregate(records, months)

    pages = [
        ("skills.md", "Skills", "top skills per category and monthly trends"),
        ("use-cases.md", "Use Cases", "keyword-classified themes with examples"),
        ("industries.md", "Industries", "keyword-classified industries and movement"),
        ("companies-locations.md", "Companies and Locations", "top employers and geographies"),
        ("trends.md", "Trends", "AI-type, seniority, and skill movers by month"),
    ]
    write_index(agg, pages)
    write_skills(agg, months)
    write_use_cases(agg, months)
    write_industries(agg, months)
    write_companies_locations(agg)
    write_trends(agg, months)
    write_dashboard(pages)
    append_log(agg)
    print(f"generated {len(pages) + 1} pages and "
          f"{len(list(CHARTS.glob('*.svg')))} charts from {agg['n_jobs']:,} postings")


if __name__ == "__main__":
    main()
