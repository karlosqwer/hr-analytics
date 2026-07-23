from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="PeoplePulse | HR Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "navy": "#07111F",
    "blue": "#3767F0",
    "cyan": "#24C8DB",
    "green": "#34D399",
    "orange": "#F59E0B",
    "red": "#FB7185",
    "muted": "#8B9BB4",
    "grid": "rgba(139,155,180,.14)",
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {font-family: 'DM Sans', sans-serif;}
    .stApp {background: #07111F;}
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1B2A 0%, #091522 100%);
        border-right: 1px solid rgba(255,255,255,.07);
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {color:#D8E2F0;}
    [data-testid="stHeader"] {background: rgba(7,17,31,.82);}
    .block-container {padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1500px;}
    .brand {display:flex; align-items:center; gap:12px; margin-bottom:28px;}
    .brand-mark {
        width:38px; height:38px; display:grid; place-items:center; border-radius:11px;
        color:white; font-weight:800; font-size:20px;
        background:linear-gradient(135deg,#3767F0,#24C8DB);
        box-shadow:0 8px 24px rgba(55,103,240,.35);
    }
    .brand-name {font-size:19px;font-weight:700;color:#F4F7FB;line-height:1;}
    .brand-sub {font-size:11px;color:#7F91AA;margin-top:5px;letter-spacing:.12em;}
    .eyebrow {color:#24C8DB;font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;}
    .hero-title {font-size:34px;font-weight:700;color:#F8FAFC;line-height:1.2;margin:7px 0 5px;}
    .hero-copy {color:#8B9BB4;font-size:15px;margin-bottom:19px;}
    .live-pill {
        display:inline-flex;align-items:center;gap:7px;border:1px solid rgba(52,211,153,.22);
        background:rgba(52,211,153,.08);color:#7CE7BD;border-radius:999px;
        padding:6px 10px;font-size:11px;font-weight:600;
    }
    .live-dot {width:7px;height:7px;border-radius:50%;background:#34D399;box-shadow:0 0 10px #34D399;}
    .metric-card {
        background:linear-gradient(145deg,rgba(19,38,59,.96),rgba(12,27,43,.96));
        border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:19px 20px 17px;
        min-height:126px;box-shadow:0 13px 35px rgba(0,0,0,.16);
    }
    .metric-top {display:flex;justify-content:space-between;align-items:center;}
    .metric-label {color:#91A1B8;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;}
    .metric-icon {width:31px;height:31px;display:grid;place-items:center;border-radius:9px;background:rgba(55,103,240,.14);color:#78A0FF;}
    .metric-value {color:#F8FAFC;font-size:27px;font-weight:700;margin-top:11px;line-height:1;}
    .metric-foot {color:#6F829E;font-size:11px;margin-top:10px;}
    .positive {color:#52D9A4;font-weight:600;}
    .section-title {color:#EDF3FA;font-size:18px;font-weight:700;margin:8px 0 1px;}
    .section-copy {color:#71839D;font-size:12px;margin-bottom:11px;}
    div[data-testid="stPlotlyChart"] {
        border:1px solid rgba(255,255,255,.065);border-radius:16px;overflow:hidden;
        box-shadow:0 12px 30px rgba(0,0,0,.12);
    }
    div[data-testid="stDataFrame"] {border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden;}
    .stTabs [data-baseweb="tab-list"] {gap:24px;border-bottom:1px solid rgba(255,255,255,.08);}
    .stTabs [data-baseweb="tab"] {color:#8091AA;font-weight:600;}
    .stTabs [aria-selected="true"] {color:#EAF1FB;}
    hr {border-color:rgba(255,255,255,.07);}
    #MainMenu, footer {visibility:hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_dados():
    funcionarios = pd.read_csv(
        DATA_DIR / "funcionarios.csv",
        parse_dates=["data_nascimento", "data_admissao", "data_desligamento"],
    )
    departamentos = pd.read_csv(DATA_DIR / "departamentos.csv")
    cargos = pd.read_csv(DATA_DIR / "cargos.csv")
    presencas = pd.read_csv(DATA_DIR / "presencas.csv", parse_dates=["data_registro"])
    avaliacoes = pd.read_csv(DATA_DIR / "avaliacoes.csv", parse_dates=["data_avaliacao"])
    funcionarios = (
        funcionarios.merge(departamentos, on="id_departamento")
        .merge(cargos[["id_cargo", "nome_cargo", "nivel", "salario_base"]], on="id_cargo")
    )
    return funcionarios, presencas, avaliacoes


def estilizar(fig, altura=365):
    fig.update_layout(
        height=altura,
        margin=dict(l=22, r=22, t=58, b=20),
        paper_bgcolor="#0C1B2B",
        plot_bgcolor="#0C1B2B",
        font=dict(family="DM Sans", color="#91A1B8", size=12),
        title=dict(font=dict(color="#F2F6FB", size=16), x=0.035, y=0.94),
        legend=dict(orientation="h", y=1.09, x=0.58, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#13283D", font_color="#F8FAFC", bordercolor="#28425E"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=COLORS["grid"])
    fig.update_yaxes(gridcolor=COLORS["grid"], zeroline=False)
    return fig


def cartao(label, value, foot, icon, positive=False):
    classe = "positive" if positive else ""
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-top"><span class="metric-label">{label}</span><span class="metric-icon">{icon}</span></div>
          <div class="metric-value">{value}</div>
          <div class="metric-foot {classe}">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


funcionarios, presencas, avaliacoes = carregar_dados()

with st.sidebar:
    st.markdown(
        """<div class="brand"><div class="brand-mark">P</div><div>
        <div class="brand-name">PeoplePulse</div><div class="brand-sub">WORKFORCE INTELLIGENCE</div>
        </div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("##### Filtros do painel")
    departamentos = sorted(funcionarios["nome_departamento"].unique())
    selecionados = st.multiselect(
        "Departamentos", departamentos, default=departamentos,
        placeholder="Selecione os departamentos",
    )
    status = st.segmented_control(
        "Vínculo", ["Todos", "Ativo", "Desligado"], default="Todos",
    )
    st.markdown("---")
    st.caption("Período de referência")
    st.markdown("**01 jan — 31 dez 2025**")
    st.markdown(
        '<div style="margin-top:18px"><span class="live-pill"><span class="live-dot"></span> DADOS ATUALIZADOS</span></div>',
        unsafe_allow_html=True,
    )

if not selecionados:
    st.warning("Selecione pelo menos um departamento para visualizar o painel.")
    st.stop()

filtrados = funcionarios[funcionarios["nome_departamento"].isin(selecionados)].copy()
if status != "Todos":
    filtrados = filtrados[filtrados["status_funcionario"] == status]
ids = filtrados["id_funcionario"]
presencas_f = presencas[presencas["id_funcionario"].isin(ids)]
avaliacoes_f = avaliacoes[avaliacoes["id_funcionario"].isin(ids)]
ativos = filtrados[filtrados["status_funcionario"] == "Ativo"]

st.markdown('<div class="eyebrow">Visão executiva</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">People Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-copy">Decisões sobre pessoas guiadas por indicadores claros, consistentes e acionáveis.</div>',
    unsafe_allow_html=True,
)

headcount = len(ativos)
folha = ativos["salario"].sum()
ausencias = presencas_f["status_presenca"].isin(["Falta", "Atestado"]).mean() * 100
nota_media = avaliacoes_f["nota_final"].mean()
turnover = (
    filtrados["data_desligamento"].between("2025-01-01", "2025-12-31").sum()
    / max((len(filtrados) + headcount) / 2, 1) * 100
)

cols = st.columns(5)
metricas = [
    ("Headcount ativo", f"{headcount:,}".replace(",", "."), "força de trabalho atual", "◎", False),
    ("Folha mensal", f"R$ {folha/1_000:.1f} mil".replace(".", ","), "salários dos ativos", "◇", False),
    ("Absenteísmo", f"{ausencias:.1f}%".replace(".", ","), "faltas + atestados", "◌", ausencias < 7),
    ("Desempenho", f"{nota_media:.1f}".replace(".", ","), "média em uma escala de 10", "↗", nota_media >= 7),
    ("Turnover 2025", f"{turnover:.1f}%".replace(".", ","), "desligamentos no período", "⇄", turnover < 15),
]
for col, metrica in zip(cols, metricas):
    with col:
        cartao(*metrica)

st.write("")
tab1, tab2, tab3 = st.tabs(["Visão geral", "Pessoas & remuneração", "Detalhamento"])

with tab1:
    col_a, col_b = st.columns([1.35, 1])
    with col_a:
        hc_depto = ativos.groupby("nome_departamento", as_index=False).size().sort_values("size")
        fig = px.bar(
            hc_depto, x="size", y="nome_departamento", orientation="h",
            color_discrete_sequence=[COLORS["blue"]], text="size",
            title="Distribuição do headcount",
            labels={"size": "Pessoas", "nome_departamento": ""},
        )
        fig.update_traces(textposition="outside", marker_cornerradius=5)
        estilizar(fig)
        st.plotly_chart(fig, width="stretch")

    with col_b:
        pres = presencas_f["status_presenca"].value_counts().reset_index()
        fig = px.pie(
            pres, values="count", names="status_presenca", hole=.68,
            color_discrete_sequence=[COLORS["blue"], COLORS["cyan"], COLORS["orange"], COLORS["green"], COLORS["red"]],
            title="Composição de presença",
        )
        fig.update_traces(textinfo="percent", textfont_size=11)
        fig.add_annotation(text=f"<b>{len(presencas_f):,.0f}</b><br><span style='font-size:11px'>registros</span>",
                           showarrow=False, font=dict(color="#F8FAFC", size=18))
        estilizar(fig)
        st.plotly_chart(fig, width="stretch")

    aval = (
        avaliacoes_f.merge(filtrados[["id_funcionario", "nome_departamento"]], on="id_funcionario")
        .groupby(["data_avaliacao", "nome_departamento"], as_index=False)["nota_final"].mean()
    )
    fig = px.line(
        aval, x="data_avaliacao", y="nota_final", color="nome_departamento",
        markers=True, title="Evolução do desempenho por departamento",
        labels={"data_avaliacao": "", "nota_final": "Nota média", "nome_departamento": ""},
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_yaxes(range=[5, 9.5])
    estilizar(fig, 385)
    st.plotly_chart(fig, width="stretch")

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        salario = ativos.groupby("nome_departamento", as_index=False)["salario"].mean().sort_values("salario")
        fig = px.bar(
            salario, x="salario", y="nome_departamento", orientation="h",
            title="Salário médio por departamento",
            labels={"salario": "Salário médio (R$)", "nome_departamento": ""},
            color_discrete_sequence=[COLORS["cyan"]],
        )
        fig.update_traces(marker_cornerradius=5)
        estilizar(fig)
        st.plotly_chart(fig, width="stretch")
    with col_b:
        sexo = ativos["sexo"].value_counts().reset_index()
        fig = px.pie(
            sexo, values="count", names="sexo", hole=.58,
            title="Diversidade de gênero",
            color_discrete_sequence=[COLORS["blue"], COLORS["cyan"], COLORS["orange"]],
        )
        estilizar(fig)
        st.plotly_chart(fig, width="stretch")

    faixa = pd.cut(
        ativos["salario"], bins=[0, 4000, 7000, 10000, 15000, float("inf")],
        labels=["Até 4k", "4k–7k", "7k–10k", "10k–15k", "Acima de 15k"],
    ).value_counts(sort=False)
    fig = go.Figure(go.Bar(
        x=faixa.index.astype(str), y=faixa.values,
        marker=dict(color=[COLORS["blue"], "#4E7AF2", "#5F8DF5", COLORS["cyan"], COLORS["green"]]),
        text=faixa.values, textposition="outside",
    ))
    fig.update_layout(title="Distribuição por faixa salarial", xaxis_title="", yaxis_title="Pessoas")
    estilizar(fig, 340)
    st.plotly_chart(fig, width="stretch")

with tab3:
    st.markdown('<div class="section-title">Base de colaboradores</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Consulte os registros utilizados nos indicadores do painel.</div>',
        unsafe_allow_html=True,
    )
    tabela = filtrados[[
        "nome_completo", "nome_departamento", "nome_cargo", "nivel",
        "cidade", "estado", "salario", "data_admissao", "status_funcionario",
    ]].sort_values("nome_completo").rename(columns={
        "nome_completo": "Colaborador", "nome_departamento": "Departamento",
        "nome_cargo": "Cargo", "nivel": "Nível", "cidade": "Cidade",
        "estado": "UF", "salario": "Salário", "data_admissao": "Admissão",
        "status_funcionario": "Status",
    })
    st.dataframe(
        tabela,
        width="stretch",
        hide_index=True,
        height=530,
        column_config={
            "Salário": st.column_config.NumberColumn(format="R$ %.2f"),
            "Admissão": st.column_config.DateColumn(format="DD/MM/YYYY"),
        },
    )
    st.download_button(
        "Baixar dados filtrados (.csv)",
        tabela.to_csv(index=False).encode("utf-8-sig"),
        "people_analytics_filtrado.csv",
        "text/csv",
    )

st.markdown(
    '<div style="text-align:center;color:#50647F;font-size:11px;margin-top:32px">'
    'PeoplePulse • Dados sintéticos para demonstração de competências em People Analytics</div>',
    unsafe_allow_html=True,
)
