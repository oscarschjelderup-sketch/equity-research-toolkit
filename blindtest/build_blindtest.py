"""Blind test: let a finance professional judge which case write-up is more thorough without knowing who wrote it.

Input: a YAML spec with the documents (our case summary, an anonymised consensus summary, a summary of the best
analysts' arguments ...), each with an author label that never reaches the judge. Output:

- ``<name>.html``: a self-contained form for the judges. Documents appear under opaque ids (``doc-3f9a``) in an
  order shuffled per judge (seeded by the judge's initials, so a judge who reloads sees the same order). The judge
  scores each document on the criteria (1-5), ranks them on thoroughness and comments; the form produces a JSON
  answer to copy or download and send back. No author label is in the file.
- ``<name>.key.json``: the mapping from opaque id to author, kept by the organiser. Do not send it.

``score_blindtest.py`` aggregates the answers with the key. Fairness rules (enforced where possible): every document
uses the same sections in the same order, word counts within ±25 % of each other (the build warns otherwise), no
names of brokers or analysts, no formatting tells. Writing the documents to that standard is the organiser's job.

    python build_blindtest.py specs/sats.yaml --out out/
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import secrets
import sys
from pathlib import Path

import yaml

DEFAULT_CRITERIA = [
    ("thesis", "The thesis is clear and specific: what the market misses, in one or two sentences"),
    ("priced_in", "It states what the share price implies (in numbers) and where the view differs"),
    ("evidence", "Claims are backed by evidence and sources (reported figures, not assertions)"),
    ("valuation", "The valuation is rigorous and consistent (method, WACC, terminal value, peers)"),
    ("risks", "Risks are specific, with what would prove the view wrong (kill criteria)"),
    ("catalysts", "Catalysts and checkpoints are dated"),
    ("numbers", "The forecasts are explained driver by driver (not just a target)"),
]
BANNED = re.compile(r"\b(DNB|Carnegie|Pareto|ABG|Arctic|SB1|SpareBank 1 Markets|Nordea|SEB|Danske|Kepler|Clarksons|Fearnley|"
                    r"Oscar|Claude|Toolkit)\b", re.I)


def _opaque(seed: str) -> str:
    return "doc-" + hashlib.sha256(seed.encode()).hexdigest()[:4]


def build(spec: dict, salt: str | None = None) -> tuple[str, dict, list[str]]:
    salt = salt or secrets.token_hex(8)
    docs = spec["documents"]
    warnings = []
    words = {d["author"]: len(re.findall(r"\w+", " ".join(s["text"] for s in d["sections"]))) for d in docs}
    lo, hi = min(words.values()), max(words.values())
    if lo and hi / lo > 1.25 / 0.75:
        warnings.append(f"word counts differ too much ({words}); a judge can tell the long one apart")
    sections = [[s["title"] for s in d["sections"]] for d in docs]
    if any(s != sections[0] for s in sections):
        warnings.append("the documents do not use the same sections in the same order")
    for d in docs:
        for s in d["sections"]:
            if BANNED.search(s["text"]) or BANNED.search(s["title"]):
                warnings.append(f"{d['author']}: section '{s['title']}' names a broker, analyst or the tool")
    for d in docs:
        if any("TODO" in s["text"] for s in d["sections"]):
            warnings.append(f"{d['author']}: still contains TODO – the document is not written yet")
    key, payload = {}, []
    for i, d in enumerate(docs):
        oid = _opaque(f"{salt}:{i}:{d['author']}")
        key[oid] = d["author"]
        payload.append({"id": oid, "sections": [{"title": s["title"], "text": s["text"]} for s in d["sections"]]})
    criteria = spec.get("criteria") or [{"id": c, "text": t} for c, t in DEFAULT_CRITERIA]
    page = PAGE.replace("__TITLE__", html.escape(spec["title"])) \
               .replace("__INTRO__", html.escape(spec.get("intro", ""))) \
               .replace("__TEST__", html.escape(spec["id"])) \
               .replace("__DATA__", json.dumps({"test": spec["id"], "docs": payload, "criteria": criteria}, ensure_ascii=False))
    return page, {"test": spec["id"], "salt": salt, "key": key, "word_counts": words}, warnings


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#f4f6f8;--card:#fff;--text:#1b2430;--muted:#5f6b7a;--line:#dde3ea;--accent:#003255}
@media (prefers-color-scheme:dark){:root{--bg:#111820;--card:#1a2330;--text:#e6ecf2;--muted:#9aa7b5;--line:#2a3647;--accent:#9ec3d1}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 -apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:20px 16px 60px}h1{font-size:24px;margin:0 0 6px}.muted{color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}
.docs{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.doc h2{font-size:17px;margin:0 0 8px;color:var(--accent)}.doc h3{font-size:14px;margin:12px 0 4px}.doc p{margin:0 0 6px;white-space:pre-wrap}
table{border-collapse:collapse;width:100%}td,th{border-top:1px solid var(--line);padding:6px;text-align:left;vertical-align:top;font-size:14px}
select,input,textarea{font:inherit;padding:6px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--text)}
textarea{width:100%;min-height:70px}button{font:inherit;padding:9px 16px;border-radius:8px;border:0;background:var(--accent);color:#fff;cursor:pointer}
pre{white-space:pre-wrap;word-break:break-all;background:var(--bg);padding:10px;border-radius:8px;font-size:12px}
</style></head><body><div class="wrap">
<h1>__TITLE__</h1><p class="muted">__INTRO__</p>
<div class="card"><label>Your initials (used only to fix the order of the documents): <input id="judge" maxlength="8" size="8"></label>
<button id="start" type="button">Show the documents</button></div>
<div id="main" hidden>
<div class="docs" id="docs"></div>
<div class="card"><h2 style="font-size:17px;margin:0 0 6px">Score each document (1 = poor, 5 = excellent)</h2><table id="scores"></table></div>
<div class="card"><h2 style="font-size:17px;margin:0 0 6px">Overall</h2>
<p>Rank the documents by thoroughness (1 = most thorough): <span id="ranks"></span></p>
<p><label>Your background (e.g. sell-side analyst, portfolio manager, student): <input id="bg" size="40"></label></p>
<p>Comments – what made the best one better?</p><textarea id="comment"></textarea>
<p><button id="done" type="button">Produce my answer</button></p><div id="out" hidden><p>Send this answer back (copy or download):</p><pre id="json"></pre>
<button id="dl" type="button">Download answer</button></div></div>
</div></div>
<script>
const DATA = __DATA__;
function seeded(s){let h=2166136261;for(const c of s){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return()=>{h^=h<<13;h^=h>>>17;h^=h<<5;return((h>>>0)%1e6)/1e6}}
function esc(t){return String(t).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]))}
let order=[];
document.getElementById("start").onclick=()=>{
  const j=document.getElementById("judge").value.trim().toUpperCase(); if(!j){alert("Initials first");return}
  const rnd=seeded(DATA.test+":"+j); order=DATA.docs.map(d=>d).sort(()=>rnd()-0.5);
  const labels="ABCDEFGH";
  document.getElementById("docs").innerHTML=order.map((d,i)=>`<div class="card doc"><h2>Document ${labels[i]}</h2>`+
    d.sections.map(s=>`<h3>${esc(s.title)}</h3><p>${esc(s.text)}</p>`).join("")+`</div>`).join("");
  const head=`<tr><th>Criterion</th>${order.map((d,i)=>`<th>Doc ${labels[i]}</th>`).join("")}</tr>`;
  const sel=(cid,did)=>`<select data-c="${cid}" data-d="${did}"><option value="">–</option>${[1,2,3,4,5].map(v=>`<option>${v}</option>`).join("")}</select>`;
  document.getElementById("scores").innerHTML=head+DATA.criteria.map(c=>`<tr><td>${esc(c.text)}</td>${order.map(d=>`<td>${sel(c.id,d.id)}</td>`).join("")}</tr>`).join("");
  document.getElementById("ranks").innerHTML=order.map((d,i)=>` Doc ${labels[i]} <select data-r="${d.id}">${order.map((_,k)=>`<option>${k+1}</option>`).join("")}</select>`).join(" ");
  document.getElementById("main").hidden=false;
};
document.getElementById("done").onclick=()=>{
  const scores={};document.querySelectorAll("select[data-c]").forEach(s=>{(scores[s.dataset.d]??={})[s.dataset.c]=s.value?+s.value:null});
  const ranks={};document.querySelectorAll("select[data-r]").forEach(s=>ranks[s.dataset.r]=+s.value);
  if(new Set(Object.values(ranks)).size!==order.length){alert("Give each document a different rank");return}
  const ans={test:DATA.test,judge:document.getElementById("judge").value.trim().toUpperCase(),background:document.getElementById("bg").value,
    shown_order:order.map(d=>d.id),scores,ranks,comment:document.getElementById("comment").value,answered_at:new Date().toISOString()};
  const txt=JSON.stringify(ans,null,1);document.getElementById("json").textContent=txt;document.getElementById("out").hidden=false;
  document.getElementById("dl").onclick=()=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([txt],{type:"application/json"}));
    a.download=`${DATA.test}-${ans.judge||"judge"}.json`;a.click()};
};
</script></body></html>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out", default=".")
    ap.add_argument("--strict", action="store_true", help="Fail on any fairness warning.")
    a = ap.parse_args(argv)
    spec = yaml.safe_load(Path(a.spec).read_text(encoding="utf8"))
    page, key, warnings = build(spec)
    for w in warnings:
        print("WARNING:", w)
    if warnings and a.strict:
        print("not built (--strict): fix the warnings first")
        return 1
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{spec['id']}.html").write_text(page, encoding="utf8")
    (out / f"{spec['id']}.key.json").write_text(json.dumps(key, indent=1), encoding="utf8")
    print(f"written {out / (spec['id'] + '.html')} (send to judges) and {spec['id']}.key.json (keep)")
    return 1 if (warnings and a.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
