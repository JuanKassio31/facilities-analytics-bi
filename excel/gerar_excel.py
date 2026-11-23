"""
Gera o workbook executivo em Excel (excel/Analise_Operacional_Facilities.xlsx)
a partir dos CSVs gerados por data/gerar_dados.py.

Utiliza fórmulas nativas do Excel (SUM, SUMIFS, AVERAGEIFS, IF, OR) para
demonstrar modelagem tabular e análise de negócios diretamente na planilha.
"""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EXCEL_DIR = PROJECT_ROOT / "excel"
OUTPUT_XLSX = EXCEL_DIR / "Analise_Operacional_Facilities.xlsx"

# Paleta executiva (Navy / Slate / Teal / Semáforo)
NAVY = "0F2744"
SLATE_BLUE = "1E3A5F"
TEAL = "0D9488"
LIGHT_BG = "F1F5F9"
ZEBRA_BG = "F8FAFC"
WHITE = "FFFFFF"
BORDER_COLOR = "CBD5E1"

CRIT_FILL = PatternFill("solid", fgColor="FEE2E2")
CRIT_FONT = Font(name="Calibri", size=10, bold=True, color="991B1B")
WARN_FILL = PatternFill("solid", fgColor="FEF3C7")
WARN_FONT = Font(name="Calibri", size=10, bold=True, color="92400E")
OK_FILL = PatternFill("solid", fgColor="DCFCE7")
OK_FONT = Font(name="Calibri", size=10, bold=True, color="166534")

HEADER_FILL = PatternFill("solid", fgColor=NAVY)
SUBHEADER_FILL = PatternFill("solid", fgColor=SLATE_BLUE)
CARD_FILL = PatternFill("solid", fgColor=LIGHT_BG)
ZEBRA_FILL = PatternFill("solid", fgColor=ZEBRA_BG)

TITLE_FONT = Font(name="Calibri", size=15, bold=True, color=WHITE)
SUBTITLE_FONT = Font(name="Calibri", size=10, italic=True, color="E2E8F0")
SECTION_FONT = Font(name="Calibri", size=12, bold=True, color=NAVY)
HEADER_FONT = Font(name="Calibri", size=10, bold=True, color=WHITE)
BODY_FONT = Font(name="Calibri", size=10, color="1E293B")
BOLD_FONT = Font(name="Calibri", size=10, bold=True, color="0F172A")
KPI_LABEL_FONT = Font(name="Calibri", size=9, bold=True, color="475569")
KPI_VAL_FONT = Font(name="Calibri", size=14, bold=True, color=NAVY)

THIN_SIDE = Side(border_style="thin", color=BORDER_COLOR)
MED_NAVY = Side(border_style="medium", color=NAVY)
GRID_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)
TOTAL_BORDER = Border(top=MED_NAVY, bottom=MED_NAVY, left=THIN_SIDE, right=THIN_SIDE)

FMT_BRL = 'R$ #,##0.00'
FMT_BRL_INT = 'R$ #,##0'
FMT_PCT = '0.0%'
FMT_INT = '#,##0'


def ler_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def auto_ajustar_colunas(ws, min_width: int = 10, max_width: int = 44) -> None:
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            if cell.row <= 2 and ws.title in ("Resumo_Executivo", "Diagnostico_Contratos"):
                continue
            val = cell.value
            if val is None:
                continue
            s = str(val)
            if s.startswith("="):
                s = "R$ 99.999.999,00"
            max_len = max(max_len, len(s))
        ws.column_dimensions[col_letter].width = max(min_width, min(max_width, max_len + 4))


def construir_excel() -> Path:
    EXCEL_DIR.mkdir(parents=True, exist_ok=True)
    fato = ler_csv(DATA_DIR / "fato_operacoes.csv")
    contratos = ler_csv(DATA_DIR / "dim_contratos.csv")
    calendario = ler_csv(DATA_DIR / "dim_calendario.csv")

    wb = Workbook()

    # =========================================================================
    # ABA 1: Resumo_Executivo (criada primeiro, populada após saber o range)
    # =========================================================================
    ws_resumo = wb.active
    ws_resumo.title = "Resumo_Executivo"
    ws_diag = wb.create_sheet("Diagnostico_Contratos")
    ws_base = wb.create_sheet("Base_Operacoes")
    ws_dim = wb.create_sheet("Dim_Contratos")

    for ws in (ws_resumo, ws_diag, ws_base, ws_dim):
        ws.views.sheetView[0].showGridLines = True

    # =========================================================================
    # ABA 3: Base_Operacoes (288 linhas + coluna auxiliar Postos_Dia)
    # =========================================================================
    base_cols = list(fato[0].keys()) + ["postos_dia"]
    int_cols = {"headcount_previsto", "dias_uteis", "faltas_colaboradores", "desligamentos"}
    pct_cols = {"taxa_absenteismo_pct", "taxa_turnover_pct", "sla_atingido_pct", "margem_pct"}
    brl_cols = {
        "receita_bruta",
        "glosa_sla",
        "receita_liquida",
        "custo_folha_base",
        "custo_hora_extra_cobertura",
        "custo_insumos",
        "custo_rescisao_admissao",
        "custo_total",
        "margem_operacional",
    }

    for col_idx, name in enumerate(base_cols, start=1):
        cell = ws_base.cell(row=1, column=col_idx, value=name)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = GRID_BORDER
    ws_base.row_dimensions[1].height = 26

    for r_idx, row in enumerate(fato, start=2):
        for c_idx, col_name in enumerate(base_cols, start=1):
            cell = ws_base.cell(row=r_idx, column=c_idx)
            if col_name == "postos_dia":
                cell.value = f"=J{r_idx}*K{r_idx}"
                cell.number_format = FMT_INT
            elif col_name in int_cols:
                cell.value = int(row[col_name])
                cell.number_format = FMT_INT
            elif col_name in pct_cols:
                cell.value = float(row[col_name])
                cell.number_format = FMT_PCT
            elif col_name in brl_cols:
                cell.value = float(row[col_name])
                cell.number_format = FMT_BRL
            else:
                cell.value = row[col_name]
            cell.font = BODY_FONT
            cell.border = GRID_BORDER
            if r_idx % 2 == 1:
                cell.fill = ZEBRA_FILL

    n_fato = len(fato) + 1  # 289
    ws_base.freeze_panes = "A2"
    ws_base.auto_filter.ref = f"A1:{get_column_letter(len(base_cols))}{n_fato}"
    auto_ajustar_colunas(ws_base, min_width=11, max_width=38)

    # Mapeamento de letras das colunas em Base_Operacoes:
    # A=id_registro, B=data, C=ano_mes, D=id_contrato, E=nome_contrato,
    # F=segmento, G=linha_servico, H=cidade, I=uf, J=headcount_previsto,
    # K=dias_uteis, L=faltas_colaboradores, M=taxa_absenteismo_pct,
    # N=desligamentos, O=taxa_turnover_pct, P=sla_atingido_pct,
    # Q=receita_bruta, R=glosa_sla, S=receita_liquida,
    # T=custo_folha_base, U=custo_hora_extra_cobertura, V=custo_insumos,
    # W=custo_rescisao_admissao, X=custo_total, Y=margem_operacional,
    # Z=margem_pct, AA=postos_dia

    # =========================================================================
    # ABA 4: Dim_Contratos
    # =========================================================================
    dim_cols = list(contratos[0].keys())
    for col_idx, name in enumerate(dim_cols, start=1):
        cell = ws_dim.cell(row=1, column=col_idx, value=name)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = GRID_BORDER
    ws_dim.row_dimensions[1].height = 24

    for r_idx, row in enumerate(contratos, start=2):
        for c_idx, col_name in enumerate(dim_cols, start=1):
            cell = ws_dim.cell(row=r_idx, column=c_idx)
            if col_name == "headcount_previsto":
                cell.value = int(row[col_name])
                cell.number_format = FMT_INT
            elif col_name == "sla_meta_pct":
                cell.value = float(row[col_name])
                cell.number_format = FMT_PCT
            elif col_name == "valor_mensal_base":
                cell.value = float(row[col_name])
                cell.number_format = FMT_BRL
            else:
                cell.value = row[col_name]
            cell.font = BODY_FONT
            cell.border = GRID_BORDER
            if r_idx % 2 == 1:
                cell.fill = ZEBRA_FILL

    ws_dim.freeze_panes = "A2"
    ws_dim.auto_filter.ref = f"A1:{get_column_letter(len(dim_cols))}{len(contratos)+1}"
    auto_ajustar_colunas(ws_dim, min_width=12, max_width=40)

    # =========================================================================
    # ABA 2: Diagnostico_Contratos (24 contratos ranqueados por Margem %)
    # =========================================================================
    # Calcular ordem de classificação (pior margem % primeiro) para ordenação inicial limpa
    perf_por_contrato: dict[str, dict] = {}
    for row in fato:
        cid = row["id_contrato"]
        d = perf_por_contrato.setdefault(cid, {"rl": 0.0, "m": 0.0})
        d["rl"] += float(row["receita_liquida"])
        d["m"] += float(row["margem_operacional"])

    contratos_ordenados = sorted(
        contratos,
        key=lambda c: perf_por_contrato[c["id_contrato"]]["m"] / perf_por_contrato[c["id_contrato"]]["rl"],
    )

    ws_diag.merge_cells("A1:P1")
    ws_diag["A1"] = "DIAGNÓSTICO POR CONTRATO — MARGEM, ABSENTEÍSMO, HORA EXTRA E SLA (2025)"
    ws_diag["A1"].font = TITLE_FONT
    ws_diag["A1"].fill = HEADER_FILL
    ws_diag["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_diag.row_dimensions[1].height = 30

    ws_diag.merge_cells("A2:P2")
    ws_diag["A2"] = "Regra de Status (via fórmula SE/OU): Crítico (Margem < 8% ou Absenteísmo > 6%) | Atenção (Margem < 12% ou Absenteísmo > 4%) | Saudável (Demais)"
    ws_diag["A2"].font = SUBTITLE_FONT
    ws_diag["A2"].fill = SUBHEADER_FILL
    ws_diag["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_diag.row_dimensions[2].height = 20

    diag_headers = [
        "ID Contrato",
        "Nome do Contrato",
        "Linha de Serviço",
        "Cidade",
        "UF",
        "Segmento",
        "Headcount",
        "Receita Líquida",
        "Custo Hora Extra",
        "Glosas SLA",
        "Custo Turnover",
        "Margem Operacional",
        "Margem %",
        "Absenteísmo %",
        "SLA Médio %",
        "Status",
    ]
    for c_idx, h in enumerate(diag_headers, start=1):
        cell = ws_diag.cell(row=4, column=c_idx, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = GRID_BORDER
    ws_diag.row_dimensions[4].height = 28

    start_diag = 5
    for idx, c in enumerate(contratos_ordenados):
        r = start_diag + idx
        cid = c["id_contrato"]
        ws_diag.cell(row=r, column=1, value=cid)
        ws_diag.cell(row=r, column=2, value=c["nome_contrato"])
        ws_diag.cell(row=r, column=3, value=c["linha_servico"])
        ws_diag.cell(row=r, column=4, value=c["cidade"])
        ws_diag.cell(row=r, column=5, value=c["uf"])
        ws_diag.cell(row=r, column=6, value=c["segmento"])
        ws_diag.cell(row=r, column=7, value=int(c["headcount_previsto"])).number_format = FMT_INT

        # Fórmulas SUMIFS / AVERAGEIFS dinâmicas ligadas à Base_Operacoes
        ws_diag.cell(row=r, column=8, value=f'=SUMIFS(Base_Operacoes!$S$2:$S${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_diag.cell(row=r, column=9, value=f'=SUMIFS(Base_Operacoes!$U$2:$U${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_diag.cell(row=r, column=10, value=f'=SUMIFS(Base_Operacoes!$R$2:$R${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_diag.cell(row=r, column=11, value=f'=SUMIFS(Base_Operacoes!$W$2:$W${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_diag.cell(row=r, column=12, value=f'=SUMIFS(Base_Operacoes!$Y$2:$Y${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_diag.cell(row=r, column=13, value=f'=IFERROR(L{r}/H{r},0)').number_format = FMT_PCT
        ws_diag.cell(
            row=r,
            column=14,
            value=f'=IFERROR(SUMIFS(Base_Operacoes!$L$2:$L${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r})/SUMIFS(Base_Operacoes!$AA$2:$AA${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r}),0)',
        ).number_format = FMT_PCT
        ws_diag.cell(row=r, column=15, value=f'=AVERAGEIFS(Base_Operacoes!$P$2:$P${n_fato},Base_Operacoes!$D$2:$D${n_fato},A{r})').number_format = FMT_PCT
        ws_diag.cell(row=r, column=16, value=f'=IF(OR(M{r}<0.08,N{r}>0.06),"Crítico",IF(OR(M{r}<0.12,N{r}>0.04),"Atenção","Saudável"))')

        # Estilização da linha
        m_est = perf_por_contrato[cid]["m"] / perf_por_contrato[cid]["rl"]
        for col_i in range(1, 17):
            cell = ws_diag.cell(row=r, column=col_i)
            cell.font = BODY_FONT
            cell.border = GRID_BORDER
            if r % 2 == 1:
                cell.fill = ZEBRA_FILL
            if col_i in (1, 5, 16):
                cell.alignment = Alignment(horizontal="center", vertical="center")
        status_cell = ws_diag.cell(row=r, column=16)
        if m_est < 0.08:
            status_cell.fill = CRIT_FILL
            status_cell.font = CRIT_FONT
        elif m_est < 0.12:
            status_cell.fill = WARN_FILL
            status_cell.font = WARN_FONT
        else:
            status_cell.fill = OK_FILL
            status_cell.font = OK_FONT

    end_diag = start_diag + len(contratos_ordenados) - 1
    tot_row = end_diag + 1
    ws_diag.cell(row=tot_row, column=1, value="TOTAL / MÉDIA")
    ws_diag.cell(row=tot_row, column=7, value=f"=SUM(G{start_diag}:G{end_diag})").number_format = FMT_INT
    for col_i in (8, 9, 10, 11, 12):
        col_l = get_column_letter(col_i)
        ws_diag.cell(row=tot_row, column=col_i, value=f"=SUM({col_l}{start_diag}:{col_l}{end_diag})").number_format = FMT_BRL_INT
    ws_diag.cell(row=tot_row, column=13, value=f"=L{tot_row}/H{tot_row}").number_format = FMT_PCT
    ws_diag.cell(row=tot_row, column=14, value=f"=SUM(Base_Operacoes!$L$2:$L${n_fato})/SUM(Base_Operacoes!$AA$2:$AA${n_fato})").number_format = FMT_PCT
    ws_diag.cell(row=tot_row, column=15, value=f"=AVERAGE(O{start_diag}:O{end_diag})").number_format = FMT_PCT
    ws_diag.cell(row=tot_row, column=16, value=f'=COUNTIF(P{start_diag}:P{end_diag},"Crítico")&" Críticos"')

    for col_i in range(1, 17):
        cell = ws_diag.cell(row=tot_row, column=col_i)
        cell.font = BOLD_FONT
        cell.fill = CARD_FILL
        cell.border = TOTAL_BORDER

    # Formatação condicional dinâmica na coluna Status e Margem %
    ws_diag.conditional_formatting.add(
        f"P{start_diag}:P{end_diag}",
        CellIsRule(operator="equal", formula=['"Crítico"'], fill=CRIT_FILL, font=CRIT_FONT),
    )
    ws_diag.conditional_formatting.add(
        f"P{start_diag}:P{end_diag}",
        CellIsRule(operator="equal", formula=['"Atenção"'], fill=WARN_FILL, font=WARN_FONT),
    )
    ws_diag.conditional_formatting.add(
        f"P{start_diag}:P{end_diag}",
        CellIsRule(operator="equal", formula=['"Saudável"'], fill=OK_FILL, font=OK_FONT),
    )

    ws_diag.freeze_panes = "C5"
    ws_diag.auto_filter.ref = f"A4:P{end_diag}"
    auto_ajustar_colunas(ws_diag, min_width=10, max_width=40)
    ws_diag.column_dimensions["B"].width = 40
    ws_diag.column_dimensions["C"].width = 23

    # =========================================================================
    # ABA 1: Resumo_Executivo
    # =========================================================================
    ws_resumo.merge_cells("A1:I1")
    ws_resumo["A1"] = "FACILITIES & OUTSOURCING ANALYTICS — PAINEL EXECUTIVO (2025)"
    ws_resumo["A1"].font = TITLE_FONT
    ws_resumo["A1"].fill = HEADER_FILL
    ws_resumo["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_resumo.row_dimensions[1].height = 32

    ws_resumo.merge_cells("A2:I2")
    ws_resumo["A2"] = "Case de Dados & Negócios | 24 Contratos no Nordeste (Teresina-PI e região) | Dados 100% sintéticos para portfólio"
    ws_resumo["A2"].font = SUBTITLE_FONT
    ws_resumo["A2"].fill = SUBHEADER_FILL
    ws_resumo["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_resumo.row_dimensions[2].height = 20

    # Bloco de KPIs Executivos (linhas 4-6)
    kpis_cards = [
        ("A", "B", "RECEITA LÍQUIDA ANUAL", f"=SUM(Base_Operacoes!$S$2:$S${n_fato})", FMT_BRL_INT),
        ("C", "D", "MARGEM OPERACIONAL (R$)", f"=SUM(Base_Operacoes!$Y$2:$Y${n_fato})", FMT_BRL_INT),
        ("E", "E", "MARGEM %", "=C5/A5", FMT_PCT),
        ("F", "F", "ABSENTEÍSMO %", f"=SUM(Base_Operacoes!$L$2:$L${n_fato})/SUM(Base_Operacoes!$AA$2:$AA${n_fato})", FMT_PCT),
        ("G", "H", "CUSTO HORA EXTRA COBERTURA", f"=SUM(Base_Operacoes!$U$2:$U${n_fato})", FMT_BRL_INT),
        ("I", "I", "GLOSAS POR SLA", f"=SUM(Base_Operacoes!$R$2:$R${n_fato})", FMT_BRL_INT),
    ]
    ws_resumo.row_dimensions[4].height = 18
    ws_resumo.row_dimensions[5].height = 28
    for c_ini, c_fim, label, formula, num_fmt in kpis_cards:
        if c_ini != c_fim:
            ws_resumo.merge_cells(f"{c_ini}4:{c_fim}4")
            ws_resumo.merge_cells(f"{c_ini}5:{c_fim}5")
        lbl_cell = ws_resumo[f"{c_ini}4"]
        lbl_cell.value = label
        lbl_cell.font = KPI_LABEL_FONT
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")

        val_cell = ws_resumo[f"{c_ini}5"]
        val_cell.value = formula
        val_cell.font = KPI_VAL_FONT
        val_cell.number_format = num_fmt
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        for col_ord in range(ord(c_ini), ord(c_fim) + 1):
            col_l = chr(col_ord)
            ws_resumo[f"{col_l}4"].fill = CARD_FILL
            ws_resumo[f"{col_l}5"].fill = CARD_FILL
            ws_resumo[f"{col_l}4"].border = GRID_BORDER
            ws_resumo[f"{col_l}5"].border = GRID_BORDER

    # Tabela 1: Desempenho por Linha de Serviço (linhas 7-13)
    ws_resumo["A7"] = "1. Desempenho por Linha de Serviço"
    ws_resumo["A7"].font = SECTION_FONT
    ws_resumo.row_dimensions[7].height = 24

    headers_linha = [
        "Linha de Serviço",
        "Receita Bruta",
        "Glosas SLA",
        "Receita Líquida",
        "Custo Hora Extra",
        "Custo Turnover",
        "Margem Operacional",
        "Margem %",
        "Absenteísmo %",
    ]
    for c_i, h in enumerate(headers_linha, start=1):
        cell = ws_resumo.cell(row=8, column=c_i, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = GRID_BORDER
    ws_resumo.row_dimensions[8].height = 26

    linhas_servico = [
        "Segurança Privada",
        "Limpeza e Conservação",
        "Manutenção Predial",
        "Atendimento e Recepção",
    ]
    for idx, linha in enumerate(linhas_servico):
        r = 9 + idx
        ws_resumo.cell(row=r, column=1, value=linha)
        ws_resumo.cell(row=r, column=2, value=f'=SUMIFS(Base_Operacoes!$Q$2:$Q${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=3, value=f'=SUMIFS(Base_Operacoes!$R$2:$R${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=4, value=f'=SUMIFS(Base_Operacoes!$S$2:$S${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=5, value=f'=SUMIFS(Base_Operacoes!$U$2:$U${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=6, value=f'=SUMIFS(Base_Operacoes!$W$2:$W${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=7, value=f'=SUMIFS(Base_Operacoes!$Y$2:$Y${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=8, value=f'=IFERROR(G{r}/D{r},0)').number_format = FMT_PCT
        ws_resumo.cell(
            row=r,
            column=9,
            value=f'=IFERROR(SUMIFS(Base_Operacoes!$L$2:$L${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r})/SUMIFS(Base_Operacoes!$AA$2:$AA${n_fato},Base_Operacoes!$G$2:$G${n_fato},A{r}),0)',
        ).number_format = FMT_PCT

        for c_i in range(1, 10):
            cell = ws_resumo.cell(row=r, column=c_i)
            cell.font = BODY_FONT
            cell.border = GRID_BORDER
            if r % 2 == 0:
                cell.fill = ZEBRA_FILL

    # Total Linhas (row 13)
    ws_resumo.cell(row=13, column=1, value="Total Geral")
    for c_i in range(2, 8):
        col_l = get_column_letter(c_i)
        ws_resumo.cell(row=13, column=c_i, value=f"=SUM({col_l}9:{col_l}12)").number_format = FMT_BRL_INT
    ws_resumo.cell(row=13, column=8, value="=G13/D13").number_format = FMT_PCT
    ws_resumo.cell(row=13, column=9, value="=F5").number_format = FMT_PCT
    for c_i in range(1, 10):
        cell = ws_resumo.cell(row=13, column=c_i)
        cell.font = BOLD_FONT
        cell.fill = CARD_FILL
        cell.border = TOTAL_BORDER

    # Tabela 2: Evolução Mensal (linhas 15-29)
    ws_resumo["A15"] = "2. Evolução Mensal (Jan–Dez 2025): Receita Cresce, Mas Margem Cai no S2"
    ws_resumo["A15"].font = SECTION_FONT
    ws_resumo.row_dimensions[15].height = 24

    headers_mes = [
        "Ano-Mês",
        "Mês",
        "Receita Bruta",
        "Glosas SLA",
        "Receita Líquida",
        "Custo Hora Extra",
        "Margem Operacional",
        "Margem %",
        "Absenteísmo %",
    ]
    for c_i, h in enumerate(headers_mes, start=1):
        cell = ws_resumo.cell(row=16, column=c_i, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = GRID_BORDER
    ws_resumo.row_dimensions[16].height = 26

    for idx, cal in enumerate(calendario):
        r = 17 + idx
        ws_resumo.cell(row=r, column=1, value=cal["ano_mes"]).alignment = Alignment(horizontal="center")
        ws_resumo.cell(row=r, column=2, value=cal["mes_abrev"]).alignment = Alignment(horizontal="center")
        ws_resumo.cell(row=r, column=3, value=f'=SUMIFS(Base_Operacoes!$Q$2:$Q${n_fato},Base_Operacoes!$C$2:$C${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=4, value=f'=SUMIFS(Base_Operacoes!$R$2:$R${n_fato},Base_Operacoes!$C$2:$C${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=5, value=f'=SUMIFS(Base_Operacoes!$S$2:$S${n_fato},Base_Operacoes!$C$2:$C${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=6, value=f'=SUMIFS(Base_Operacoes!$U$2:$U${n_fato},Base_Operacoes!$C$2:$C${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=7, value=f'=SUMIFS(Base_Operacoes!$Y$2:$Y${n_fato},Base_Operacoes!$C$2:$C${n_fato},A{r})').number_format = FMT_BRL_INT
        ws_resumo.cell(row=r, column=8, value=f'=IFERROR(G{r}/E{r},0)').number_format = FMT_PCT
        ws_resumo.cell(
            row=r,
            column=9,
            value=f'=IFERROR(SUMIFS(Base_Operacoes!$L$2:$L${n_fato},Base_Operacoes!$C$2:$C${n_fato},A{r})/SUMIFS(Base_Operacoes!$AA$2:$AA${n_fato},Base_Operacoes!$C$2:$C${n_fato},A{r}),0)',
        ).number_format = FMT_PCT

        for c_i in range(1, 10):
            cell = ws_resumo.cell(row=r, column=c_i)
            cell.font = BODY_FONT
            cell.border = GRID_BORDER
            if r % 2 == 0:
                cell.fill = ZEBRA_FILL

    # Comparativo S1 vs S2 (linhas 30-31)
    ws_resumo.cell(row=29, column=1, value="Acumulado S1 (Jan–Jun)")
    ws_resumo.cell(row=30, column=1, value="Acumulado S2 (Jul–Dez)")
    for c_i in range(3, 8):
        col_l = get_column_letter(c_i)
        ws_resumo.cell(row=29, column=c_i, value=f"=SUM({col_l}17:{col_l}22)").number_format = FMT_BRL_INT
        ws_resumo.cell(row=30, column=c_i, value=f"=SUM({col_l}23:{col_l}28)").number_format = FMT_BRL_INT
    ws_resumo.cell(row=29, column=8, value="=G29/E29").number_format = FMT_PCT
    ws_resumo.cell(row=30, column=8, value="=G30/E30").number_format = FMT_PCT
    ws_resumo.cell(
        row=29,
        column=9,
        value=f'=SUMIFS(Base_Operacoes!$L$2:$L${n_fato},Base_Operacoes!$C$2:$C${n_fato},"<=2025-06")/SUMIFS(Base_Operacoes!$AA$2:$AA${n_fato},Base_Operacoes!$C$2:$C${n_fato},"<=2025-06")',
    ).number_format = FMT_PCT
    ws_resumo.cell(
        row=30,
        column=9,
        value=f'=SUMIFS(Base_Operacoes!$L$2:$L${n_fato},Base_Operacoes!$C$2:$C${n_fato},">=2025-07")/SUMIFS(Base_Operacoes!$AA$2:$AA${n_fato},Base_Operacoes!$C$2:$C${n_fato},">=2025-07")',
    ).number_format = FMT_PCT
    for r_s in (29, 30):
        for c_i in range(1, 10):
            cell = ws_resumo.cell(row=r_s, column=c_i)
            cell.font = BOLD_FONT
            cell.fill = CARD_FILL
            cell.border = TOTAL_BORDER

    # Gráfico nativo no Excel (Receita Líquida vs Margem Operacional por Mês)
    bar_chart = BarChart()
    bar_chart.type = "col"
    bar_chart.title = "Receita Líquida vs Margem Operacional (R$)"
    bar_chart.y_axis.title = "Valor (R$)"
    bar_chart.x_axis.title = "Mês (2025)"
    data_ref = Reference(ws_resumo, min_col=5, max_col=5, min_row=16, max_row=28)
    data_margem = Reference(ws_resumo, min_col=7, max_col=7, min_row=16, max_row=28)
    cats = Reference(ws_resumo, min_col=2, min_row=17, max_row=28)
    bar_chart.add_data(data_ref, titles_from_data=True)
    bar_chart.add_data(data_margem, titles_from_data=True)
    bar_chart.set_categories(cats)
    bar_chart.width = 18
    bar_chart.height = 10
    ws_resumo.add_chart(bar_chart, "K7")

    line_chart = LineChart()
    line_chart.title = "Evolução de Margem % vs Absenteísmo %"
    line_chart.y_axis.number_format = "0.0%"
    pct_data = Reference(ws_resumo, min_col=8, max_col=9, min_row=16, max_row=28)
    line_chart.add_data(pct_data, titles_from_data=True)
    line_chart.set_categories(cats)
    line_chart.width = 18
    line_chart.height = 10
    ws_resumo.add_chart(line_chart, "K23")

    ws_resumo.freeze_panes = "A4"
    widths_resumo = {
        "A": 26,
        "B": 16,
        "C": 16,
        "D": 17,
        "E": 17,
        "F": 17,
        "G": 20,
        "H": 14,
        "I": 16,
    }
    for col_l, w in widths_resumo.items():
        ws_resumo.column_dimensions[col_l].width = w

    wb.save(OUTPUT_XLSX)
    return OUTPUT_XLSX


if __name__ == "__main__":
    out = construir_excel()
    print(f"Workbook Excel gerado com sucesso: {out} ({out.stat().st_size:,} bytes)")
