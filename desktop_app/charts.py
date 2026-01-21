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


def build_figure(records: Iterable[StudentRecord]) -> Figure:
    df = _to_dataframe(records)

    fig = Figure(figsize=(9, 6), dpi=100, tight_layout=True)
    axs = fig.subplots(2, 2)

    if df.empty:
        for ax in axs.flat:
            ax.set_visible(False)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "Chưa có dữ liệu", ha="center", va="center", fontsize=12)
        ax.set_axis_off()
        return fig

    # 1) Histogram of scores
    ax = axs[0, 0]
    for col, color in zip(SCORE_COLS, ["#3b82f6", "#f59e0b", "#10b981"]):
        if col in df:
            sns.histplot(df[col], ax=ax, kde=True, color=color, label=col, alpha=0.4)
    ax.set_title("Phân phối điểm")
    ax.set_xlabel("Điểm")
    ax.set_ylabel("Số lượng")
    ax.legend(loc="upper right")

    # 2) Boxplot by subject
    ax = axs[0, 1]
    melt = df.melt(value_vars=SCORE_COLS, var_name="Môn", value_name="Điểm")
    sns.boxplot(data=melt, x="Môn", y="Điểm", ax=ax)
    ax.set_title("Boxplot theo môn")
    ax.set_xlabel("Môn")
    ax.set_ylabel("Điểm")

    # 3) Average score by subject
    ax = axs[1, 0]
    means = df[SCORE_COLS].mean().reset_index()
    means.columns = ["Môn", "Điểm TB"]
    sns.barplot(data=means, x="Môn", y="Điểm TB", ax=ax, palette="Blues_d")
    ax.set_title("Điểm trung bình theo môn")
    ax.set_xlabel("Môn")
    ax.set_ylabel("Điểm TB")

    # 4) Top hometown by English score
    ax = axs[1, 1]
    if "hometown" in df.columns and "english_score" in df.columns:
        by_home = (
            df.groupby("hometown", dropna=False)["english_score"]
            .mean()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )
        sns.barplot(data=by_home, x="english_score", y="hometown", ax=ax, palette="Greens_d")
        ax.set_title("Top quê quán theo điểm Anh")
        ax.set_xlabel("Điểm Anh TB")
        ax.set_ylabel("Quê quán")
    else:
        ax.set_visible(False)

    return fig
