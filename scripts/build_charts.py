"""Построение графиков KPI для Wiki «ЛогиХаб».

Использует выгрузку заказов из репозитория дашборда:
    python scripts/build_charts.py ../logihub-dashboard/data/logistics_orders.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "charts"
RELEASES = [("2024-01-01", "v1.0"), ("2025-02-01", "v1.5"), ("2026-02-01", "v2.0")]
INDIGO, AMBER, GREY = "#3f51b5", "#ffb300", "#9e9e9e"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False})


def main(csv_path: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path, parse_dates=["order_date"])
    done = df[df["status"] != "Отменён"].copy()
    done["month"] = done["order_date"].dt.to_period("M").dt.to_timestamp()

    # 1. OTIF по месяцам с точками релизов
    monthly = done.groupby("month")["otif"].mean() * 100
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    ax.plot(monthly.index, monthly.values, color=INDIGO, lw=2.2, marker="o", ms=3.5, label="OTIF, %")
    for start, name in RELEASES:
        x = pd.Timestamp(start)
        level = done[done["release"] == name]["otif"].mean() * 100
        ax.axvline(x, color=AMBER, ls="--", lw=1.4)
        ax.annotate(f"{name}\n{level:.0f} %", xy=(x, 96), xytext=(6, 0), textcoords="offset points",
                    color="#5d4037", fontsize=10, va="top", fontweight="bold")
    ax.axhline(90, color=GREY, ls=":", lw=1.2)
    ax.text(monthly.index[2], 90.6, "цель 2026 – 90 %", color="#616161", fontsize=9)
    ax.set_ylim(55, 98)
    ax.set_ylabel("OTIF, %")
    ax.set_title("OTIF по месяцам и релизы продукта ЛогиХаб", loc="left", fontweight="bold")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y"))
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "otif_by_month.png")
    plt.close(fig)

    # 2. Выручка и затраты по месяцам
    fin = done.groupby("month")[["revenue", "total_cost", "profit"]].sum() / 1e6
    fig, ax = plt.subplots(figsize=(10, 4.4), dpi=150)
    ax.plot(fin.index, fin["revenue"], color=INDIGO, lw=2.2, label="Выручка")
    ax.plot(fin.index, fin["total_cost"], color="#e53935", lw=2.2, label="Затраты")
    ax.fill_between(fin.index, fin["total_cost"], fin["revenue"], color=INDIGO, alpha=0.08, label="Прибыль")
    ax.set_ylabel("млн руб.")
    ax.set_title("Выручка и затраты по месяцам", loc="left", fontweight="bold")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y"))
    ax.legend(frameon=False, ncol=3)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "revenue_cost.png")
    plt.close(fig)

    # 3. Структура затрат
    costs = done[["cost_fuel", "cost_driver", "cost_warehouse", "cost_tolls", "cost_other"]].sum()
    labels = ["Топливо", "Оплата водителей", "Складские операции", "Платные дороги", "Прочие и штрафы"]
    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=150)
    ax.pie(costs.values, labels=labels, autopct="%1.1f %%", startangle=90, pctdistance=0.78,
           colors=[INDIGO, "#7986cb", AMBER, "#ffe082", GREY],
           wedgeprops={"width": 0.45, "edgecolor": "white"})
    ax.set_title("Структура затрат, 2024–2026", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "cost_structure.png")
    plt.close(fig)

    v2 = done[done["release"] == "v2.0"]
    print("on_time", round(v2["on_time"].mean() * 100), "in_full", round(v2["in_full"].mean() * 100),
          "cancel", round((df["status"] == "Отменён").mean() * 100, 1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../logihub-dashboard/data/logistics_orders.csv")
