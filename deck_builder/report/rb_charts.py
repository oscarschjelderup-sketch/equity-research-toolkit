"""Charts for the report: matplotlib rendered to inline SVG (text stays text, so the HTML remains searchable).

Every function returns an SVG string ready to drop into an exhibit. Colours follow the toolkit palette.
"""
from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402


def _dates(ax, x):
    """Readable date axis: at most seven ticks, concise labels."""
    import datetime as _dt
    if x and isinstance(x[0], (_dt.date, _dt.datetime)):
        loc = mdates.AutoDateLocator(maxticks=7)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

NAVY, LBLUE, MIDBLUE, PALEBLUE = "#003255", "#81B0C0", "#4F7FA0", "#D6E6EC"
GREEN, RED, AMBER, GREY = "#2E7D32", "#C00000", "#C9A227", "#8A8A8A"
PALETTE = [NAVY, LBLUE, MIDBLUE, GREEN, AMBER, GREY, "#B5651D", "#7B4F9D"]

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Arial", "font.size": 7, "axes.titlesize": 7.5, "axes.labelsize": 7,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5, "axes.edgecolor": "#888", "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "axes.grid": True, "grid.color": "#E6E6E6", "grid.linewidth": 0.5, "axes.axisbelow": True,
})


def _svg(fig) -> str:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    s = buf.getvalue()
    i = s.find("<svg")
    return s[i:]


def _fmt(unit: str | None):
    if unit == "%":
        return FuncFormatter(lambda v, _: f"{v * 100:.0f}%")
    if unit == "x":
        return FuncFormatter(lambda v, _: f"{v:.0f}x")
    return FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " "))


def _lab(v, unit):
    if v is None:
        return ""
    if unit == "%":
        return f"{v * 100:.1f}%" if abs(v) < 0.1 else f"{v * 100:.0f}%"
    if unit == "x":
        return f"{v:.1f}x"
    if unit == "nok2":
        return f"{v:.2f}"
    return f"{v:,.0f}".replace(",", " ") if abs(v) >= 10 else f"{v:.1f}"


def bars(x, series, unit=None, stacked=False, labels=True, size=(5.2, 2.2), ylim=None, legend=True, colors=None, hline=None):
    """Grouped or stacked bars. series = [(label, values), ...]."""
    fig, ax = plt.subplots(figsize=size)
    n = len(series)
    idx = list(range(len(x)))
    colors = colors or PALETTE
    if stacked:
        pos_base = [0.0] * len(x)
        neg_base = [0.0] * len(x)
        for k, (lab, vals) in enumerate(series):
            bottoms = [pos_base[i] if (v or 0) >= 0 else neg_base[i] for i, v in enumerate(vals)]
            ax.bar(idx, [v or 0 for v in vals], 0.62, bottom=bottoms, label=lab, color=colors[k % len(colors)], linewidth=0)
            for i, v in enumerate(vals):
                if v is None:
                    continue
                if v >= 0:
                    pos_base[i] += v
                else:
                    neg_base[i] += v
        if labels:
            for i in idx:
                ax.text(i, pos_base[i], _lab(pos_base[i] + neg_base[i], unit), ha="center", va="bottom", fontsize=6)
    else:
        w = 0.78 / n
        for k, (lab, vals) in enumerate(series):
            xs = [i - 0.39 + w * (k + 0.5) for i in idx]
            ax.bar(xs, [v if v is not None else 0 for v in vals], w, label=lab, color=colors[k % len(colors)], linewidth=0)
            if labels:
                for xx, v in zip(xs, vals):
                    if v is not None:
                        ax.text(xx, v, _lab(v, unit), ha="center", va="bottom" if v >= 0 else "top", fontsize=5.8)
    ax.set_xticks(idx)
    ax.set_xticklabels([str(v) for v in x])
    ax.yaxis.set_major_formatter(_fmt(unit))
    ax.grid(axis="x", visible=False)
    if ylim:
        ax.set_ylim(*ylim)
    if hline is not None:
        ax.axhline(hline[0], color=RED, linewidth=0.8, linestyle="--")
        ax.text(idx[-1] + 0.45, hline[0], hline[1], color=RED, fontsize=6, va="center", ha="right")
    if legend and (n > 1 or stacked):
        ax.legend(frameon=False, ncol=min(n, 4), loc="upper left", bbox_to_anchor=(0, 1.14))
    return _svg(fig)


def hbars(labels, values, unit=None, size=(5.2, 2.4), highlight=None, sort=True):
    """Sorted horizontal bars (price screens, rankings). `highlight` = label to colour differently."""
    pairs = list(zip(labels, values))
    if sort:
        pairs.sort(key=lambda t: (t[1] is None, -(t[1] or 0)))
    pairs = pairs[::-1]
    fig, ax = plt.subplots(figsize=size)
    ys = list(range(len(pairs)))
    cols = [NAVY if (highlight and highlight.lower() in str(l_).lower()) else LBLUE for l_, _ in pairs]
    ax.barh(ys, [v or 0 for _, v in pairs], 0.62, color=cols, linewidth=0)
    for y, (_, v) in zip(ys, pairs):
        if v is not None:
            ax.text(v, y, " " + _lab(v, unit), va="center", fontsize=6)
    ax.set_yticks(ys)
    ax.set_yticklabels([str(l_) for l_, _ in pairs])
    ax.xaxis.set_major_formatter(_fmt(unit))
    ax.grid(axis="y", visible=False)
    return _svg(fig)


def line(x, series, unit=None, size=(5.2, 2.2), avg=None, markers=False, labels_last=True, colors=None, ylim=None):
    """Lines. series = [(label, values)]; avg = (value, label) draws a horizontal average line."""
    fig, ax = plt.subplots(figsize=size)
    colors = colors or PALETTE
    for k, (lab, vals) in enumerate(series):
        ax.plot(x, vals, label=lab, color=colors[k % len(colors)], linewidth=1.3, marker="o" if markers else None, markersize=2.5)
        if labels_last:
            last = [(xx, v) for xx, v in zip(x, vals) if v is not None]
            if last:
                ax.text(last[-1][0], last[-1][1], " " + _lab(last[-1][1], unit), fontsize=6, va="center", color=colors[k % len(colors)])
    if avg is not None:
        ax.axhline(avg[0], color=GREY, linewidth=0.8, linestyle="--")
        ax.text(x[0], avg[0], avg[1], fontsize=6, color=GREY, va="bottom")
    ax.yaxis.set_major_formatter(_fmt(unit))
    if ylim:
        ax.set_ylim(*ylim)
    if len(series) > 1:
        ax.legend(frameon=False, ncol=min(len(series), 4), loc="upper left", bbox_to_anchor=(0, 1.14))
    _dates(ax, list(x))
    return _svg(fig)


def waterfall(labels, values, unit=None, size=(5.2, 2.3), totals=(0,), colors=None):
    """Bridge chart. `values[i]` is a delta except for indices in `totals`, which are absolute levels."""
    fig, ax = plt.subplots(figsize=size)
    level = 0.0
    bottoms, heights, cols = [], [], []
    for i, v in enumerate(values):
        v = v or 0
        if i in totals:
            bottoms.append(0)
            heights.append(v)
            cols.append(NAVY)
            level = v
        else:
            bottoms.append(level if v >= 0 else level + v)
            heights.append(abs(v))
            cols.append(GREEN if v >= 0 else RED)
            level += v
    xs = list(range(len(labels)))
    ax.bar(xs, heights, 0.62, bottom=bottoms, color=cols, linewidth=0)
    # connectors
    run = 0.0
    for i, v in enumerate(values):
        v = v or 0
        run = v if i in totals else run + v
        if i < len(values) - 1:
            ax.plot([i + 0.31, i + 0.69], [run, run], color="#999", linewidth=0.5)
    for i, (b, h, v) in enumerate(zip(bottoms, heights, values)):
        v = v or 0
        txt = _lab(v, unit) if i in totals else (("+" if v > 0 else "") + _lab(v, unit))
        ax.text(i, b + h, txt, ha="center", va="bottom", fontsize=6)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=6)
    ax.yaxis.set_major_formatter(_fmt(unit))
    ax.grid(axis="x", visible=False)
    lo = min(min(bottoms), 0)
    hi = max(b + h for b, h in zip(bottoms, heights))
    ax.set_ylim(lo - (hi - lo) * 0.05, hi + (hi - lo) * 0.12)
    return _svg(fig)


def price_fan(dates, prices, index=None, index_label="OSEBX (rebased)", horizon_date=None, points=None, size=(5.2, 2.5),
              current_label="Price"):
    """Share price with the index rebased, and a fan from the last price to bear/target/bull values at the horizon.

    points = [(label, value, colour)] drawn at horizon_date.
    """
    fig, ax = plt.subplots(figsize=size)
    ax.plot(dates, prices, color=NAVY, linewidth=1.2, label=current_label)
    if index is not None:
        ax.plot(dates, index, color=LBLUE, linewidth=1.0, label=index_label)
    if points and horizon_date is not None:
        x0, y0 = dates[-1], prices[-1]
        vals = [v for _, v, _ in points]
        ax.fill([x0, horizon_date, horizon_date], [y0, min(vals), max(vals)], color=PALEBLUE, alpha=0.7, linewidth=0)
        for lab, v, c in points:
            ax.plot([x0, horizon_date], [y0, v], color=c, linewidth=0.8, linestyle="--")
            ax.plot([horizon_date], [v], marker="o", color=c, markersize=3)
            ax.text(horizon_date, v, "  " + lab, fontsize=6, va="center", color=c)
        ax.text(x0, y0, f"  {y0:.1f}", fontsize=6, va="bottom", color=NAVY)
        ax.set_xlim(dates[0], horizon_date + (horizon_date - dates[0]) * 0.22)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.legend(frameon=False, ncol=2, loc="upper left", bbox_to_anchor=(0, 1.14))
    _dates(ax, list(dates))
    return _svg(fig)


def range_bars(rows, current, target, unit="NOK", size=(5.2, 3.0), xlabel="Value per share (NOK)"):
    """Valuation summary: one horizontal range per method (low–high with the mid marked), lines for price and target.

    rows = [(label, low, mid, high)]
    """
    fig, ax = plt.subplots(figsize=size)
    ys = list(range(len(rows)))[::-1]
    for y, (lab, lo, mid, hi) in zip(ys, rows):
        if lo is None or hi is None:
            ax.text(current, y, "not available", fontsize=6, va="center", color=GREY, style="italic")
            continue
        ax.barh(y, hi - lo, 0.5, left=lo, color=PALEBLUE, linewidth=0)
        if mid is not None:
            ax.plot([mid], [y], marker="^", color=NAVY, markersize=4)
        ax.text(lo, y, f"{lo:.0f} ", fontsize=5.8, va="center", ha="right")
        ax.text(hi, y, f" {hi:.0f}", fontsize=5.8, va="center", ha="left")
    ax.axvline(current, color=RED, linewidth=0.9)
    ax.text(current, len(rows) - 0.4, f" price {current:.1f}", color=RED, fontsize=6, va="bottom")
    if target is not None:
        ax.axvline(target, color=GREEN, linewidth=0.9, linestyle="--")
        ax.text(target, len(rows) - 0.4, f" TP {target:.0f}", color=GREEN, fontsize=6, va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=6.3)
    ax.set_xlabel(xlabel)
    ax.grid(axis="y", visible=False)
    ax.set_ylim(-0.6, len(rows) + 0.3)
    return _svg(fig)


def heat_table(rowlab, collab, grid, center=None, size=(3.6, 1.9), fmt="{:.0f}", title_r="", title_c=""):
    """A small coloured sensitivity grid (values vs two drivers)."""
    fig, ax = plt.subplots(figsize=size)
    import numpy as np
    arr = np.array([[v if v is not None else np.nan for v in r] for r in grid], dtype=float)
    ax.imshow(arr, cmap="Blues", aspect="auto", alpha=0.85)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            v = arr[i, j]
            if np.isnan(v):
                continue
            bold = center is not None and (i, j) == center
            ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=6.3, fontweight="bold" if bold else "normal",
                    color="#fff" if v > np.nanmean(arr) * 1.15 else "#000")
    ax.set_xticks(range(len(collab)))
    ax.set_xticklabels(collab, fontsize=6)
    ax.set_yticks(range(len(rowlab)))
    ax.set_yticklabels(rowlab, fontsize=6)
    ax.set_xlabel(title_c, fontsize=6.5)
    ax.set_ylabel(title_r, fontsize=6.5)
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    return _svg(fig)


def pie(labels, values, size=(2.4, 1.9)):
    fig, ax = plt.subplots(figsize=size)
    vals = [v or 0 for v in values]
    ax.pie(vals, labels=None, colors=PALETTE[: len(vals)], startangle=90, counterclock=False,
           wedgeprops=dict(linewidth=0.8, edgecolor="#fff"), autopct=lambda p: f"{p:.0f}%" if p >= 5 else "", pctdistance=0.72,
           textprops=dict(fontsize=6, color="#fff"))
    ax.legend(labels, frameon=False, loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=6)
    ax.grid(False)
    return _svg(fig)
