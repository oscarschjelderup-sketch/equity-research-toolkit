"""HTML building blocks, number formats and the print stylesheet for the research report.

Every exhibit (table or chart) goes through `exhibit()`, which forces a source line and a date – the test suite checks
that no exhibit is without one. Estimates are marked EST in column headers through `est_header()`.
"""
from __future__ import annotations

import html
import math

NAVY, LBLUE, MIDBLUE, PALEBLUE = "#003255", "#81B0C0", "#4F7FA0", "#D6E6EC"
GREEN, RED, AMBER, GREY = "#2E7D32", "#C00000", "#C9A227", "#6B6B6B"
NA = "not available"


# ------------------------------------------------------------------ numbers
def isnum(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and not (isinstance(x, float) and math.isnan(x))


def num(x, d=0, paren=True, dash="–"):
    """1 234 / (56) – thousands separated by a thin space, negatives in parentheses."""
    if not isnum(x):
        return dash if x in (None, "") else html.escape(str(x))
    if d == 0 and abs(x) < 0.5:
        return "0"
    s = f"{abs(x):,.{d}f}".replace(",", " ")
    if x < 0:
        return f"({s})" if paren else f"-{s}"
    return s


def pct(x, d=1, sign=False, dash="–"):
    if not isnum(x):
        return "n.m." if isinstance(x, str) and x else dash
    s = f"{abs(x) * 100:.{d}f}%"
    if x < 0:
        return f"({s})"
    return ("+" if sign and x > 0 else "") + s


def pp(x, d=1):
    """Percentage-point difference with a sign."""
    if not isnum(x):
        return "–"
    return f"{x * 100:+.{d}f}pp"


def mult(x, d=1):
    if not isnum(x) or x <= 0 or x > 500:
        return "n.m."
    return f"{x:.{d}f}x"


def nok(x, d=0):
    if not isnum(x):
        return "–"
    return f"NOK {num(x, d, paren=False)}"


def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=False)


def md(s) -> str:
    """Minimal inline markup: **bold** only (the case text files use it)."""
    s = esc(s)
    out, bold = [], False
    for part in s.split("**"):
        out.append(f"<b>{part}</b>" if bold else part)
        bold = not bold
    return "".join(out)


# ------------------------------------------------------------------ html blocks
def est_header(label: str, estimate: bool) -> str:
    return f"{esc(label)}<span class='est'>EST</span>" if estimate else esc(label)


def table(headers, rows, cls="num", widths=None, first_left=True, bold_rows=(), rules_before=(), left=()):
    """A table. `headers` are already-escaped strings (use est_header); cells are strings. The first column and the
    columns listed in `left` are text (left-aligned, wrapping); the rest are numbers (right-aligned)."""
    txt = set(left) | ({0} if first_left else set())
    th = "".join(f"<th{' class=\"txt\"' if i in txt else ''}>{h}</th>" for i, h in enumerate(headers))
    cg = ""
    if widths:
        cg = "<colgroup>" + "".join(f"<col style='width:{w}'>" for w in widths) + "</colgroup>"
    body = []
    for ri, r in enumerate(rows):
        tds = "".join(f"<td{' class=\"txt\"' if i in txt else ''}>{c}</td>" for i, c in enumerate(r))
        classes = []
        if ri in bold_rows:
            classes.append("b")
        if ri in rules_before:
            classes.append("rule")
        cl = f" class='{' '.join(classes)}'" if classes else ""
        body.append(f"<tr{cl}>{tds}</tr>")
    return f"<table class='{cls}'>{cg}<thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def exhibit(title: str, body: str, source: str, date: str, note: str | None = None, cls: str = "") -> str:
    """A figure with a mandatory source and date. `date` is the date of the data (not the build date)."""
    if not source or not date:
        raise ValueError(f"exhibit '{title}' needs a source and a date")
    n = f"<div class='note'>Note: {md(note)}</div>" if note else ""
    return (f"<figure class='ex {cls}'><figcaption>{md(title)}</figcaption>{body}{n}"
            f"<div class='src'>Source: {md(source)}. Data as of {esc(date)}.</div></figure>")


def section(sid: str, title: str, lead: str | None = None, body: str = "", number: int | None = None, cont: bool = False) -> str:
    """A numbered section on a new page; `cont=True` lets a short section (a single placeholder) follow on the same page."""
    n = f"<span class='n'>{number}</span>" if number else ""
    l_ = f"<p class='lead'>{md(lead)}</p>" if lead else ""
    return f"<section id='{sid}' class='sec{' cont' if cont else ''}'><h1>{n}{esc(title)}</h1>{l_}{body}</section>"


def h2(t):
    return f"<h2>{md(t)}</h2>"


def h3(t):
    return f"<h3>{md(t)}</h3>"


def p(t, cls=""):
    c = f" class='{cls}'" if cls else ""
    return f"<p{c}>{md(t)}</p>"


def ul(items, cls=""):
    c = f" class='{cls}'" if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{md(i)}</li>" for i in items) + "</ul>"


def box(title, body, cls=""):
    return f"<div class='box {cls}'><div class='bt'>{md(title)}</div>{body}</div>"


def cols(*parts, widths=None):
    if widths is None:
        widths = [f"{100 / len(parts):.1f}%"] * len(parts)
    return "<div class='cols'>" + "".join(f"<div class='col' style='width:{w}'>{b}</div>" for b, w in zip(parts, widths)) + "</div>"


def kv(rows, cls="kv"):
    return f"<table class='{cls}'>" + "".join(f"<tr><td class='txt'>{md(k)}</td><td>{v}</td></tr>" for k, v in rows) + "</table>"


def placeholder(what: str, how: str = "") -> str:
    """A visible gap: data not collected or not available – never an invented number."""
    return f"<div class='gap'><b>{esc(what)}</b>{(' – ' + md(how)) if how else ''}</div>"


def page_break():
    return "<div class='pb'></div>"


# ------------------------------------------------------------------ stylesheet
def css(runhead: str, rundate: str) -> str:
    """The stylesheet with the running header filled in (Chromium prints @page margin boxes with static content)."""
    q = lambda s: str(s).replace("\\", "\\\\").replace('"', '\\"')  # noqa: E731
    return CSS.replace("__RUNHEAD__", q(runhead)).replace("__RUNDATE__", q(rundate))


CSS = """
@page { size: A4; margin: 17mm 14mm 16mm 14mm;
  @top-left { content: "__RUNHEAD__"; font: 7pt Arial, Helvetica, sans-serif; color: #003255; }
  @top-right { content: "__RUNDATE__"; font: 7pt Arial, Helvetica, sans-serif; color: #003255; }
  @bottom-left { content: "A student case study and a process document – not investment research or investment advice."; font: 6.5pt Arial, Helvetica, sans-serif; color: #6B6B6B; }
  @bottom-right { content: counter(page); font: 7.5pt Arial, Helvetica, sans-serif; color: #003255; } }
@page :first { @top-left { content: none; } @top-right { content: none; } }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font: 10pt/1.38 Arial, Helvetica, sans-serif; color: #111; background: #fff; }
.runhead { string-set: runhead content(text); } .rundate { string-set: rundate content(text); }
.hidden { position: absolute; left: -9999px; top: 0; font-size: 1pt; }
h1 { font: 700 16pt/1.15 Arial, Helvetica, sans-serif; color: #003255; margin: 0 0 6px 0; padding-bottom: 4px; border-bottom: 1.5px solid #003255; }
h1 .n { display: inline-block; min-width: 22px; color: #81B0C0; margin-right: 6px; }
h2 { font: 700 11pt/1.2 Arial, Helvetica, sans-serif; color: #003255; margin: 10px 0 4px 0; }
h3 { font: 700 9pt/1.2 Arial, Helvetica, sans-serif; color: #4F7FA0; margin: 8px 0 3px 0; }
p { margin: 0 0 5px 0; text-align: left; }
p.lead { font-size: 10.6pt; color: #003255; margin-bottom: 8px; }
ul { margin: 0 0 5px 0; padding-left: 13px; } li { margin: 0 0 2px 0; }
ul.tight li { margin: 0; }
.sec { break-before: page; }
.sec.first { break-before: auto; }
.sec.cont { break-before: auto; margin-top: 14px; }
.pb { break-after: page; }
.cols { display: flex; gap: 12px; align-items: flex-start; } .col { min-width: 0; }
.box { border: 1px solid #D6E6EC; padding: 6px 8px; margin: 4px 0 8px 0; background: #fff; break-inside: avoid; }
.box .bt { font-weight: 700; color: #003255; margin-bottom: 3px; font-size: 9pt; }
.box.grey { background: #F2F6F8; }
.box.navy { background: #003255; color: #fff; } .box.navy .bt { color: #81B0C0; }
figure.ex { margin: 6px 0 10px 0; break-inside: avoid; }
figure.ex figcaption { font-weight: 700; color: #003255; font-size: 9.6pt; margin: 0 0 3px 0; padding-bottom: 2px; border-bottom: 1px solid #81B0C0; }
figure.ex .src { font-size: 7.4pt; color: #6B6B6B; margin-top: 2px; }
figure.ex .note { font-size: 7.4pt; color: #444; margin-top: 2px; }
figure.ex svg { width: 100%; height: auto; display: block; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; }
table.num th, table.num td { padding: 2.6px 4px; text-align: right; white-space: nowrap; }
table.num th { background: #003255; color: #fff; font-weight: 700; border-bottom: 1px solid #003255; }
table.num td { border-bottom: 0.5px solid #E3EAEE; }
table.num th.txt, table.num td.txt { text-align: left; white-space: normal; }
table.num tr.b td { font-weight: 700; }
table.num tr.rule td { border-top: 1px solid #003255; }
table.num tbody tr:nth-child(even) td { background: #FAFCFD; }
table.kv { font-size: 8.5pt; } table.kv td { padding: 2.4px 3px; border-bottom: 0.5px solid #E3EAEE; text-align: right; white-space: nowrap; }
table.kv td.txt { text-align: left; color: #333; white-space: normal; }
table.wrap td, table.wrap th { white-space: normal !important; vertical-align: top; }
.est { display: inline-block; font-size: 5.6pt; font-weight: 700; color: #003255; background: #D6E6EC; border-radius: 2px; padding: 0 2px; margin-left: 3px; vertical-align: 1px; }
th .est { color: #003255; background: #D6E6EC; }
.gap { border: 1px dashed #C9A227; background: #FFFBEA; color: #5a4a00; padding: 4px 7px; font-size: 8pt; margin: 4px 0 8px 0; break-inside: avoid; }
.na { color: #6B6B6B; font-style: italic; }
.pos { color: #2E7D32; } .neg { color: #C00000; }
.tag { display: inline-block; font-size: 6.6pt; font-weight: 700; padding: 1px 5px; border-radius: 2px; color: #fff; background: #4F7FA0; }
.tag.buy { background: #2E7D32; } .tag.sell { background: #C00000; } .tag.hold { background: #C9A227; }
.tag.ok { background: #2E7D32; } .tag.watch { background: #C9A227; } .tag.broken { background: #C00000; } .tag.na { background: #6B6B6B; }
/* front page */
.front { display: flex; gap: 14px; }
.front .main { width: 63%; } .front .rail { width: 37%; }
.front .brand { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #003255; padding-bottom: 4px; margin-bottom: 10px; }
.front .brand .t1 { font: 700 9pt Arial; color: #003255; letter-spacing: 0.4px; }
.front .brand .t2 { font: 7pt Arial; color: #6B6B6B; }
.front .co { font: 700 22pt/1.05 Arial; color: #003255; margin: 2px 0 0 0; }
.front .title { font: 400 15pt/1.15 Arial; color: #003255; margin: 2px 0 8px 0; }
.front .abstract { font-size: 10.6pt; line-height: 1.3; color: #222; margin-bottom: 9px; }
.front .memo p { margin-bottom: 6px; }
.front .memo b.h { color: #003255; }
.front .rec { border: 1.5px solid #003255; padding: 6px 9px; margin-bottom: 8px; }
.front .rec .r1 { font: 700 20pt/1 Arial; color: #003255; }
.front .rec .r2 { font: 700 12pt/1.3 Arial; color: #003255; }
.front .rec .r3 { font-size: 7.6pt; color: #333; }
.front .rail h4 { font: 700 7.6pt Arial; color: #003255; margin: 7px 0 2px 0; border-bottom: 1px solid #81B0C0; text-transform: uppercase; letter-spacing: 0.3px; }
.front .rail table.kv { font-size: 7.6pt; }
.front .fin { margin-top: 8px; }
.front .fin table { font-size: 7.8pt; }
.front .disc { font-size: 6.6pt; color: #444; border-top: 1px solid #81B0C0; margin-top: 8px; padding-top: 3px; }
.front .analysts { font-size: 7pt; margin-top: 6px; color: #333; }
/* misc */
.small { font-size: 8pt; } .muted { color: #6B6B6B; }
.toc td { padding: 1.5px 4px; border-bottom: 0.5px dotted #B8CBD4; font-size: 8pt; }
.kill td { vertical-align: top; }
.center { text-align: center; }
.legend { font-size: 7.4pt; color: #444; }
"""
