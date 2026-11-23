"""
Gera gráficos executivos estáticos em alta resolução (PNG) para o README e portfólio:
1. assets/evolucao_receita_margem.png
2. assets/absenteismo_vs_margem.png
"""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "fato_operacoes.csv"
CAL_PATH = PROJECT_ROOT / "data" / "dim_calendario.csv"
ASSETS_DIR = PROJECT_ROOT / "assets"


def gerar_graficos() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)
    cal = pd.read_csv(CAL_PATH)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#CBD5E1",
        "axes.linewidth": 0.8,
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
    })

    # =========================================================================
    # GRÁFICO 1: Evolução Mensal — Receita Líquida (R$ M) vs Margem Operacional %
    # =========================================================================
    mensal = (
        df.groupby("ano_mes", as_index=False)
        .agg(
            receita_liquida=("receita_liquida", "sum"),
            margem_operacional=("margem_operacional", "sum"),
            custo_he=("custo_hora_extra_cobertura", "sum"),
            glosa=("glosa_sla", "sum"),
        )
        .merge(cal[["ano_mes", "mes_abrev", "mes_num"]], on="ano_mes", how="left")
        .sort_values("mes_num")
    )
    mensal["margem_pct"] = (mensal["margem_operacional"] / mensal["receita_liquida"]) * 100.0
    mensal["rec_m"] = mensal["receita_liquida"] / 1e6

    fig, ax1 = plt.subplots(figsize=(11.5, 5.6), dpi=180)
    x = range(len(mensal))

    # Destacar S2 (Jul-Dez) com fundo suave
    ax1.axvspan(5.5, 11.5, color="#FEF2F2", alpha=0.65, zorder=0)
    ax1.text(
        8.5,
        mensal["rec_m"].max() * 1.13,
        "2º Semestre: Receita cresce, mas margem cai para 8,0%",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEE2E2", edgecolor="#FCA5A5", lw=0.8),
    )

    bars = ax1.bar(
        x,
        mensal["rec_m"],
        width=0.56,
        color="#1E3A5F",
        alpha=0.86,
        label="Receita Líquida (R$ Milhões)",
        zorder=2,
    )
    ax1.set_ylim(0, mensal["rec_m"].max() * 1.48)
    ax1.set_ylabel("Receita Líquida (R$ Milhões)", fontsize=10, fontweight="bold", color="#1E3A5F")
    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter("R$ %.1fM"))
    ax1.grid(axis="y", linestyle="--", alpha=0.35, color="#94A3B8", zorder=1)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(mensal["mes_abrev"], fontsize=9.5, color="#334155")
    ax1.spines["top"].set_visible(False)

    # Ajustar posição da caixa de destaque no S2
    for txt in list(ax1.texts):
        txt.remove()
    ax1.text(
        8.5,
        mensal["rec_m"].max() * 1.32,
        "2º Semestre: Receita cresce (+5,4%), mas margem cai para 8,0%",
        ha="center",
        va="center",
        fontsize=9.3,
        fontweight="bold",
        color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.32", facecolor="#FEE2E2", edgecolor="#FCA5A5", lw=0.9),
    )

    for bar, val in zip(bars, mensal["rec_m"]):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.08,
            f"{val:.2f}M",
            ha="center",
            va="bottom",
            fontsize=7.8,
            color="#334155",
            fontweight="bold",
        )

    ax2 = ax1.twinx()
    ax2.plot(
        x,
        mensal["margem_pct"],
        color="#DC2626",
        marker="o",
        linewidth=2.6,
        markersize=7,
        markerfacecolor="#FFFFFF",
        markeredgewidth=2.2,
        label="Margem Operacional (%)",
        zorder=4,
    )
    ax2.set_ylim(0, 21)
    ax2.set_ylabel("Margem Operacional (%)", fontsize=10, fontweight="bold", color="#DC2626")
    ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.0f%%"))
    ax2.spines["top"].set_visible(False)

    for xi, mp in zip(x, mensal["margem_pct"]):
        offset = 1.45 if xi < 6 else -1.65
        ax2.text(
            xi,
            mp + offset,
            f"{mp:.1f}%",
            ha="center",
            va="center",
            fontsize=8.2,
            fontweight="bold",
            color="#B91C1C",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#FFFFFF", edgecolor="#FCA5A5", alpha=0.94, lw=0.7),
            zorder=5,
        )

    fig.suptitle(
        "Faturamento Cresceu no Ano, Mas a Margem Foi Corroída no 2º Semestre",
        fontsize=13.5,
        fontweight="bold",
        color="#0F172A",
        x=0.06,
        ha="left",
        y=0.96,
    )
    ax1.set_title(
        "Evolução mensal de Receita Líquida (R$ M) vs. Margem Operacional (%) — 24 contratos (Dados Simulados 2025)",
        fontsize=9.8,
        color="#475569",
        loc="left",
        pad=14,
    )

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0", fontsize=9)

    fig.tight_layout(rect=[0, 0.02, 1, 0.92])
    out1 = ASSETS_DIR / "evolucao_receita_margem.png"
    fig.savefig(out1, dpi=180)
    plt.close(fig)

    # =========================================================================
    # GRÁFICO 2: Absenteísmo % vs Margem Operacional % por Contrato (Quadrantes)
    # =========================================================================
    df["postos_dia"] = df["headcount_previsto"] * df["dias_uteis"]
    ctr = (
        df.groupby(["id_contrato", "nome_contrato", "linha_servico"], as_index=False)
        .agg(
            receita_liquida=("receita_liquida", "sum"),
            margem_operacional=("margem_operacional", "sum"),
            faltas=("faltas_colaboradores", "sum"),
            postos_dia=("postos_dia", "sum"),
            he=("custo_hora_extra_cobertura", "sum"),
            glosa=("glosa_sla", "sum"),
        )
    )
    ctr["margem_pct"] = (ctr["margem_operacional"] / ctr["receita_liquida"]) * 100.0
    ctr["abs_pct"] = (ctr["faltas"] / ctr["postos_dia"]) * 100.0

    def classificar(row):
        if row["margem_pct"] < 8.0 or row["abs_pct"] > 6.0:
            return "Crítico"
        if row["margem_pct"] < 12.0 or row["abs_pct"] > 4.0:
            return "Atenção"
        return "Saudável"

    ctr["status"] = ctr.apply(classificar, axis=1)

    fig, ax = plt.subplots(figsize=(12.0, 6.2), dpi=180)

    # Zona crítica exata (Abs >= 6% e Margem <= 8%)
    ax.fill_between([6.0, 10.2], -3.5, 8.0, color="#FEE2E2", alpha=0.52, zorder=0)
    ax.axvline(4.0, color="#94A3B8", linestyle="--", linewidth=1.0, zorder=1)
    ax.axvline(6.0, color="#DC2626", linestyle=":", linewidth=1.2, zorder=1)
    ax.axhline(12.0, color="#94A3B8", linestyle="--", linewidth=1.0, zorder=1)
    ax.axhline(8.0, color="#DC2626", linestyle=":", linewidth=1.2, zorder=1)

    palette = {
        "Crítico": "#DC2626",
        "Atenção": "#D97706",
        "Saudável": "#0D9488",
    }
    for st in ["Saudável", "Atenção", "Crítico"]:
        sub = ctr[ctr["status"] == st]
        sizes = (sub["receita_liquida"] / 1e6) * 140 + 45
        ax.scatter(
            sub["abs_pct"],
            sub["margem_pct"],
            s=sizes,
            color=palette[st],
            alpha=0.86,
            edgecolors="#FFFFFF",
            linewidth=1.5,
            label=f"{st} ({len(sub)} contratos)",
            zorder=3,
        )

    # Posicionamento explícito (x_text, y_text) sem sobreposição
    label_coords = {
        "CTR-019": (6.25, 6.1),   # Mall Aldeota
        "CTR-011": (6.20, 1.9),   # Hospital Timon
        "CTR-006": (6.20, -1.7),  # Distrito Industrial THE
        "CTR-001": (7.38, -2.55), # Hospital Regional Sul
        "CTR-015": (8.55, 5.1),   # Terminal Portuário
        "CTR-002": (8.78, -2.55), # Shopping Poty Center
        "CTR-018": (3.70, 13.7),  # Hospital São Marcos
        "CTR-009": (5.45, 14.3),  # Rede Supermercado Norte
        "CTR-010": (4.55, 8.9),   # Polo Logístico Timon
    }
    short_names = {
        "CTR-001": "CTR-001 Hosp. Reg. Sul",
        "CTR-002": "CTR-002 Shop. Poty",
        "CTR-006": "CTR-006 Dist. Ind. THE",
        "CTR-009": "CTR-009 Supermercado Norte",
        "CTR-010": "CTR-010 Polo Timon",
        "CTR-011": "CTR-011 Hosp. Timon",
        "CTR-015": "CTR-015 Term. Portuário",
        "CTR-018": "CTR-018 Hosp. São Marcos",
        "CTR-019": "CTR-019 Mall Aldeota",
    }
    for _, row in ctr[ctr["status"].isin(["Crítico", "Atenção"])].iterrows():
        cid = row["id_contrato"]
        tx, ty = label_coords.get(cid, (row["abs_pct"] + 0.2, row["margem_pct"] + 1.0))
        is_crit = row["status"] == "Crítico"
        ax.annotate(
            short_names.get(cid, cid),
            xy=(row["abs_pct"], row["margem_pct"]),
            xytext=(tx, ty),
            fontsize=7.9,
            fontweight="bold" if is_crit else "semibold",
            color="#7F1D1D" if is_crit else "#78350F",
            bbox=dict(
                boxstyle="round,pad=0.22",
                facecolor="#FFFFFF",
                edgecolor="#FCA5A5" if is_crit else "#FCD34D",
                alpha=0.92,
                lw=0.7,
            ),
            arrowprops=dict(arrowstyle="-", color="#64748B", lw=0.8),
            zorder=5,
        )

    ax.text(
        8.25,
        10.7,
        "ZONA CRÍTICA (Abs > 6% | Margem < 8%)\n6 contratos concentram 76% da Hora Extra\ne 85% das Glosas de SLA",
        ha="center",
        va="center",
        fontsize=8.7,
        fontweight="bold",
        color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor="#F87171", lw=1.0),
        zorder=5,
    )
    ax.text(2.05, 22.0, "Benchmark Saudável (Abs ≤ 4% | Margem ≥ 12%)", fontsize=8.9, fontweight="bold", color="#0F766E")

    ax.set_xlim(1.8, 10.1)
    ax.set_ylim(-3.5, 23.8)
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f%%"))
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.0f%%"))
    ax.set_xlabel("Taxa Média Anual de Absenteísmo (%)", fontsize=10, fontweight="bold", color="#1E293B")
    ax.set_ylabel("Margem Operacional Anual (%)", fontsize=10, fontweight="bold", color="#1E293B")
    ax.grid(True, linestyle="--", alpha=0.3, color="#94A3B8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.suptitle(
        "Quanto Maior o Absenteísmo, Menor a Margem: O Efeito Cascata nos Contratos",
        fontsize=13.5,
        fontweight="bold",
        color="#0F172A",
        x=0.06,
        ha="left",
        y=0.96,
    )
    ax.set_title(
        "Correlação entre Absenteísmo (%) e Margem Operacional (%) por contrato (tamanho da bolha = Receita Líquida)",
        fontsize=9.8,
        color="#475569",
        loc="left",
        pad=14,
    )
    ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0", fontsize=9)

    fig.tight_layout(rect=[0, 0.02, 1, 0.92])
    out2 = ASSETS_DIR / "absenteismo_vs_margem.png"
    fig.savefig(out2, dpi=180)
    plt.close(fig)
    print(f"Gráficos gerados: {out1.name}, {out2.name}")


if __name__ == "__main__":
    gerar_graficos()
