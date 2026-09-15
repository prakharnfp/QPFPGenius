"""
QPFP Genius — remote MCP server (custom connector for Claude).

Exposes the Network FP QPFP ProTool Formula Bible as callable tools so that any
Claude user can add one URL and get ProTool-faithful answers, with no project
setup, no file uploads and no local course folder.

Deploy: Railway / Render / Fly / Cloudflare. Listens on $PORT, path /mcp.
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from pathlib import Path

from fastmcp import FastMCP

DATA = Path(__file__).parent / "data"
BIBLE = (DATA / "formula_bible.md").read_text(encoding="utf-8")
PROTOCOL = (DATA / "operating_protocol.md").read_text(encoding="utf-8")

mcp = FastMCP(
    name="QPFP Genius",
    instructions=(
        "QPFP Genius is the Network FP QPFP (Qualified Personal Finance Professional) "
        "exam and practice engine. It carries two bodies of knowledge: (1) the live cell "
        "formulas, conventions and verified figures of all 36 official ProTool workbooks, "
        "and (2) the full course corpus — Handouts, PPTs and session material across "
        "Levels I, II and III.\n\n"
        "ALWAYS call `qpfp_operating_protocol` first in a conversation — it returns the "
        "answering protocol and the required 10-section output format.\n\n"
        "For CALCULATION questions: route with `route_question`, load the tool with "
        "`get_protool`, compute with `tvm_calculate`, sanity-check with "
        "`get_convention_register`.\n\n"
        "For THEORY, CONCEPT, DEFINITION, REGULATION or any other personal-finance "
        "question: use `search_course_content` to retrieve the Handout and PPT passages, "
        "and cite the session and file you answered from. Use `get_session_material` when "
        "the learner names a session.\n\n"
        "Never answer from generic financial theory when the corpus covers it. The "
        "ProTool's convention decides a calculated answer; textbook shortcuts manufacture "
        "the distractors. If neither the Bible nor the corpus covers a point, say so and "
        "flag the answer as not course-verified."
    ),
)

# ---------------------------------------------------------------- Bible index

_SECTION_RE = re.compile(r"^## ProTool (\d{2}) — (.+)$", re.M)
_PART_RE = re.compile(r"^# PART (\d) — (.+)$", re.M)


def _index_sections() -> dict[int, dict]:
    marks = [(m.start(), int(m.group(1)), m.group(2).strip()) for m in _SECTION_RE.finditer(BIBLE)]
    stops = sorted([m.start() for m in _PART_RE.finditer(BIBLE)] + [len(BIBLE)])
    out: dict[int, dict] = {}
    for i, (pos, num, title) in enumerate(marks):
        nxt = marks[i + 1][0] if i + 1 < len(marks) else len(BIBLE)
        hard = next((s for s in stops if s > pos), len(BIBLE))
        out[num] = {"title": title, "text": BIBLE[pos : min(nxt, hard)].rstrip()}
    return out


def _index_parts() -> dict[int, str]:
    marks = [(m.start(), int(m.group(1))) for m in _PART_RE.finditer(BIBLE)]
    out: dict[int, str] = {}
    for i, (pos, num) in enumerate(marks):
        nxt = marks[i + 1][0] if i + 1 < len(marks) else len(BIBLE)
        out[num] = BIBLE[pos:nxt].rstrip()
    return out


SECTIONS = _index_sections()
PARTS = _index_parts()

LEVEL = {**{n: "Level I" for n in range(1, 13)},
         **{n: "Level II" for n in range(13, 25)},
         **{n: "Level III" for n in range(25, 37)}}

# ------------------------------------------------------- course corpus + BM25

CORPUS_PATH = DATA / "course_corpus.json"
CORPUS: dict = {}
PASSAGES: list[dict] = []          # {doc, session, level, kind, file, text, tokens}
_DF: Counter = Counter()
_AVGLEN: float = 1.0

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOP = {
    "the", "a", "an", "of", "to", "in", "is", "and", "for", "on", "at", "as", "by",
    "it", "be", "are", "was", "with", "that", "this", "from", "or", "if", "will",
    "can", "has", "have", "not", "but", "which", "you", "your", "i", "we", "he",
    "she", "they", "his", "her", "their", "there", "what", "when", "how", "all",
    "any", "may", "than", "then", "so", "such", "into", "also", "its", "per",
}


def _tok(s: str) -> list[str]:
    return [t for t in _TOKEN_RE.findall(s.lower()) if t not in _STOP and len(t) > 1]


def _load_corpus() -> None:
    global CORPUS, PASSAGES, _DF, _AVGLEN
    if not CORPUS_PATH.exists():
        return
    try:
        CORPUS = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    except Exception:
        CORPUS = {}
        return
    for doc in CORPUS.get("docs", []):
        for ch in doc.get("chunks", []):
            PASSAGES.append({
                "title": doc.get("title", ""),
                "file": doc.get("file", ""),
                "session": doc.get("session"),
                "level": doc.get("level"),
                "kind": doc.get("kind", "other"),
                "text": ch,
                "tokens": _tok(ch),
            })
    for p in PASSAGES:
        _DF.update(set(p["tokens"]))
    if PASSAGES:
        _AVGLEN = sum(len(p["tokens"]) for p in PASSAGES) / len(PASSAGES)


def _bm25(query: str, pool: list[dict], top: int, k1: float = 1.5, b: float = 0.75):
    q = _tok(query)
    if not q or not pool:
        return []
    N = max(len(PASSAGES), 1)
    scored = []
    for p in pool:
        tf = Counter(p["tokens"])
        dl = len(p["tokens"]) or 1
        s = 0.0
        for term in q:
            f = tf.get(term, 0)
            if not f:
                continue
            idf = math.log(1 + (N - _DF[term] + 0.5) / (_DF[term] + 0.5))
            s += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * dl / _AVGLEN))
        if s > 0:
            scored.append((s, p))
    scored.sort(key=lambda x: -x[0])
    return scored[:top]


_load_corpus()

# Keyword → ProTool number. First match on a longer phrase wins.
ROUTES: list[tuple[str, int]] = [
    ("ppf", 30), ("public provident", 30), ("epf", 30), ("vpf", 30), ("nps", 30),
    ("gratuity", 30), ("employee benefit", 30), ("employment benefit", 30), ("eps", 30),
    ("retirement distribution", 20), ("bucket strategy", 20), ("bucket", 20),
    ("retirement corpus", 19), ("retirement accumulation", 19), ("retirement", 19),
    ("swp", 28), ("systematic withdrawal", 28), ("how long will the corpus last", 28),
    ("step-up sip", 27), ("stepup sip", 27), ("sip", 27),
    ("foreclose", 33), ("foreclosure", 33), ("prepay", 32), ("prepayment", 32),
    ("amortization", 32), ("amortisation", 32), ("emi", 32), ("home loan", 32),
    ("ltcg", 36), ("stcg", 36), ("capital gain", 36), ("indexation", 36),
    ("grandfather", 36), ("cii", 36), ("cost inflation", 36),
    ("hlv", 15), ("human life value", 15), ("sum assured", 15), ("life insurance", 15),
    ("emergency fund", 16), ("contingency fund", 16),
    ("children's education", 17), ("child education", 17), ("marriage goal", 17),
    ("children's future", 17), ("education goal", 17),
    ("rent vs", 34), ("rent versus", 34), ("buy vs rent", 34), ("rent or buy", 34),
    ("house purchase", 18), ("down payment", 18), ("downpayment", 18),
    ("old vs new regime", 21), ("income tax", 21), ("80c", 21), ("80d", 21),
    ("80ccd", 21), ("section 24", 21), ("surcharge", 21), ("87a", 21), ("hra", 21),
    ("savings ratio", 4), ("debt to income", 4), ("dti", 4), ("dta", 4),
    ("financial health", 4), ("ratio", 4),
    ("risk profil", 14), ("asset allocation", 24), ("portfolio return", 24),
    ("xirr", 6), ("cagr", 6), ("irr", 6), ("real return", 6), ("real rate", 6),
    ("effective rate", 6), ("absolute return", 6), ("rate of return", 6),
    ("rule of 72", 10), ("asset class", 10),
    ("will", 22), ("testator", 22), ("codicil", 22), ("succession", 22),
    ("health insurance", 26), ("co-pay", 26), ("restoration", 26), ("ped", 26),
    ("equity mf", 29), ("whitelist", 29), ("sharpe", 29), ("sortino", 29),
    ("modified duration", 31), ("ytm", 31), ("debt mf", 31),
    ("ethics", 3), ("code of conduct", 8), ("sebi", 8), ("amfi", 8), ("compliance", 8),
    ("fidok", 13), ("consultancy process", 11), ("goals matrix", 12),
    ("letter of engagement", 35), ("onboarding", 35),
    ("nper", 5), ("pmt", 5), ("present value", 5), ("future value", 5),
    ("annuity", 5), ("tvm", 5), ("time value", 5),
]

# --------------------------------------------------------------- TVM kernel


def _fv(r, n, pmt=0.0, pv=0.0, typ=0):
    if r == 0:
        return -(pv + pmt * n)
    return -(pv * (1 + r) ** n + pmt * (1 + r * typ) * (((1 + r) ** n - 1) / r))


def _pv(r, n, pmt=0.0, fv=0.0, typ=0):
    if r == 0:
        return -(fv + pmt * n)
    return -(pmt * (1 + r * typ) * ((1 - (1 + r) ** -n) / r) + fv * (1 + r) ** -n)


def _pmt(r, n, pv=0.0, fv=0.0, typ=0):
    if r == 0:
        return -(pv + fv) / n
    return -(pv * (1 + r) ** n + fv) / ((1 + r * typ) * (((1 + r) ** n - 1) / r))


def _nper(r, pmt, pv=0.0, fv=0.0, typ=0):
    from math import log
    if r == 0:
        return -(pv + fv) / pmt
    a = pmt * (1 + r * typ) / r
    return log((a - fv) / (a + pv)) / log(1 + r)


def _rate(n, pmt, pv, fv=0.0, typ=0):
    lo, hi = -0.9999, 10.0

    def f(r):
        return _fv(r, n, pmt, pv, typ) - fv

    flo = f(lo)
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = f(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def _periodic(rate: float, convention: str, periods_per_year: int) -> float:
    c = convention.upper()
    if c == "A":                       # EFFECT(NOMINAL(r,I),J)/I with I=J  ->  r/I
        return rate / periods_per_year
    if c == "B":                       # NOMINAL(effective, m)/m
        return periods_per_year * ((1 + rate) ** (1 / periods_per_year) - 1) / periods_per_year
    if c == "C":                       # (1+r)^(1/m) - 1
        return (1 + rate) ** (1 / periods_per_year) - 1
    if c == "D":                       # plain r/m
        return rate / periods_per_year
    raise ValueError("convention must be A, B, C or D")


# ------------------------------------------------------------------- tools


@mcp.tool
def qpfp_operating_protocol() -> str:
    """Return the QPFP Genius answering protocol and the mandatory 10-section output
    format. CALL THIS FIRST, before answering any QPFP exam or practice question.
    It configures how every subsequent answer in this conversation must be structured."""
    return PROTOCOL


@mcp.tool
def route_question(question: str) -> str:
    """Map a QPFP question to the correct ProTool. Pass the question text (or the key
    phrase from it). Returns the matched ProTool number, name, level and session, plus
    the periodic-rate convention that tool uses. Call this before get_protool."""
    q = question.lower()
    hits: list[int] = []
    for kw, num in ROUTES:
        if kw in q and num not in hits:
            hits.append(num)
    if not hits:
        return (
            "No keyword match. Use `list_protools` to pick manually, or "
            "`search_formula_bible` with a distinctive term from the question."
        )
    lines = ["# Routing result", ""]
    for num in hits[:4]:
        sec = SECTIONS.get(num, {})
        conv = {**{n: "A" for n in (5, 10)},
                **{n: "B" for n in (17, 18, 19, 28, 30)},
                **{n: "C" for n in (27,)},
                **{n: "D" for n in (32, 34)},
                33: "C for the SIP leg, D for the loan leg"}.get(num, "n/a")
        lines.append(
            f"**ProTool {num:02d} — {sec.get('title','(not in Bible)')}** · "
            f"{LEVEL.get(num,'?')} · Session {num:02d} · rate convention: {conv}"
        )
    lines.append("")
    lines.append(f"Primary match: **ProTool {hits[0]:02d}**. Now call "
                 f"`get_protool(protool_number={hits[0]})`.")
    if len(hits) > 1:
        lines.append("Secondary matches listed above — confirm against the question stem.")
    return "\n".join(lines)


@mcp.tool
def get_protool(protool_number: int) -> str:
    """Return the complete Formula Bible entry for one ProTool (1–36): input cell map,
    the live Excel cell formulas, the tool's conventions, the workbook's own verified
    figures, and the Case Study answer key for that session."""
    sec = SECTIONS.get(protool_number)
    if not sec:
        return f"No entry for ProTool {protool_number}. Valid range 1–36. Use `list_protools`."
    header = f"_{LEVEL.get(protool_number,'')} · Session {protool_number:02d}_\n\n"
    return header + sec["text"]


@mcp.tool
def list_protools() -> str:
    """List all 36 ProTools by number, name and level. Use when routing is ambiguous."""
    rows = ["| # | Level | ProTool |", "|---|---|---|"]
    for n in sorted(SECTIONS):
        rows.append(f"| {n:02d} | {LEVEL.get(n,'')} | {SECTIONS[n]['title']} |")
    return "\n".join(rows)


@mcp.tool
def get_convention_register() -> str:
    """Return the cross-tool convention register — the rules that decide the answer and
    the traps that manufacture the wrong options. Check this before finalising any
    calculated answer."""
    return PARTS.get(4, "Not found.")


@mcp.tool
def get_replication_kernel() -> str:
    """Return the Part 0 replication kernel: the exact Python equivalents of Excel's
    FV/PV/PMT/RATE/NPER, plus the four periodic-rate conventions and which ProTool
    uses each."""
    return PARTS.get(0, "Not found.")


@mcp.tool
def get_case_study_answers(protool_number: int | None = None) -> str:
    """Return the Trainers Sheet Case Study answer key — for one ProTool if a number is
    given, otherwise the full cross-tool index. Use to sanity-check a computed figure
    against the official workbook result."""
    full = PARTS.get(5, "Not found.")
    if protool_number is None:
        return full
    want = f"| {protool_number:02d} "
    rows = [ln for ln in full.splitlines() if ln.startswith(want)]
    if not rows:
        return f"No Case Study row for ProTool {protool_number}.\n\n{full}"
    return "\n".join(["| ProTool | Q1 | Q2 | Q3 |", "|---|---|---|---|", *rows])


@mcp.tool
def search_formula_bible(query: str, max_results: int = 6) -> str:
    """Full-text search across the entire Formula Bible. Returns matching lines with
    the ProTool they belong to. Use for a cell reference (e.g. 'D30'), a rule
    ('grandfathering'), a scheme term, or a figure you want to trace."""
    q = query.lower().strip()
    if not q:
        return "Empty query."
    out = []
    for num in sorted(SECTIONS):
        for ln in SECTIONS[num]["text"].splitlines():
            if q in ln.lower():
                out.append(f"**ProTool {num:02d} — {SECTIONS[num]['title']}**\n  {ln.strip()}")
                if len(out) >= max_results:
                    break
        if len(out) >= max_results:
            break
    if not out:
        for pnum, ptext in PARTS.items():
            for ln in ptext.splitlines():
                if q in ln.lower():
                    out.append(f"**Part {pnum}**\n  {ln.strip()}")
                    if len(out) >= max_results:
                        break
            if len(out) >= max_results:
                break
    return "\n\n".join(out) if out else f"No match for '{query}'."


@mcp.tool
def tvm_calculate(
    solve_for: str,
    rate: float,
    convention: str = "A",
    periods_per_year: int = 1,
    years: float | None = None,
    pv: float = 0.0,
    fv: float = 0.0,
    pmt: float = 0.0,
    annuity_type: int = 0,
) -> str:
    """Run a TVM calculation using a specific ProTool periodic-rate convention.

    solve_for: 'FV' | 'PV' | 'PMT' | 'NPER' | 'RATE'
    rate: annual rate as a decimal (0.12 for 12%)
    convention: 'A' (r/I, input nominal — ProTool 05, 10) | 'B' (NOMINAL(r,12)/12,
      input effective — ProTool 17/18/19/28/30-EPF) | 'C' ((1+r)^(1/12)−1 —
      ProTool 27, 33 SIP leg) | 'D' (plain r/12 — ProTool 32, 33 loan leg, 34)
    periods_per_year: 12 for monthly, 1 for annual
    annuity_type: 0 = end of period (ordinary), 1 = beginning (annuity-due)

    Excel sign convention applies: cash out is negative. Returns the periodic rate
    used and the result, so the convention is auditable.
    """
    pr = _periodic(rate, convention, periods_per_year)
    n = (years * periods_per_year) if years is not None else None
    s = solve_for.upper()

    if s in {"FV", "PV", "PMT"} and n is None:
        return "years is required for FV, PV and PMT."

    if s == "FV":
        res, label = _fv(pr, n, pmt, pv, annuity_type), "FV"
    elif s == "PV":
        res, label = _pv(pr, n, pmt, fv, annuity_type), "PV"
    elif s == "PMT":
        res, label = _pmt(pr, n, pv, fv, annuity_type), "PMT (per period)"
    elif s == "NPER":
        per = _nper(pr, pmt, pv, fv, annuity_type)
        res, label = per / periods_per_year, "NPER (years)"
    elif s == "RATE":
        if n is None:
            return "years is required for RATE."
        per = _rate(n, pmt, pv, fv, annuity_type)
        res, label = per * periods_per_year, "RATE (nominal annual)"
    else:
        return "solve_for must be FV, PV, PMT, NPER or RATE."

    return (
        f"**{label} = {res:,.4f}**\n\n"
        f"- Convention **{convention.upper()}** → periodic rate = {pr:.10f} "
        f"({pr*100:.6f}% per period)\n"
        f"- Periods = {n if n is not None else 'solved'} "
        f"({periods_per_year}/yr), Type = {annuity_type} "
        f"({'begin' if annuity_type else 'end'} of period)\n"
        f"- Inputs: PV={pv:,.2f} · FV={fv:,.2f} · PMT={pmt:,.2f}\n\n"
        f"Verify the convention against `get_protool` before reporting this figure."
    )


@mcp.tool
def search_course_content(
    query: str,
    session: int | None = None,
    kind: str | None = None,
    max_results: int = 5,
) -> str:
    """Search the full QPFP course corpus — Handouts, PPTs and session material across
    all three Levels. Use this for ANY theory, concept, definition, regulation, product
    or process question, and for anything the Formula Bible does not cover.

    query: natural-language question or key terms
    session: optional 1–36 filter
    kind: optional 'handout' | 'ppt' | 'protool' | 'assessment'
    Returns ranked passages with their session, file and Level, for citation.
    """
    if not PASSAGES:
        return (
            "Course corpus not loaded. Only the ProTool Formula Bible is available "
            "on this server — use `get_protool`, `search_formula_bible` and "
            "`list_protools`. (To add the corpus, run ingest.py over the course "
            "folder and redeploy.)"
        )
    pool = PASSAGES
    if session is not None:
        pool = [p for p in pool if p["session"] == session]
    if kind:
        pool = [p for p in pool if p["kind"] == kind.lower()]
    if not pool:
        return f"No material matches session={session}, kind={kind}."

    hits = _bm25(query, pool, max(1, min(max_results, 10)))
    if not hits:
        return (
            f"No course passage matches '{query}'. Try broader terms, or "
            f"`search_formula_bible` if this is a ProTool calculation point."
        )
    out = [f"# Course corpus — {len(hits)} passage(s) for: {query}", ""]
    for score, p in hits:
        sess = f"Session {p['session']:02d}" if p["session"] else "unmapped"
        out.append(
            f"---\n**{p['title']}** · {p['level'] or '?'} · {sess} · "
            f"{p['kind']} · _relevance {score:.1f}_\n"
            f"`{p['file']}`\n\n{p['text']}\n"
        )
    out.append(
        "---\nCite the session and file above in section 8 of your answer. "
        "If the passage does not settle the question, say so rather than extrapolating."
    )
    return "\n".join(out)


@mcp.tool
def get_session_material(session_number: int, kind: str | None = None) -> str:
    """List every course document held for one session (1–36) — Handouts, PPTs,
    workbooks — with a preview of each. Use when the learner names a session, then
    follow up with `search_course_content(session=N, query=...)` for the detail."""
    if not PASSAGES:
        return "Course corpus not loaded on this server. See `corpus_status`."
    docs = [d for d in CORPUS.get("docs", []) if d.get("session") == session_number]
    if kind:
        docs = [d for d in docs if d.get("kind") == kind.lower()]
    if not docs:
        return (
            f"No course material for session {session_number}"
            f"{f' of kind {kind}' if kind else ''}. "
            f"The ProTool logic is still available via `get_protool({session_number})`."
        )
    out = [f"# Session {session_number:02d} — {LEVEL.get(session_number,'')}", ""]
    for d in docs:
        preview = d["chunks"][0][:400].replace("\n", " ") if d.get("chunks") else ""
        out.append(
            f"**{d['title']}** · {d['kind']} · {len(d.get('chunks', []))} passages\n"
            f"`{d['file']}`\n\n> {preview}…\n"
        )
    return "\n".join(out)


@mcp.tool
def corpus_status() -> str:
    """Report what course material this server is carrying — document count, passage
    count, sessions covered, and when it was last ingested. Use to check coverage
    before telling a learner something is not in the course."""
    lines = [
        "# QPFP Genius coverage", "",
        f"- ProTool Formula Bible: **{len(SECTIONS)}/36** tools, "
        f"Parts {', '.join(str(p) for p in sorted(PARTS))}",
    ]
    if not PASSAGES:
        lines += [
            "- Course corpus: **not loaded**",
            "",
            "Only ProTool logic is available. Theory questions should be answered from "
            "the framework entries (ProTools 03, 08, 09, 11, 12, 13, 14, 22, 25, 26, "
            "29, 31, 35) and flagged where the course text would be needed.",
        ]
        return "\n".join(lines)
    sessions = sorted({d["session"] for d in CORPUS.get("docs", []) if d.get("session")})
    missing = [n for n in range(1, 37) if n not in sessions]
    kinds = Counter(d.get("kind") for d in CORPUS.get("docs", []))
    lines += [
        f"- Course corpus: **{CORPUS.get('doc_count', 0)} documents**, "
        f"**{CORPUS.get('chunk_count', 0):,} passages**",
        f"- Sessions covered: **{len(sessions)}/36**",
        f"- By kind: " + " · ".join(f"{k} {v}" for k, v in kinds.most_common()),
        f"- Ingested: {CORPUS.get('generated', 'unknown')}",
    ]
    if missing:
        lines.append(f"- **No course text for sessions: {missing}** — answer those from "
                     f"the Formula Bible and flag the gap.")
    return "\n".join(lines)


@mcp.prompt
def answer_qpfp_question(question: str) -> str:
    """Prepared prompt: answer a QPFP exam question in the full 10-section format."""
    return (
        f"{PROTOCOL}\n\n---\n\nNow answer this QPFP question, following the workflow "
        f"and the 10-section output format exactly:\n\n{question}"
    )


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        # Set MCP_PATH in Railway to something unguessable (e.g. /b15-9f3a2c71/mcp)
        # to turn the URL itself into a revocable access key. Change it to revoke.
        path=os.environ.get("MCP_PATH", "/mcp"),
    )
