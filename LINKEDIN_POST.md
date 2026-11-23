# Kit de Lançamento — GitHub, LinkedIn e Candidatura (Servfaz)

> **Atenção ao prazo:** O anúncio da vaga **Estágio de Dados e Negócios (Servfaz — Teresina/PI)** no Themos Vagas informa prazo de candidatura até **23/11/2026** (hoje!) pelo site `app.talentbrand.com.br`. Siga o checklist rápido abaixo para colocar tudo no ar e enviar sua candidatura ainda hoje.

---

## Checklist Rápido (15 minutos)

1. **Subir o projeto no GitHub:**
   - Crie um repositório público no GitHub com o nome: `facilities-analytics-bi`
   - Envie toda a pasta do projeto (`git init`, `git add .`, `git commit -m "feat: case facilities analytics bi"`, `git push`).
2. **Ativar o Dashboard Online (GitHub Pages — gratuito e impressiona muito!):**
   - No repositório do GitHub, vá em **Settings > Pages**.
   - Em *Build and deployment*, selecione **Deploy from a branch** → Branch `main` → pasta `/ (root)` → **Save**.
   - Em ~1 minuto, seu dashboard interativo estará online no link:
     `https://<seu-usuario>.github.io/facilities-analytics-bi/dashboard/`
3. **Preparar as imagens do post no LinkedIn:**
   - Abra `dashboard/index.html` no navegador em tela cheia e tire **1 print bem enquadrado** do painel (pegando os filtros, os 5 KPIs e os dois primeiros gráficos).
   - Você também pode anexar as imagens de `assets/evolucao_receita_margem.png` e `assets/absenteismo_vs_margem.png` como carrossel/galeria no LinkedIn.
4. **Publicar no LinkedIn e conectar com a equipe da Servfaz:**
   - Escolha uma das 2 opções de legenda abaixo, personalize `[SEU LINK DO GITHUB]` e `[SEU LINK DO DASHBOARD]`, e publique!
   - Marque a página oficial da **Servfaz** (`@Servfaz`) ou mencione de forma respeitosa — e **interaja com recrutadores / analistas de dados / gestores da Servfaz em Teresina** enviando uma nota educada com o link do case.
5. **Anexar na candidatura:**
   - Coloque o link do repositório GitHub e do Dashboard ao vivo no campo de portfólio/currículo da plataforma `app.talentbrand.com.br` hoje mesmo!

---

## Opção 1 de Post no LinkedIn (Storytelling Direto e Forte — Recomendada)

> Em empresas de prestação de serviços e *facilities*, o faturamento pode crescer todos os meses enquanto o lucro encolhe em silêncio.
>
> Foi exatamente essa pergunta que tentei responder no meu novo projeto de **Dados e Negócios** (com base 100% simulada de 24 contratos no Nordeste — Limpeza, Segurança Privada, Atendimento e Manutenção Predial):
>
> **O problema encontrado:**
> No 2º semestre, a receita líquida cresceu **+5,4%** (de R$ 22,5M para R$ 23,7M), mas a margem operacional despencou de **15,0% para 8,0%**.
>
> **O "porquê" por trás dos números:**
> Cruzando operação, RH e financeiro, descobri que a queda não era generalizada: **apenas 6 contratos críticos (25% da carteira)** concentravam **76,3% do custo com hora extra de cobertura** e **85,5% das glosas por falha de SLA**.
>
> O mecanismo é um efeito dominó clássico no setor:
> Absenteísmo alto (8%–12%) → cobertura emergencial em hora extra (~2x mais cara) → atrasos/falhas que derrubam o SLA abaixo de 95% → glosa contratual na fatura → aumento de *turnover*.
>
> **O impacto estimado da ação:**
> Atuando com reserva técnica volante, ajuste de escalas noturnas e gatilho preventivo de absenteísmo (> 4,5%) apenas nesses 6 contratos, o potencial de recuperação chega a **R$ 2,02 milhões/ano** na margem operacional.
>
> **O que construí neste case:**
> - Modelagem Estrela (Star Schema) + base simulada em Python
> - Planilha executiva em **Excel** com fórmulas dinâmicas (`SUMIFS`, `AVERAGEIFS`, `SE/OU`) e semáforo de status
> - Catálogo de medidas **DAX** para **Power BI**
> - **Dashboard Web Interativo** com filtros por linha de serviço, cidade (incluindo Teresina-PI), segmento e período
>
> Dashboard ao vivo: [SEU LINK DO DASHBOARD]
> Código, Excel e DAX no GitHub: [SEU LINK DO GITHUB]
>
> Como estudante interessado em atuar na ponte entre **dados e decisões de negócio**, fico aberto a feedbacks de quem trabalha com controladoria, operações, BI e *facilities*!
>
> #AnaliseDeDados #BusinessIntelligence #PowerBI #Excel #DadosENegocios #Facilities #Teresina #Piaui #PortfolioDeDados

---

## Opção 2 de Post no LinkedIn (Formato Estruturado / Portfólio Técnico)

> **Novo Projeto de Portfólio | Facilities & Outsourcing Analytics (Excel + Power BI/DAX + Python + Dashboard Interativo)**
>
> Mais do que montar gráficos bonitos, o papel de quem trabalha com **Dados e Negócios** é ouvir a dor da operação, investigar os números e devolver uma resposta clara para quem decide.
>
> Simulei a operação anual de uma empresa de terceirização e *facilities* no Nordeste (**24 contratos**, **~703 colaboradores**, **R$ 46,2M de receita líquida**) para responder: *por que a margem caiu pela metade no 2º semestre?*
>
> **Principais insights da análise:**
> - **Receita vs. Rentabilidade:** Receita líquida subiu +5,4% do S1 para o S2, mas a margem caiu de 15,0% para 8,0%.
> - **Causa raiz (Pareto):** 6 contratos (em Segurança Privada e Limpeza Hospitalar/Shopping) concentraram **76,3% das horas extras de cobertura** e **85,5% das glosas de SLA** (R$ 861 mil perdidos no ano).
> - **Linhas de serviço:** Atendimento/Recepção (20,0%) e Manutenção Predial (18,0%) sustentam a carteira, enquanto Segurança (7,1%) e Limpeza (9,9%) sofrem maior pressão de escalas.
> - **Plano de recuperação:** R$ 2,02M/ano estimados ao reduzir coberturas emergenciais e zerar glosas evitáveis nos contratos críticos.
>
> **Arquitetura do repositório:**
> - `data/`: Tabelas Fato e Dimensões (Modelo Estrela) geradas em Python
> - `excel/`: Pasta de trabalho pronta com `SUMIFS`, `AVERAGEIFS`, `IF/OR` e gráficos
> - `powerbi/`: Guia de relacionamentos e catálogo completo de medidas DAX
> - `dashboard/`: Painel interativo publicado via GitHub Pages
>
> Confira o dashboard interativo: [SEU LINK DO DASHBOARD]
> Repositório completo no GitHub: [SEU LINK DO GITHUB]
>
> Se você atua com Gestão de Contratos, Operações, RH ou BI — principalmente aqui no Piauí e Nordeste — o que você adicionaria a esse painel?
>
> #PowerBI #Excel #DAX #Python #BusinessAnalytics #FacilitiesManagement #EstagioDados #Teresina

---

## Mensagem Curta para Enviar no LinkedIn ao Recrutador / Gestor (Opcional, mas Diferencial!)

> Olá, [Nome]! Tudo bem? Acabei de me candidatar à vaga de **Estágio de Dados e Negócios na Servfaz** e, como fiquei muito empolgado com o desafio de conectar dados e áreas de negócio, criei um case prático voltado para o setor de *facilities* e terceirização (analisando margem por contrato, impacto do absenteísmo em horas extras e glosas de SLA), com planilha em Excel, modelagem DAX/Power BI e dashboard interativo.
>
> Deixo o link caso queira dar uma olhada rápida: [SEU LINK DO DASHBOARD] (e código/Excel em [SEU LINK DO GITHUB]). Muito obrigado pela atenção!
