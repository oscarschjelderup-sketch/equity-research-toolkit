# Blind test

Lets finance professionals judge which write-up of a case is most thorough without knowing who wrote it.
`build_blindtest.py spec.yaml --out out/ --strict` writes `out/<id>.html` (send to judges: documents under opaque
ids, order shuffled per judge, an answer to copy or download) and `out/<id>.key.json` (keep: which id is whose).
`score_blindtest.py out/<id>.key.json answers/*.json` aggregates the answers by author; fewer than five judges is
reported as anecdote.

Fairness, enforced by `--strict`: the same sections in the same order, word counts within ±25 %, no broker,
analyst or tool names, no TODO left. Writing the documents to that standard is the organiser's job.

Specs:
- `specs/sats.yaml` – our case, a consensus summary from public data, and a third document (the strongest published
  broker arguments) that must be written from material the organiser has lawful access to; the full broker reports
  are behind portals and paywalls (docs/research/02 section 5). Until it is written, `--strict` refuses to build.
- Private cases get their specs outside the repository. A newly listed company needs analyst coverage first: a
  spec can be written only after the first initiations.

`out/`, `*.key.json` and `specs/private-*.yaml` are git-ignored.
