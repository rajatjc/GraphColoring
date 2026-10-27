import csv

from coloring import study


def test_study_writes_csvs_and_chart(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "FIRST_FIT_NS", [10, 20])
    monkeypatch.setattr(study, "CBIP_NS", [10, 20])

    study.main(["--instances", "3", "--seed", "1", "--out", str(tmp_path)])

    with (tmp_path / "first_fit.csv").open() as f:
        first_fit = list(csv.DictReader(f))
    with (tmp_path / "cbip.csv").open() as f:
        bipartite = list(csv.DictReader(f))

    assert [(r["k"], r["n"]) for r in first_fit] == [("2", "10"), ("2", "20"), ("3", "10"), ("3", "20"), ("4", "10"), ("4", "20")]
    assert {r["algorithm"] for r in bipartite} == {"first-fit", "cbip"}
    assert all(float(r["best"]) <= float(r["average"]) <= float(r["worst"]) for r in first_fit + bipartite)
    assert (tmp_path / "ratios.png").read_bytes().startswith(b"\x89PNG")
