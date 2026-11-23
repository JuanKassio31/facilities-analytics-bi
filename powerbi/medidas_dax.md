# Catálogo de Medidas DAX — Facilities & Outsourcing BI

Todas as medidas abaixo foram escritas em DAX padrão para o Power BI Desktop utilizando as tabelas do modelo estrela (`fato_operacoes`, `dim_contratos` e `dim_calendario`).

> **Sugestão de organização:** Crie uma tabela vazia chamada `_Medidas` (via *Inserir Dados*) e organize as medidas nas pastas de exibição indicadas abaixo.

---

## 1. Pasta: `01. Financeiro & Margem`

```dax
Receita Bruta =
SUM(fato_operacoes[receita_bruta])
```

```dax
Total Glosas SLA =
SUM(fato_operacoes[glosa_sla])
```

```dax
Receita Líquida =
SUM(fato_operacoes[receita_liquida])
```

```dax
Custo Folha Base =
SUM(fato_operacoes[custo_folha_base])
```

```dax
Custo Hora Extra Cobertura =
SUM(fato_operacoes[custo_hora_extra_cobertura])
```

```dax
Custo Rescisão e Admissão =
SUM(fato_operacoes[custo_rescisao_admissao])
```

```dax
Custo Insumos =
SUM(fato_operacoes[custo_insumos])
```

```dax
Custo Total =
SUM(fato_operacoes[custo_total])
```

```dax
Margem Operacional R$ =
[Receita Líquida] - [Custo Total]
```

```dax
Margem Operacional % =
DIVIDE([Margem Operacional R$], [Receita Líquida], 0)
```
*(Formatar como Percentual `0.0%`)*

```dax
Perdas por Ineficiência R$ =
[Custo Hora Extra Cobertura] + [Total Glosas SLA] + [Custo Rescisão e Admissão]
```

---

## 2. Pasta: `02. Operação & Pessoas (Absenteísmo e SLA)`

```dax
Postos-Dia Previstos =
SUMX(
    fato_operacoes,
    fato_operacoes[headcount_previsto] * fato_operacoes[dias_uteis]
)
```

```dax
Total Faltas =
SUM(fato_operacoes[faltas_colaboradores])
```

```dax
Taxa Absenteísmo % =
DIVIDE([Total Faltas], [Postos-Dia Previstos], 0)
```
*(Formatar como Percentual `0.0%`)*

```dax
Headcount Médio =
AVERAGEX(
    VALUES(dim_calendario[ano_mes]),
    SUM(fato_operacoes[headcount_previsto])
)
```

```dax
Total Desligamentos =
SUM(fato_operacoes[desligamentos])
```

```dax
Taxa Turnover Mensal Média % =
AVERAGE(fato_operacoes[taxa_turnover_pct])
```
*(Formatar como Percentual `0.0%`)*

```dax
SLA Médio % =
AVERAGE(fato_operacoes[sla_atingido_pct])
```
*(Formatar como Percentual `0.0%`)*

---

## 3. Pasta: `03. Diagnóstico de Contratos & Impacto`

```dax
Status Contrato =
VAR _Margem = [Margem Operacional %]
VAR _Abs = [Taxa Absenteísmo %]
RETURN
SWITCH(
    TRUE(),
    ISBLANK([Receita Líquida]), BLANK(),
    _Margem < 0.08 || _Abs > 0.06, "Crítico",
    _Margem < 0.12 || _Abs > 0.04, "Atenção",
    "Saudável"
)
```

```dax
Contratos Críticos =
COUNTROWS(
    FILTER(
        VALUES(dim_contratos[id_contrato]),
        [Margem Operacional %] < 0.08 || [Taxa Absenteísmo %] > 0.06
    )
)
```

```dax
Hora Extra Contratos Críticos =
CALCULATE(
    [Custo Hora Extra Cobertura],
    FILTER(
        VALUES(dim_contratos[id_contrato]),
        [Margem Operacional %] < 0.08 || [Taxa Absenteísmo %] > 0.06
    )
)
```

```dax
% Hora Extra nos Críticos =
DIVIDE([Hora Extra Contratos Críticos], [Custo Hora Extra Cobertura], 0)
```

```dax
Glosas Contratos Críticos =
CALCULATE(
    [Total Glosas SLA],
    FILTER(
        VALUES(dim_contratos[id_contrato]),
        [Margem Operacional %] < 0.08 || [Taxa Absenteísmo %] > 0.06
    )
)
```

```dax
Potencial de Recuperação R$ =
VAR _ContratosCriticos =
    FILTER(
        VALUES(dim_contratos[id_contrato]),
        [Margem Operacional %] < 0.08 || [Taxa Absenteísmo %] > 0.06
    )
VAR _RecHE =
    CALCULATE([Custo Hora Extra Cobertura], _ContratosCriticos) * 0.60
VAR _RecGlosa =
    CALCULATE([Total Glosas SLA], _ContratosCriticos) * 0.80
VAR _RecTurnover =
    CALCULATE([Custo Rescisão e Admissão], _ContratosCriticos) * 0.35
RETURN
_RecHE + _RecGlosa + _RecTurnover
```

---

## 4. Pasta: `04. Comparativo Semestral (S1 vs S2)`

```dax
Margem % S1 =
CALCULATE(
    [Margem Operacional %],
    dim_calendario[semestre] = "S1"
)
```

```dax
Margem % S2 =
CALCULATE(
    [Margem Operacional %],
    dim_calendario[semestre] = "S2"
)
```

```dax
Variação Margem S2 vs S1 (pp) =
([Margem % S2] - [Margem % S1]) * 100
```
*(Formatar como `+#,##0.0" pp";-#,##0.0" pp";0.0" pp"`)*
