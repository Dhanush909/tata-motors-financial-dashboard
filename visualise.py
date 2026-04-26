"""
visualise.py — Chart generation for Tata Motors Dashboard
Author: Bonthu Raj Dhanush
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

COLORS = {
    "blue":       "#1F3864",
    "light_blue": "#2E75B6",
    "green":      "#375623",
    "green_bg":   "#70AD47",
    "red":        "#C00000",
    "orange":     "#E36C09",
    "grey":       "#808080",
    "profit":     "#70AD47",
    "loss":       "#C00000",
}

plt.rcParams.update({
    "font.family":    "Arial",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "figure.facecolor":   "white",
    "axes.facecolor":     "white",
    "axes.titlesize":     13,
    "axes.titleweight":   "bold",
    "axes.labelsize":     10,
    "xtick.labelsize":    9,
    "ytick.labelsize":    9,
})


def cr_formatter(x, _):
    return f"₹{x/1000:.0f}K Cr" if abs(x) >= 1000 else f"₹{x:.0f} Cr"


def load_data():
    csv = os.path.join(os.path.dirname(__file__), "data", "tata_motors_pl.csv")
    return pd.read_csv(csv)


def chart1_revenue_trend(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(df["year"], df["revenue"] / 1000,
                  color=[COLORS["light_blue"]] * len(df), width=0.6, zorder=2)
    ax.plot(df["year"], df["revenue"] / 1000,
            color=COLORS["blue"], marker="o", linewidth=2, zorder=3)
    ax.set_title("Tata Motors — Revenue Trend (FY2016–FY2025)", pad=15)
    ax.set_ylabel("₹ Thousand Crores")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}K Cr"))
    ax.grid(axis="y", alpha=0.3, zorder=1)
    ax.set_xlabel("")
    for bar, val in zip(bars, df["revenue"] / 1000):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f"₹{val:.0f}K", ha="center", va="bottom", fontsize=8, fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "01_revenue_trend.png"), dpi=150)
    plt.close()
    print("Chart 1 saved: Revenue Trend")


def chart2_pat_turnaround(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = [COLORS["profit"] if v >= 0 else COLORS["loss"] for v in df["pat"]]
    bars = ax.bar(df["year"], df["pat"] / 100, color=colors, width=0.6, zorder=2)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("Tata Motors — PAT Turnaround: Loss to Profit (FY2016–FY2025)", pad=15)
    ax.set_ylabel("₹ Hundreds of Crores")
    ax.grid(axis="y", alpha=0.3, zorder=1)
    for bar, val in zip(bars, df["pat"] / 100):
        offset = 2 if val >= 0 else -8
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + offset,
                f"₹{val:.0f}H", ha="center", va="bottom", fontsize=7.5, fontweight="bold")
    ax.annotate("Peak Loss\n₹34,153 Cr", xy=("FY2022", -341.53),
                xytext=("FY2020", -280),
                arrowprops=dict(arrowstyle="->", color=COLORS["red"]),
                fontsize=8.5, color=COLORS["red"], fontweight="bold")
    ax.annotate("Turnaround\n₹27,391 Cr", xy=("FY2025", 273.91),
                xytext=("FY2024", 220),
                arrowprops=dict(arrowstyle="->", color=COLORS["green"]),
                fontsize=8.5, color=COLORS["green"], fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "02_pat_turnaround.png"), dpi=150)
    plt.close()
    print("Chart 2 saved: PAT Turnaround")


def chart3_margin_trend(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["year"], df["opm_pct"], color=COLORS["blue"],
            marker="o", linewidth=2.5, label="EBITDA Margin %", zorder=3)
    ax.plot(df["year"], df["pat_margin_pct"], color=COLORS["orange"],
            marker="s", linewidth=2.5, linestyle="--", label="PAT Margin %", zorder=3)
    ax.axhline(0, color="black", linewidth=0.8, linestyle=":")
    ax.fill_between(df["year"], df["opm_pct"], 0,
                    where=[v >= 0 for v in df["opm_pct"]],
                    alpha=0.1, color=COLORS["green_bg"])
    ax.fill_between(df["year"], df["opm_pct"], 0,
                    where=[v < 0 for v in df["opm_pct"]],
                    alpha=0.1, color=COLORS["red"])
    ax.set_title("EBITDA & PAT Margin Trend (FY2016–FY2025)", pad=15)
    ax.set_ylabel("Margin %")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="y", alpha=0.3, zorder=1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "03_margin_trend.png"), dpi=150)
    plt.close()
    print("Chart 3 saved: Margin Trend")


def chart4_cost_structure(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    width = 0.35
    x = range(len(df))
    ax.bar([i - width/2 for i in x], df["revenue"] / 1000,
           width=width, label="Revenue", color=COLORS["light_blue"], zorder=2)
    ax.bar([i + width/2 for i in x], df["expenses"] / 1000,
           width=width, label="Total Expenses", color=COLORS["orange"], zorder=2)
    ax.set_title("Revenue vs Total Expenses (FY2016–FY2025)", pad=15)
    ax.set_ylabel("₹ Thousand Crores")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["year"], rotation=45)
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3, zorder=1)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "04_revenue_vs_expenses.png"), dpi=150)
    plt.close()
    print("Chart 4 saved: Revenue vs Expenses")


def chart5_eps_recovery(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = [COLORS["profit"] if v >= 0 else COLORS["loss"] for v in df["eps"]]
    ax.bar(df["year"], df["eps"], color=colors, width=0.6, zorder=2)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("EPS Recovery — From -₹99.45 to +₹71.64 (FY2016–FY2025)", pad=15)
    ax.set_ylabel("EPS (₹ per share)")
    ax.grid(axis="y", alpha=0.3, zorder=1)
    for i, (yr, eps) in enumerate(zip(df["year"], df["eps"])):
        offset = 1.5 if eps >= 0 else -5
        ax.text(i, eps + offset, f"₹{eps:.1f}", ha="center",
                fontsize=7.5, fontweight="bold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "05_eps_recovery.png"), dpi=150)
    plt.close()
    print("Chart 5 saved: EPS Recovery")


def generate_all_charts():
    df = load_data()
    chart1_revenue_trend(df)
    chart2_pat_turnaround(df)
    chart3_margin_trend(df)
    chart4_cost_structure(df)
    chart5_eps_recovery(df)
    print(f"\nAll charts saved to: {CHARTS_DIR}")


if __name__ == "__main__":
    generate_all_charts()
