import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard Autoescola",
    layout="wide"
)

# Título
st.title("Dashboard – Plataforma de Instrutores de Direção")

# Leitura dos dados
dados = pd.read_csv(
    "Autoescola_Aulas.csv",
    sep=";",
    encoding="utf-8"
)

dados.columns = dados.columns.str.strip()

# ====================
# KPIs
# ====================

total_aulas = dados["Quantidade_Aulas"].sum()

total_alunos = dados["Aluno"].nunique()

media_satisfacao = dados["Avaliacao"].mean()

cidade_lider = (
    dados.groupby("Cidade")["Quantidade_Aulas"]
    .sum()
    .idxmax()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total de Aulas Realizadas",
        total_aulas
    )

with col2:
    st.metric(
        "Total de Alunos Cadastrados",
        total_alunos
    )

with col3:
    st.metric(
    "Média Geral de Satisfação",
f"{media_satisfacao:.2f} / 5")

with col4:
    st.metric(
        "Cidade com Maior Demanda",
        cidade_lider
    )

# ====================
# Quantidade de Aulas por Instrutor
# ====================

st.subheader("Instrutores com Maior Volume de Aulas")

aulas_instrutor = (
    dados.groupby("Instrutor")["Quantidade_Aulas"]
    .sum()
    .reset_index()
    .sort_values(
        by="Quantidade_Aulas",
        ascending=True
    )
)

fig_instrutor = px.bar(
    aulas_instrutor,
    x="Quantidade_Aulas",
    y="Instrutor",
    orientation="h",
    text="Quantidade_Aulas"
)

fig_instrutor.update_layout(
    yaxis_title="",
    xaxis_title="Quantidade de Aulas"
)

st.plotly_chart(
    fig_instrutor,
    width="stretch"
)

# ====================
# Evolução Mensal das Aulas
# ====================

st.subheader("Evolução Mensal das Aulas")

aulas_mes = (
    dados.groupby("Mes")["Quantidade_Aulas"]
    .sum()
    .reset_index()
)

ordem_meses = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

aulas_mes["Mes"] = pd.Categorical(
    aulas_mes["Mes"],
    categories=ordem_meses,
    ordered=True
)

aulas_mes = aulas_mes.sort_values("Mes")

fig_mes = px.line(
    aulas_mes,
    x="Mes",
    y="Quantidade_Aulas",
    markers=True,
    text="Quantidade_Aulas"
)

fig_mes.update_traces(
    textposition="top center"
)

fig_mes.update_layout(
    xaxis_title="Mês",
    yaxis_title="Quantidade de Aulas"
)

st.plotly_chart(
    fig_mes,
    width="stretch"
)

# ====================
# Quantidade de Aulas por Cidade
# ====================

st.subheader("Demanda por Cidade")

aulas_cidade = (
    dados.groupby("Cidade")["Quantidade_Aulas"]
    .sum()
    .reset_index()
    .sort_values(
        by="Quantidade_Aulas",
        ascending=False
    )
)

fig_cidade = px.bar(
    aulas_cidade,
    x="Cidade",
    y="Quantidade_Aulas",
    text="Quantidade_Aulas",
    color_discrete_sequence=["#1f77b4"]
)

fig_cidade.update_traces(
    textposition="outside"
)

fig_cidade.update_layout(
    xaxis_title="Cidade",
    yaxis_title="Quantidade de Aulas"
)

st.plotly_chart(
    fig_cidade,
    width="stretch"
)

# ====================
# Desempenho dos Instrutores
# ====================

st.subheader("Desempenho dos Instrutores")

avaliacao_instrutor = (
    dados.groupby("Instrutor")["Avaliacao"]
    .mean()
    .round(2)
    .reset_index()
    .sort_values(
        by="Avaliacao",
        ascending=True
    )
)

fig_desempenho = px.bar(
    avaliacao_instrutor,
    x="Avaliacao",
    y="Instrutor",
    orientation="h",
    text="Avaliacao",
    color_discrete_sequence=["#2E8B57"]
)


fig_desempenho.update_layout(
    xaxis_title="Média de Avaliação",
    yaxis_title="",
    )

st.plotly_chart(
    fig_desempenho,
    width="stretch"
)

# ====================
# Satisfação dos Alunos
# ====================

st.subheader("Satisfação dos Alunos")

perfil_satisfacao = (
    dados["Perfil"]
    .value_counts()
    .reset_index()
)

perfil_satisfacao.columns = [
    "Perfil",
    "Quantidade"
]

fig_satisfacao = px.pie(
    perfil_satisfacao,
    names="Perfil",
    values="Quantidade",
    hole=0.5
)

st.plotly_chart(
    fig_satisfacao,
    width="stretch"
)