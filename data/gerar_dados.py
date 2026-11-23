"""
Gerador de base de dados simulada para o case:
Facilities & Outsourcing Analytics — Gestão de Contratos, Absenteísmo, SLA e Margem Operacional.

Nota: Todos os dados gerados são 100% sintéticos (fictícios), criados exclusivamente
para fins de estudo, portfólio e demonstração de análise de dados e negócios.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path


SEED = 42
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"


CALENDARIO_2025 = [
    ("2025-01-01", 2025, "S1", "T1", 1, "Janeiro", "Jan", "2025-01", 22),
    ("2025-02-01", 2025, "S1", "T1", 2, "Fevereiro", "Fev", "2025-02", 20),
    ("2025-03-01", 2025, "S1", "T1", 3, "Março", "Mar", "2025-03", 21),
    ("2025-04-01", 2025, "S1", "T2", 4, "Abril", "Abr", "2025-04", 21),
    ("2025-05-01", 2025, "S1", "T2", 5, "Maio", "Mai", "2025-05", 22),
    ("2025-06-01", 2025, "S1", "T2", 6, "Junho", "Jun", "2025-06", 21),
    ("2025-07-01", 2025, "S2", "T3", 7, "Julho", "Jul", "2025-07", 23),
    ("2025-08-01", 2025, "S2", "T3", 8, "Agosto", "Ago", "2025-08", 21),
    ("2025-09-01", 2025, "S2", "T3", 9, "Setembro", "Set", "2025-09", 22),
    ("2025-10-01", 2025, "S2", "T4", 10, "Outubro", "Out", "2025-10", 23),
    ("2025-11-01", 2025, "S2", "T4", 11, "Novembro", "Nov", "2025-11", 20),
    ("2025-12-01", 2025, "S2", "T4", 12, "Dezembro", "Dez", "2025-12", 22),
]

# 24 contratos distribuídos entre 4 linhas de serviço e 6 cidades do Nordeste (foco PI/MA/CE/PE)
# Os contratos marcados com critica_h2=True representam os 6 focos de deterioração no S2 (Jul-Dez).
CONTRATOS_SPEC = [
    # --- TERESINA - PI (9 contratos) ---
    {
        "id_contrato": "CTR-001",
        "nome_contrato": "Hospital Regional Sul — Higienização",
        "segmento": "Hospitalar",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 58,
        "turno_predominante": "24h (12x36)",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 4350.0,
        "insumo_pct": 0.085,
        "critica_h2": True,
        "severidade": 1.15,
    },
    {
        "id_contrato": "CTR-002",
        "nome_contrato": "Shopping Poty Center — Segurança",
        "segmento": "Varejo & Shopping",
        "linha_servico": "Segurança Privada",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 44,
        "turno_predominante": "Noturno / 12x36",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 6450.0,
        "insumo_pct": 0.030,
        "critica_h2": True,
        "severidade": 1.20,
    },
    {
        "id_contrato": "CTR-003",
        "nome_contrato": "Centro Administrativo Estadual — Recepção",
        "segmento": "Órgão Público",
        "linha_servico": "Atendimento e Recepção",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 28,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4150.0,
        "insumo_pct": 0.025,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-004",
        "nome_contrato": "Campus Universitário Fátima — Limpeza",
        "segmento": "Educação",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 40,
        "turno_predominante": "Diurno / Vespertino",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4100.0,
        "insumo_pct": 0.075,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-005",
        "nome_contrato": "Torre Empresarial Dom Severino — Manutenção",
        "segmento": "Corporativo",
        "linha_servico": "Manutenção Predial",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 16,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 7200.0,
        "insumo_pct": 0.095,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-006",
        "nome_contrato": "Distrito Industrial Teresina — Vigilância",
        "segmento": "Indústria",
        "linha_servico": "Segurança Privada",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 36,
        "turno_predominante": "Noturno / 12x36",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 6250.0,
        "insumo_pct": 0.028,
        "critica_h2": True,
        "severidade": 1.05,
    },
    {
        "id_contrato": "CTR-007",
        "nome_contrato": "Clínica Integrada Centro — Atendimento",
        "segmento": "Hospitalar",
        "linha_servico": "Atendimento e Recepção",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 22,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4300.0,
        "insumo_pct": 0.025,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-008",
        "nome_contrato": "Tribunal Regional PI — Manutenção Predial",
        "segmento": "Órgão Público",
        "linha_servico": "Manutenção Predial",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 18,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 6950.0,
        "insumo_pct": 0.088,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-009",
        "nome_contrato": "Rede Supermercado Norte — Limpeza",
        "segmento": "Varejo & Shopping",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "Teresina",
        "uf": "PI",
        "headcount_previsto": 30,
        "turno_predominante": "Misto / Escala",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 3980.0,
        "insumo_pct": 0.080,
        "critica_h2": False,
        "severidade": 0.0,
    },
    # --- TIMON - MA (3 contratos) ---
    {
        "id_contrato": "CTR-010",
        "nome_contrato": "Polo Logístico Timon — Vigilância Patrimonial",
        "segmento": "Indústria",
        "linha_servico": "Segurança Privada",
        "cidade": "Timon",
        "uf": "MA",
        "headcount_previsto": 32,
        "turno_predominante": "24h (12x36)",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 6150.0,
        "insumo_pct": 0.028,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-011",
        "nome_contrato": "Hospital Municipal Timon — Limpeza Técnica",
        "segmento": "Hospitalar",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "Timon",
        "uf": "MA",
        "headcount_previsto": 34,
        "turno_predominante": "24h (12x36)",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 4250.0,
        "insumo_pct": 0.090,
        "critica_h2": True,
        "severidade": 0.95,
    },
    {
        "id_contrato": "CTR-012",
        "nome_contrato": "Faculdade Metropolitana Timon — Recepção",
        "segmento": "Educação",
        "linha_servico": "Atendimento e Recepção",
        "cidade": "Timon",
        "uf": "MA",
        "headcount_previsto": 14,
        "turno_predominante": "Diurno / Noturno",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 3950.0,
        "insumo_pct": 0.022,
        "critica_h2": False,
        "severidade": 0.0,
    },
    # --- PARNAÍBA - PI (2 contratos) ---
    {
        "id_contrato": "CTR-013",
        "nome_contrato": "Complexo Litoral Parnaíba — Manutenção",
        "segmento": "Corporativo",
        "linha_servico": "Manutenção Predial",
        "cidade": "Parnaíba",
        "uf": "PI",
        "headcount_previsto": 12,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 6850.0,
        "insumo_pct": 0.092,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-014",
        "nome_contrato": "Instituto Federal Delta — Limpeza",
        "segmento": "Educação",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "Parnaíba",
        "uf": "PI",
        "headcount_previsto": 24,
        "turno_predominante": "Diurno",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 3920.0,
        "insumo_pct": 0.072,
        "critica_h2": False,
        "severidade": 0.0,
    },
    # --- SÃO LUÍS - MA (4 contratos) ---
    {
        "id_contrato": "CTR-015",
        "nome_contrato": "Terminal Portuário Ilha — Segurança Armada",
        "segmento": "Indústria",
        "linha_servico": "Segurança Privada",
        "cidade": "São Luís",
        "uf": "MA",
        "headcount_previsto": 46,
        "turno_predominante": "24h (12x36)",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 6750.0,
        "insumo_pct": 0.032,
        "critica_h2": True,
        "severidade": 1.12,
    },
    {
        "id_contrato": "CTR-016",
        "nome_contrato": "Shopping Praia Maranhão — Limpeza",
        "segmento": "Varejo & Shopping",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "São Luís",
        "uf": "MA",
        "headcount_previsto": 38,
        "turno_predominante": "Misto / Escala",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4180.0,
        "insumo_pct": 0.082,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-017",
        "nome_contrato": "Sede Corporativa Renascença — Recepção",
        "segmento": "Corporativo",
        "linha_servico": "Atendimento e Recepção",
        "cidade": "São Luís",
        "uf": "MA",
        "headcount_previsto": 16,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4450.0,
        "insumo_pct": 0.025,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-018",
        "nome_contrato": "Hospital São Marcos — Manutenção Predial",
        "segmento": "Hospitalar",
        "linha_servico": "Manutenção Predial",
        "cidade": "São Luís",
        "uf": "MA",
        "headcount_previsto": 20,
        "turno_predominante": "24h (Plantão)",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 7450.0,
        "insumo_pct": 0.095,
        "critica_h2": False,
        "severidade": 0.0,
    },
    # --- FORTALEZA - CE (3 contratos) ---
    {
        "id_contrato": "CTR-019",
        "nome_contrato": "Mall Aldeota — Limpeza & Conservação",
        "segmento": "Varejo & Shopping",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "Fortaleza",
        "uf": "CE",
        "headcount_previsto": 42,
        "turno_predominante": "Misto / Escala",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4380.0,
        "insumo_pct": 0.084,
        "critica_h2": True,
        "severidade": 1.00,
    },
    {
        "id_contrato": "CTR-020",
        "nome_contrato": "Parque Tecnológico Ceará — Segurança",
        "segmento": "Corporativo",
        "linha_servico": "Segurança Privada",
        "cidade": "Fortaleza",
        "uf": "CE",
        "headcount_previsto": 30,
        "turno_predominante": "24h (12x36)",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 6550.0,
        "insumo_pct": 0.028,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-021",
        "nome_contrato": "Secretaria Fazenda CE — Atendimento",
        "segmento": "Órgão Público",
        "linha_servico": "Atendimento e Recepção",
        "cidade": "Fortaleza",
        "uf": "CE",
        "headcount_previsto": 24,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4350.0,
        "insumo_pct": 0.024,
        "critica_h2": False,
        "severidade": 0.0,
    },
    # --- RECIFE - PE (3 contratos) ---
    {
        "id_contrato": "CTR-022",
        "nome_contrato": "Fábrica Suape Alimentos — Limpeza Industrial",
        "segmento": "Indústria",
        "linha_servico": "Limpeza e Conservação",
        "cidade": "Recife",
        "uf": "PE",
        "headcount_previsto": 36,
        "turno_predominante": "Turnos A/B",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 4420.0,
        "insumo_pct": 0.088,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-023",
        "nome_contrato": "Centro Empresarial Boa Viagem — Segurança",
        "segmento": "Corporativo",
        "linha_servico": "Segurança Privada",
        "cidade": "Recife",
        "uf": "PE",
        "headcount_previsto": 28,
        "turno_predominante": "24h (12x36)",
        "sla_meta_pct": 0.96,
        "valor_posto_mensal": 6650.0,
        "insumo_pct": 0.028,
        "critica_h2": False,
        "severidade": 0.0,
    },
    {
        "id_contrato": "CTR-024",
        "nome_contrato": "Universidade Recife Campus — Manutenção",
        "segmento": "Educação",
        "linha_servico": "Manutenção Predial",
        "cidade": "Recife",
        "uf": "PE",
        "headcount_previsto": 15,
        "turno_predominante": "Comercial",
        "sla_meta_pct": 0.95,
        "valor_posto_mensal": 7150.0,
        "insumo_pct": 0.090,
        "critica_h2": False,
        "severidade": 0.0,
    },
]


def gerar_dados() -> dict:
    rng = random.Random(SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    # 1. dim_calendario.csv
    cal_headers = [
        "data",
        "ano",
        "semestre",
        "trimestre",
        "mes_num",
        "mes_nome",
        "mes_abrev",
        "ano_mes",
        "dias_uteis",
    ]
    with (DATA_DIR / "dim_calendario.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(cal_headers)
        for row in CALENDARIO_2025:
            writer.writerow(row)

    # 2. dim_contratos.csv
    dim_headers = [
        "id_contrato",
        "nome_contrato",
        "segmento",
        "linha_servico",
        "cidade",
        "uf",
        "headcount_previsto",
        "turno_predominante",
        "sla_meta_pct",
        "valor_mensal_base",
    ]
    with (DATA_DIR / "dim_contratos.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(dim_headers)
        for c in CONTRATOS_SPEC:
            valor_base = round(c["headcount_previsto"] * c["valor_posto_mensal"], 2)
            writer.writerow([
                c["id_contrato"],
                c["nome_contrato"],
                c["segmento"],
                c["linha_servico"],
                c["cidade"],
                c["uf"],
                c["headcount_previsto"],
                c["turno_predominante"],
                f"{c['sla_meta_pct']:.4f}",
                f"{valor_base:.2f}",
            ])

    # 3. fato_operacoes.csv (24 contratos x 12 meses = 288 registros)
    fato_headers = [
        "id_registro",
        "data",
        "ano_mes",
        "id_contrato",
        "nome_contrato",
        "segmento",
        "linha_servico",
        "cidade",
        "uf",
        "headcount_previsto",
        "dias_uteis",
        "faltas_colaboradores",
        "taxa_absenteismo_pct",
        "desligamentos",
        "taxa_turnover_pct",
        "sla_atingido_pct",
        "receita_bruta",
        "glosa_sla",
        "receita_liquida",
        "custo_folha_base",
        "custo_hora_extra_cobertura",
        "custo_insumos",
        "custo_rescisao_admissao",
        "custo_total",
        "margem_operacional",
        "margem_pct",
    ]

    registros = []
    rec_counter = 1

    for cal in CALENDARIO_2025:
        data_str, _ano, _sem, _tri, mes_num, _mes_nome, _mes_abrev, ano_mes, dias_uteis = cal
        # Crescimento gradual de faturamento ao longo do ano (reajustes + ampliações de escopo no S2)
        fator_crescimento_receita = 1.0 + (mes_num - 1) * 0.008 + (0.025 if mes_num >= 7 else 0.0)

        for c in CONTRATOS_SPEC:
            hc = c["headcount_previsto"]
            postos_dia = hc * dias_uteis
            critico = c["critica_h2"]
            sev = c["severidade"]

            # Receita bruta cresce suavemente com o ano + pequeno ruído operacional de escopo extra
            receita_bruta = round(
                hc * c["valor_posto_mensal"] * fator_crescimento_receita * rng.uniform(0.992, 1.018),
                2,
            )

            # Folha base (salário + encargos + benefícios ~ 73.5% a 76% da receita base de referência)
            ratio_folha_por_linha = {
                "Limpeza e Conservação": 0.720,
                "Segurança Privada": 0.765,
                "Atendimento e Recepção": 0.755,
                "Manutenção Predial": 0.695,
            }[c["linha_servico"]]
            custo_folha_base = round(receita_bruta * ratio_folha_por_linha * rng.uniform(0.99, 1.01), 2)
            custo_insumos = round(receita_bruta * c["insumo_pct"] * rng.uniform(0.96, 1.04), 2)

            # Comportamento de Absenteísmo, Turnover e SLA:
            # Contratos saudáveis mantêm absenteísmo entre 1.8% e 3.8% o ano todo.
            # Contratos em atenção (3 contratos de alta demanda) operam com absenteísmo entre 4.2% e 5.5%.
            # Os 6 contratos críticos já começam pressionados no S1 (4.4%-6.2%)
            # e sofrem deterioração acentuada no S2 (Jul-Dez: 8.5%-13.5%), especialmente Out-Dez.
            atencao_ids = {"CTR-009", "CTR-010", "CTR-018"}
            is_atencao = (not critico) and (c["id_contrato"] in atencao_ids)

            if not critico and not is_atencao:
                abs_alvo = rng.uniform(0.019, 0.036)
                if mes_num in (7, 12):
                    abs_alvo += rng.uniform(0.002, 0.005)
                turnover_alvo = rng.uniform(0.012, 0.030)
            elif is_atencao:
                abs_alvo = rng.uniform(0.042, 0.056)
                if mes_num >= 8:
                    abs_alvo += rng.uniform(0.004, 0.010)
                turnover_alvo = rng.uniform(0.030, 0.048)
            else:
                if mes_num <= 6:
                    abs_alvo = rng.uniform(0.044, 0.062) * (0.95 + 0.05 * sev)
                    turnover_alvo = rng.uniform(0.025, 0.048)
                else:
                    # Escalada progressiva entre Julho e Dezembro
                    rampa = (mes_num - 6) / 6.0
                    abs_alvo = (0.078 + 0.038 * rampa) * sev * rng.uniform(0.94, 1.07)
                    abs_alvo = min(abs_alvo, 0.145)
                    turnover_alvo = (0.052 + 0.034 * rampa) * sev * rng.uniform(0.92, 1.08)

            faltas = max(1, int(round(postos_dia * abs_alvo)))
            taxa_abs = faltas / postos_dia

            # Desligamentos mensais
            desligamentos = max(0, int(round(hc * turnover_alvo)))
            if critico and mes_num >= 7 and desligamentos == 0:
                desligamentos = 1
            taxa_turnover = desligamentos / hc

            # Custo diário médio por colaborador na folha
            custo_dia_colaborador = custo_folha_base / postos_dia

            # Cobertura por hora extra / diária emergencial:
            if not critico and not is_atencao:
                fator_cobertura = rng.uniform(0.32, 0.48)
                multiplicador_he = rng.uniform(1.60, 1.75)
            elif is_atencao:
                fator_cobertura = rng.uniform(0.65, 0.82)
                multiplicador_he = rng.uniform(1.80, 1.98)
            elif mes_num <= 6:
                fator_cobertura = rng.uniform(0.65, 0.80)
                multiplicador_he = rng.uniform(1.80, 1.95)
            else:
                fator_cobertura = rng.uniform(0.92, 1.05)
                multiplicador_he = rng.uniform(2.05, 2.25)

            custo_he = round(faltas * custo_dia_colaborador * fator_cobertura * multiplicador_he, 2)

            # Custo de rescisão + admissão (ASO, uniforme, integração, treinamento) por desligamento
            custo_unit_turnover = {
                "Limpeza e Conservação": 2350.0,
                "Segurança Privada": 3450.0,
                "Atendimento e Recepção": 2250.0,
                "Manutenção Predial": 3600.0,
            }[c["linha_servico"]]
            custo_rescisao_admissao = round(desligamentos * custo_unit_turnover * rng.uniform(0.92, 1.08), 2)

            # SLA atingido: cai proporcionalmente ao excesso de absenteísmo e turnover
            if not critico and not is_atencao:
                sla = 0.992 - (taxa_abs * 0.42) - rng.uniform(0.002, 0.010)
                sla = max(0.954, min(0.996, sla))
            elif is_atencao:
                sla = 0.980 - (taxa_abs * 0.50) - rng.uniform(0.002, 0.010)
                sla = max(0.942, min(0.968, sla))
            elif mes_num <= 6:
                sla = 0.980 - (taxa_abs * 0.45) - rng.uniform(0.002, 0.008)
                sla = max(0.938, min(0.968, sla))
            else:
                sla = 0.972 - (taxa_abs * 0.56) - (taxa_turnover * 0.14) - rng.uniform(0.003, 0.010)
                sla = max(0.875, min(0.946, sla))

            # Glosa contratual por descumprimento de SLA (abaixo da meta do contrato)
            if sla >= c["sla_meta_pct"]:
                glosa_sla = 0.0
            else:
                deficit_pp = (c["sla_meta_pct"] - sla) * 100.0  # pontos percentuais abaixo da meta
                # Escalonamento realista: 1.5% base + 0.75% por ponto percentual abaixo da meta (teto 6.5%)
                pct_glosa = min(0.065, 0.015 + deficit_pp * 0.0075)
                glosa_sla = round(receita_bruta * pct_glosa, 2)

            receita_liquida = round(receita_bruta - glosa_sla, 2)
            custo_total = round(custo_folha_base + custo_he + custo_insumos + custo_rescisao_admissao, 2)
            margem_op = round(receita_liquida - custo_total, 2)
            margem_pct = margem_op / receita_liquida if receita_liquida else 0.0

            reg = {
                "id_registro": f"OP-{rec_counter:04d}",
                "data": data_str,
                "ano_mes": ano_mes,
                "id_contrato": c["id_contrato"],
                "nome_contrato": c["nome_contrato"],
                "segmento": c["segmento"],
                "linha_servico": c["linha_servico"],
                "cidade": c["cidade"],
                "uf": c["uf"],
                "headcount_previsto": hc,
                "dias_uteis": dias_uteis,
                "faltas_colaboradores": faltas,
                "taxa_absenteismo_pct": round(taxa_abs, 4),
                "desligamentos": desligamentos,
                "taxa_turnover_pct": round(taxa_turnover, 4),
                "sla_atingido_pct": round(sla, 4),
                "receita_bruta": receita_bruta,
                "glosa_sla": glosa_sla,
                "receita_liquida": receita_liquida,
                "custo_folha_base": custo_folha_base,
                "custo_hora_extra_cobertura": custo_he,
                "custo_insumos": custo_insumos,
                "custo_rescisao_admissao": custo_rescisao_admissao,
                "custo_total": custo_total,
                "margem_operacional": margem_op,
                "margem_pct": round(margem_pct, 4),
            }
            registros.append(reg)
            rec_counter += 1

    with (DATA_DIR / "fato_operacoes.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fato_headers)
        writer.writeheader()
        writer.writerows(registros)

    # 4. Exportar dashboard/data.js com dados brutos + metadados para uso offline/GitHub Pages
    contratos_dim_export = [
        {
            "id_contrato": c["id_contrato"],
            "nome_contrato": c["nome_contrato"],
            "segmento": c["segmento"],
            "linha_servico": c["linha_servico"],
            "cidade": c["cidade"],
            "uf": c["uf"],
            "headcount_previsto": c["headcount_previsto"],
            "turno_predominante": c["turno_predominante"],
            "sla_meta_pct": c["sla_meta_pct"],
        }
        for c in CONTRATOS_SPEC
    ]
    calendario_export = [
        {
            "data": row[0],
            "ano": row[1],
            "semestre": row[2],
            "trimestre": row[3],
            "mes_num": row[4],
            "mes_nome": row[5],
            "mes_abrev": row[6],
            "ano_mes": row[7],
            "dias_uteis": row[8],
        }
        for row in CALENDARIO_2025
    ]

    resumo = calcular_resumo_executivo(registros)

    payload = {
        "metadata": {
            "titulo": "Facilities & Outsourcing Analytics — Gestão de Margem, Absenteísmo e SLA",
            "periodo": "Jan–Dez 2025",
            "total_contratos": len(CONTRATOS_SPEC),
            "total_registros": len(registros),
            "aviso_dados": "Dados 100% sintéticos/simulados para fins de portfólio em Dados e Negócios.",
        },
        "calendario": calendario_export,
        "contratos": contratos_dim_export,
        "operacoes": registros,
        "resumo": resumo,
    }

    js_content = (
        "// Arquivo gerado automaticamente por data/gerar_dados.py\n"
        "window.FACILITIES_DATA = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n"
    )
    (DASHBOARD_DIR / "data.js").write_text(js_content, encoding="utf-8")

    return resumo


def calcular_resumo_executivo(registros: list[dict]) -> dict:
    tot_rec_bruta = sum(r["receita_bruta"] for r in registros)
    tot_glosa = sum(r["glosa_sla"] for r in registros)
    tot_rec_liq = sum(r["receita_liquida"] for r in registros)
    tot_custo = sum(r["custo_total"] for r in registros)
    tot_he = sum(r["custo_hora_extra_cobertura"] for r in registros)
    tot_resc = sum(r["custo_rescisao_admissao"] for r in registros)
    tot_margem = sum(r["margem_operacional"] for r in registros)
    tot_faltas = sum(r["faltas_colaboradores"] for r in registros)
    tot_postos_dia = sum(r["headcount_previsto"] * r["dias_uteis"] for r in registros)
    tot_deslig = sum(r["desligamentos"] for r in registros)
    hc_medio = sum(r["headcount_previsto"] for r in registros) / 12.0

    # H1 vs H2
    h1 = [r for r in registros if int(r["ano_mes"].split("-")[1]) <= 6]
    h2 = [r for r in registros if int(r["ano_mes"].split("-")[1]) >= 7]

    def agg_slice(rows: list[dict]) -> dict:
        rl = sum(r["receita_liquida"] for r in rows)
        rb = sum(r["receita_bruta"] for r in rows)
        m = sum(r["margem_operacional"] for r in rows)
        he = sum(r["custo_hora_extra_cobertura"] for r in rows)
        gl = sum(r["glosa_sla"] for r in rows)
        fl = sum(r["faltas_colaboradores"] for r in rows)
        pd = sum(r["headcount_previsto"] * r["dias_uteis"] for r in rows)
        sla_med = sum(r["sla_atingido_pct"] for r in rows) / len(rows)
        return {
            "receita_bruta": round(rb, 2),
            "receita_liquida": round(rl, 2),
            "margem_operacional": round(m, 2),
            "margem_pct": round(m / rl, 4) if rl else 0.0,
            "absenteismo_pct": round(fl / pd, 4) if pd else 0.0,
            "custo_hora_extra": round(he, 2),
            "glosa_sla": round(gl, 2),
            "sla_medio_pct": round(sla_med, 4),
        }

    # Por contrato
    by_contract: dict[str, list[dict]] = {}
    for r in registros:
        by_contract.setdefault(r["id_contrato"], []).append(r)

    contratos_agg = []
    for cid, rows in by_contract.items():
        rl = sum(r["receita_liquida"] for r in rows)
        m = sum(r["margem_operacional"] for r in rows)
        he = sum(r["custo_hora_extra_cobertura"] for r in rows)
        gl = sum(r["glosa_sla"] for r in rows)
        resc = sum(r["custo_rescisao_admissao"] for r in rows)
        fl = sum(r["faltas_colaboradores"] for r in rows)
        pd = sum(r["headcount_previsto"] * r["dias_uteis"] for r in rows)
        sla_med = sum(r["sla_atingido_pct"] for r in rows) / len(rows)
        h2_rows = [r for r in rows if int(r["ano_mes"].split("-")[1]) >= 7]
        h2_rl = sum(r["receita_liquida"] for r in h2_rows)
        h2_m = sum(r["margem_operacional"] for r in h2_rows)
        h2_fl = sum(r["faltas_colaboradores"] for r in h2_rows)
        h2_pd = sum(r["headcount_previsto"] * r["dias_uteis"] for r in h2_rows)
        margem_pct = m / rl if rl else 0.0
        abs_pct = fl / pd if pd else 0.0
        status = "Crítico" if (margem_pct < 0.08 or abs_pct > 0.06) else ("Atenção" if (margem_pct < 0.12 or abs_pct > 0.04) else "Saudável")
        contratos_agg.append({
            "id_contrato": cid,
            "nome_contrato": rows[0]["nome_contrato"],
            "linha_servico": rows[0]["linha_servico"],
            "cidade_uf": f"{rows[0]['cidade']} - {rows[0]['uf']}",
            "segmento": rows[0]["segmento"],
            "headcount": rows[0]["headcount_previsto"],
            "receita_liquida": round(rl, 2),
            "margem_operacional": round(m, 2),
            "margem_pct": round(margem_pct, 4),
            "margem_h2_pct": round(h2_m / h2_rl, 4) if h2_rl else 0.0,
            "absenteismo_pct": round(abs_pct, 4),
            "absenteismo_h2_pct": round(h2_fl / h2_pd, 4) if h2_pd else 0.0,
            "sla_medio_pct": round(sla_med, 4),
            "custo_hora_extra": round(he, 2),
            "glosa_sla": round(gl, 2),
            "custo_rescisao": round(resc, 2),
            "status": status,
        })

    contratos_agg.sort(key=lambda x: x["margem_pct"])
    criticos = [c for c in contratos_agg if c["status"] == "Crítico"]

    # Potencial de recuperação estimado nos contratos críticos:
    # Redução de ~60% nas horas extras de cobertura + eliminação de ~80% das glosas de SLA + ~35% do custo de turnover
    rec_he = sum(c["custo_hora_extra"] for c in criticos) * 0.60
    rec_glosa = sum(c["glosa_sla"] for c in criticos) * 0.80
    rec_turnover = sum(c["custo_rescisao"] for c in criticos) * 0.35
    potencial_recuperacao = round(rec_he + rec_glosa + rec_turnover, 2)

    # Por linha de serviço
    by_line: dict[str, list[dict]] = {}
    for r in registros:
        by_line.setdefault(r["linha_servico"], []).append(r)
    linhas_agg = []
    for linha, rows in by_line.items():
        s = agg_slice(rows)
        s["linha_servico"] = linha
        linhas_agg.append(s)
    linhas_agg.sort(key=lambda x: x["margem_pct"])

    # Evolução mensal
    mensal = []
    for cal in CALENDARIO_2025:
        ym = cal[7]
        rows = [r for r in registros if r["ano_mes"] == ym]
        s = agg_slice(rows)
        s["ano_mes"] = ym
        s["mes_abrev"] = cal[6]
        mensal.append(s)

    return {
        "kpis": {
            "receita_bruta_anual": round(tot_rec_bruta, 2),
            "glosas_sla_anual": round(tot_glosa, 2),
            "receita_liquida_anual": round(tot_rec_liq, 2),
            "custo_total_anual": round(tot_custo, 2),
            "custo_hora_extra_anual": round(tot_he, 2),
            "custo_rescisao_anual": round(tot_resc, 2),
            "margem_operacional_anual": round(tot_margem, 2),
            "margem_pct_anual": round(tot_margem / tot_rec_liq, 4),
            "absenteismo_pct_anual": round(tot_faltas / tot_postos_dia, 4),
            "sla_medio_pct": round(sum(r["sla_atingido_pct"] for r in registros) / len(registros), 4),
            "headcount_medio": int(round(hc_medio)),
            "desligamentos_anual": tot_deslig,
            "qtd_contratos_criticos": len(criticos),
            "participacao_criticos_he_pct": round(
                sum(c["custo_hora_extra"] for c in criticos) / tot_he, 4
            ) if tot_he else 0.0,
            "participacao_criticos_glosa_pct": round(
                sum(c["glosa_sla"] for c in criticos) / tot_glosa, 4
            ) if tot_glosa else 0.0,
            "potencial_recuperacao_anual": potencial_recuperacao,
        },
        "semestres": {
            "S1": agg_slice(h1),
            "S2": agg_slice(h2),
        },
        "linhas_servico": linhas_agg,
        "mensal": mensal,
        "contratos": contratos_agg,
    }


if __name__ == "__main__":
    resumo = gerar_dados()
    print("=== RESUMO EXECUTIVO GERADO ===")
    print(json.dumps(resumo["kpis"], ensure_ascii=False, indent=2))
    print("\n=== S1 vs S2 ===")
    print(json.dumps(resumo["semestres"], ensure_ascii=False, indent=2))
    print("\n=== LINHAS DE SERVIÇO ===")
    for l in resumo["linhas_servico"]:
        print(
            f"{l['linha_servico']} | Rec Líq: R$ {l['receita_liquida']:,.2f} | "
            f"Margem: {l['margem_pct']*100:.1f}% (R$ {l['margem_operacional']:,.2f}) | "
            f"Abs: {l['absenteismo_pct']*100:.1f}% | HE: R$ {l['custo_hora_extra']:,.2f} | Glosa: R$ {l['glosa_sla']:,.2f}"
        )
    print("\n=== TOP 11 CONTRATOS (CRÍTICOS + ATENÇÃO) ===")
    for c in resumo["contratos"][:11]:
        print(
            f"{c['id_contrato']} | {c['nome_contrato']} | {c['cidade_uf']} | "
            f"Margem: {c['margem_pct']*100:.1f}% (S2: {c['margem_h2_pct']*100:.1f}%) | "
            f"Abs: {c['absenteismo_pct']*100:.1f}% (S2: {c['absenteismo_h2_pct']*100:.1f}%) | "
            f"SLA: {c['sla_medio_pct']*100:.1f}% | HE: R$ {c['custo_hora_extra']:,.2f} | "
            f"Glosa: R$ {c['glosa_sla']:,.2f} | Status: {c['status']}"
        )
