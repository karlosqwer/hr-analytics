<div align="center">

# PeoplePulse — HR Analytics

### Do dado bruto à decisão de pessoas

Dashboard executivo de People Analytics desenvolvido para transformar dados de
RH em indicadores claros sobre força de trabalho, desempenho, presença,
turnover e remuneração.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Data_Model-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

</div>

---

## Sobre o projeto

O PeoplePulse simula um desafio real de uma área de RH: informações relevantes
estão espalhadas entre cadastros, movimentações, salários, frequência e
avaliações. O projeto organiza essas fontes em um modelo relacional, cria uma
base sintética reprodutível e entrega uma visão executiva para apoiar decisões.

Mais do que exibir gráficos, o painel responde perguntas de negócio:

- Qual é o headcount atual e como ele está distribuído?
- Quanto representa a folha salarial mensal?
- Quais áreas concentram maior absenteísmo e turnover?
- Como o desempenho evolui entre os departamentos?
- Há diferenças relevantes de remuneração e diversidade?
- Quais colaboradores exigem uma análise mais detalhada?

## Resultado

| Dimensão | Volume |
|---|---:|
| Colaboradores | 500 |
| Departamentos | 8 |
| Cargos | 45 |
| Registros de presença | 107.750 |
| Avaliações de desempenho | 1.542 |

O dashboard oferece filtros globais, cinco KPIs executivos, análise de
headcount, composição de presença, evolução do desempenho, salários,
diversidade, consulta detalhada e exportação dos dados filtrados.

## Principais indicadores

| Indicador | Regra de negócio |
|---|---|
| Headcount ativo | Colaboradores com vínculo ativo na data de referência |
| Folha mensal | Soma dos salários dos colaboradores ativos |
| Absenteísmo | Faltas e atestados ÷ registros de presença |
| Desempenho | Média das avaliações dos colaboradores selecionados |
| Turnover | Desligamentos no período ÷ headcount médio aproximado |

## Arquitetura

```text
Geração sintética (Faker + Pandas)
             │
             ▼
         Arquivos CSV
             │
      ┌──────┴────────┐
      ▼               ▼
Modelo MySQL      Dashboard Streamlit
      │               │
      ▼               ▼
Consultas SQL     KPIs + Plotly + filtros
```

```text
hr-analytics/
├── dashboard/
│   └── app.py
├── data/
│   ├── departamentos.csv
│   ├── cargos.csv
│   ├── funcionarios.csv
│   ├── presencas.csv
│   └── avaliacoes.csv
├── database/
│   ├── 01_create_database.sql
│   ├── 02_insert_data.sql
│   └── 03_business_queries.sql
├── python/
│   └── generate_data.py
├── requirements.txt
└── README.md
```

## Competências demonstradas

- modelagem relacional e integridade referencial em MySQL;
- definição e tradução de métricas de negócio;
- geração e validação de dados sintéticos;
- tratamento e análise de dados com Pandas;
- storytelling e visualização com Plotly;
- desenvolvimento de dashboard interativo com Streamlit;
- documentação técnica orientada ao contexto de negócio.

## Como executar

### 1. Prepare o ambiente

```bash
git clone https://github.com/karlosqwer/hr-analytics.git
cd hr-analytics
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

No Linux ou macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Gere novamente a base

```bash
python python/generate_data.py
```

O gerador utiliza seed fixa (`42`), portanto a base é reprodutível.

### 3. Abra o dashboard

```bash
streamlit run dashboard/app.py
```

Acesse `http://localhost:8501`.

### 4. Opcional: carregue o MySQL

Requer MySQL 8+ com `local_infile` habilitado.

```bash
mysql --local-infile=1 -u root -p < database/01_create_database.sql
mysql --local-infile=1 -u root -p hr_analytics < database/02_insert_data.sql
```

Depois, explore as análises em `database/03_business_queries.sql`.

## Decisões de projeto

- **Dados sintéticos:** nenhuma informação pessoal real é utilizada.
- **Seed fixa:** garante resultados reproduzíveis durante testes e entrevistas.
- **Camadas separadas:** geração, armazenamento, análise e visualização podem
  evoluir de forma independente.
- **Filtros globais:** todas as visualizações refletem o mesmo recorte.
- **SQL analítico:** as consultas documentam as regras além do dashboard.

## Possíveis evoluções

- pipeline automatizado de atualização;
- autenticação e perfis de acesso;
- previsão de turnover com machine learning;
- testes unitários das regras de negócio;
- deploy público com integração a banco gerenciado.

## Ética e privacidade

Todos os nomes e registros são fictícios. O projeto foi criado exclusivamente
para estudo e demonstração técnica. Métricas de pessoas devem sempre ser
interpretadas com contexto, transparência e revisão humana.

---

<div align="center">
Desenvolvido como projeto de portfólio em Data Analytics e People Analytics.
</div>
