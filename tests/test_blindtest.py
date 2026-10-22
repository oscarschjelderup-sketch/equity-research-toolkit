"""Blind test: the judge's form carries no author, fairness warnings fire, answers aggregate by author."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "blindtest"))
import build_blindtest  # noqa: E402
import score_blindtest  # noqa: E402

SECTIONS = ["Thesis", "What is priced in", "Valuation", "Risks"]


def spec(texts):
    return {"id": "t1", "title": "Which is more thorough?", "documents": [
        {"author": author, "sections": [{"title": s, "text": t} for s in SECTIONS]} for author, t in texts.items()]}


def test_form_hides_authors_and_key_maps_back():
    page, key, warnings = build_blindtest.build(spec({"ours": "word " * 50, "consensus": "word " * 55}), salt="x")
    assert "ours" not in page and "consensus" not in page
    assert set(key["key"].values()) == {"ours", "consensus"} and all(k.startswith("doc-") for k in key["key"])
    assert all(k in page for k in key["key"]) and warnings == []


def test_fairness_warnings():
    _, _, warnings = build_blindtest.build(spec({"ours": "word " * 200, "consensus": "Pareto says " + "word " * 40}), salt="x")
    assert any("word counts" in w for w in warnings) and any("names a broker" in w for w in warnings)


def test_scores_aggregate_by_author():
    _, key, _ = build_blindtest.build(spec({"ours": "w " * 50, "consensus": "w " * 50}), salt="x")
    inv = {v: k for k, v in key["key"].items()}
    a1 = {"test": "t1", "judge": "AB", "ranks": {inv["ours"]: 1, inv["consensus"]: 2},
          "scores": {inv["ours"]: {"thesis": 5}, inv["consensus"]: {"thesis": 3}}}
    a2 = {"test": "t1", "judge": "CD", "ranks": {inv["ours"]: 2, inv["consensus"]: 1},
          "scores": {inv["ours"]: {"thesis": 4}, inv["consensus"]: {"thesis": 4}}}
    bad = {"test": "other", "judge": "EF", "ranks": {}, "scores": {}}
    res = score_blindtest.score(key, [a1, a2, bad])
    assert res["judges"] == 2 and res["skipped"] == ["EF"] and "anecdote" in res["note"]
    assert res["authors"]["ours"]["mean_rank"] == 1.5 and res["authors"]["ours"]["by_criterion"]["thesis"] == 4.5
