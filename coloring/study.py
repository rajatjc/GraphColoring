"""Reproduce the experiments from the notebooks: average competitive ratio as n grows.

    python -m coloring.study                    # 100 graphs per point, a couple of minutes
    python -m coloring.study --instances 1000   # the original N=1000 study, about 20 minutes

Writes results/first_fit.csv, results/cbip.csv and results/ratios.png.
"""

import argparse
import csv
import random
import time
from pathlib import Path

from coloring.experiment import run_trials

FIRST_FIT_KS = [2, 3, 4]
FIRST_FIT_NS = [50, 100, 200, 400, 600, 800, 1000, 1400, 1600]
CBIP_NS = list(range(10, 101, 10))


def sweep(algorithms, k, ns, instances, rng, label):
    rows = []
    for n in ns:
        started = time.perf_counter()
        trials = run_trials(algorithms, n, k, instances, rng)
        for result in trials.results:
            rows.append({"algorithm": result.algorithm, "k": k, "n": n, "instances": instances,
                         "average": round(result.average, 4), "best": round(result.best, 4),
                         "worst": round(result.worst, 4)})
        summary = ", ".join(f"{r.label} {r.average:.3f}" for r in trials.results)
        print(f"{label} k={k} n={n:>4}: {summary}  ({time.perf_counter() - started:.1f}s)", flush=True)
    return rows


def write_csv(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def plot(first_fit_rows, cbip_rows, path):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.2))
    for k in FIRST_FIT_KS:
        rows = [r for r in first_fit_rows if r["k"] == k]
        left.plot([r["n"] for r in rows], [r["average"] for r in rows], marker="o", label=f"k = {k}")
    left.set(title="First-Fit on random k-colorable graphs", xlabel="vertices n", ylabel="average competitive ratio")
    left.legend()

    for name, label in [("first-fit", "First-Fit"), ("cbip", "CBIP")]:
        rows = [r for r in cbip_rows if r["algorithm"] == name]
        right.plot([r["n"] for r in rows], [r["average"] for r in rows], marker="o", label=label)
    right.set(title="CBIP vs First-Fit on the same bipartite graphs", xlabel="vertices n")
    right.legend()

    for ax in (left, right):
        ax.grid(alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--instances", type=int, default=100, help="random graphs per point (default 100)")
    parser.add_argument("--seed", type=int, default=2023, help="random seed (default 2023)")
    parser.add_argument("--out", type=Path, default=Path("results"), help="output folder (default results/)")
    args = parser.parse_args(argv)

    rng = random.Random(args.seed)
    args.out.mkdir(parents=True, exist_ok=True)

    first_fit_rows = []
    for k in FIRST_FIT_KS:
        first_fit_rows += sweep(["first-fit"], k, FIRST_FIT_NS, args.instances, rng, "First-Fit")
    cbip_rows = sweep(["first-fit", "cbip"], 2, CBIP_NS, args.instances, rng, "Bipartite")

    write_csv(args.out / "first_fit.csv", first_fit_rows)
    write_csv(args.out / "cbip.csv", cbip_rows)
    plot(first_fit_rows, cbip_rows, args.out / "ratios.png")
    print(f"Wrote {args.out}/first_fit.csv, {args.out}/cbip.csv and {args.out}/ratios.png")


if __name__ == "__main__":
    main()
