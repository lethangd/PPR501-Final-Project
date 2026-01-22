"""Chart utilities for the desktop app."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from .xml_parser import StudentRecord

SCORE_COLS = ["math_score", "literature_score", "english_score"]

sns.set_theme(style="whitegrid")


def _to_dataframe(records: Iterable[StudentRecord]) -> pd.DataFrame:
    data = [asdict(r) for r in records]
    df = pd.DataFrame(data)
    for col in SCORE_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def build_figures(records: Iterable[StudentRecord]) -> list[Figure]:
    df = _to_dataframe(records)

    figs: list[Figure] = []

    if df.empty:
        fig = Figure(figsize=(10, 6), dpi=100, tight_layout=True)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "Chưa có dữ liệu", ha="center", va="center", fontsize=12)
        ax.set_axis_off()
        return [fig]

    # 1) Histogram of scores
    fig = Figure(figsize=(10, 6), dpi=100, tight_layout=True)
    axs = fig.subplots(2, 1)

    ax = axs[0]
    for col, color in zip(SCORE_COLS, ["#3b82f6", "#f59e0b", "#10b981"]):
        if col in df:
            sns.histplot(df[col], ax=ax, kde=True, color=color, label=col, alpha=0.4)
    ax.set_title("Phân phối điểm")
    ax.set_xlabel("Điểm")
    ax.set_ylabel("Số lượng")
    ax.legend(loc="upper right")

    # 2) Boxplot by subject
    ax = axs[1]
    melt = df.melt(value_vars=SCORE_COLS, var_name="Môn", value_name="Điểm")
    sns.boxplot(data=melt, x="Môn", y="Điểm", ax=ax)
    ax.set_title("Boxplot theo môn")
    ax.set_xlabel("Môn")
    ax.set_ylabel("Điểm")

    figs.append(fig)

    fig = Figure(figsize=(10, 6), dpi=100, tight_layout=True)
    axs = fig.subplots(2, 1)

    # 3) Average score by subject
    ax = axs[0]
    means = df[SCORE_COLS].mean().reset_index()
    means.columns = ["Môn", "Điểm TB"]
    sns.barplot(data=means, x="Môn", y="Điểm TB", ax=ax, palette="Blues_d")
    ax.set_title("Điểm trung bình theo môn")
    ax.set_xlabel("Môn")
    ax.set_ylabel("Điểm TB")

    # 4) Top hometown by English score
    def plot_hometown(ax, score_col: str, title: str, palette: str) -> None:
        if "hometown" not in df.columns or score_col not in df.columns:
            ax.set_visible(False)
            return
        by_home = (
            df.groupby("hometown", dropna=False)[score_col]
            .mean()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )
        sns.barplot(data=by_home, x=score_col, y="hometown", ax=ax, palette=palette)
        ax.set_title(title)
        ax.set_xlabel("Điểm TB")
        ax.set_ylabel("Quê quán")

    plot_hometown(axs[1], "english_score", "Điểm Anh theo quê quán", "Greens_d")
    figs.append(fig)

    fig = Figure(figsize=(10, 6), dpi=100, tight_layout=True)
    axs = fig.subplots(2, 1)

    plot_hometown(axs[0], "math_score", "Điểm Toán theo quê quán", "Blues_d")
    plot_hometown(axs[1], "literature_score", "Điểm Văn theo quê quán", "Oranges_d")
    figs.append(fig)

    return figs
