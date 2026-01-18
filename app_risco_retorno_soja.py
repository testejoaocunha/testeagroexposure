import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="Análise de Risco x Retorno - Soja",
    layout="wide",
    page_icon="🌱"
)

# ---------------- ESTILO PREMIUM ----------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: #FAFAFA;
}
div[data-testid="metric-container"] {
    background-color: #161B22;
    border-radius: 12px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TÍTULO ----------------
st.title("📊 Análise de Risco x Retorno – Soja")
st.caption("Simulação de margem, risco e breakeven da produção agrícola")

# ---------------- INPUTS ----------------
st.subheader("🔧 Parâmetros")

col1, col2, col3 = st.columns(3)

with col1:
    area = st.number_input("Área (ha)", value=2000.0)
    produtividade = st.number_input("Produtividade (sc/ha)", value=65.0)
    custo_ha = st.number_input("Custo por hectare (R$)", value=6200.0)

with col2:
    perc_comercializado = st.slider("% Comercializado", 0, 100, 30)
    preco_saca = st.number_input("Preço da Saca Vendida (R$)", value=108.0)

with col3:
    margem_desejada = st.slider("Margem Desejada (%)", 0, 40, 15)

# ---------------- CÁLCULOS ----------------
producao_total = area * produtividade
qtd_comercializada = producao_total * (perc_comercializado / 100)
qtd_a_vender = producao_total - qtd_comercializada

custo_total = area * custo_ha
receita_vendida = qtd_comercializada * preco_saca

exposicao = 100 - perc_comercializado

# Margem atual
if receita_vendida > 0:
    margem_atual = ((receita_vendida - (custo_total * (perc_comercializado / 100))) / custo_total) * 100
else:
    margem_atual = 0

gap_meta = margem_atual - margem_desejada

# Breakeven do saldo
receita_alvo_total = custo_total * (1 + margem_desejada / 100)
receita_necessaria_saldo = receita_alvo_total - receita_vendida

if qtd_a_vender > 0:
    preco_breakeven = receita_necessaria_saldo / qtd_a_vender
else:
    preco_breakeven = 0

# ---------------- MÉTRICAS ----------------
st.subheader("📌 Resultados")

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Produção Total (sc)", f"{producao_total:,.0f}")
m2.metric("Qtd. Comercializada (sc)", f"{qtd_comercializada:,.0f}")
m3.metric("Exposição (%)", f"{exposicao:.1f}%")
m4.metric("Margem Atual (%)", f"{margem_atual:.1f}%")
m5.metric("Gap vs Meta (%)", f"{gap_meta:.1f}%")

st.metric("Preço Breakeven do Saldo (R$/sc)", f"R$ {preco_breakeven:,.2f}")

# ---------------- GRÁFICO RISCO X RETORNO ----------------
st.subheader("📈 Gráfico Risco x Retorno")

fig_rr = go.Figure()

# Quadrantes
fig_rr.add_shape(type="rect", x0=0, x1=50, y0=margem_desejada, y1=40,
                 fillcolor="green", opacity=0.15, line_width=0)
fig_rr.add_shape(type="rect", x0=50, x1=100, y0=margem_desejada, y1=40,
                 fillcolor="yellow", opacity=0.15, line_width=0)
fig_rr.add_shape(type="rect", x0=0, x1=50, y0=0, y1=margem_desejada,
                 fillcolor="blue", opacity=0.15, line_width=0)
fig_rr.add_shape(type="rect", x0=50, x1=100, y0=0, y1=margem_desejada,
                 fillcolor="red", opacity=0.15, line_width=0)

# Ponto atual
fig_rr.add_trace(go.Scatter(
    x=[exposicao],
    y=[margem_atual],
    mode="markers",
    marker=dict(size=14, color="cyan"),
    name="Ponto Atual"
))

# Linhas
fig_rr.add_vline(x=exposicao, line_dash="dash", line_color="cyan")
fig_rr.add_hline(y=margem_desejada, line_dash="dash", line_color="white")

fig_rr.update_layout(
    xaxis_title="Exposição de Risco (%)",
    yaxis_title="Margem de Lucro (%)",
    xaxis=dict(range=[0, 100]),
    yaxis=dict(range=[0, 40]),
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig_rr, use_container_width=True)

# ---------------- SENSIBILIDADE ----------------
st.subheader("📉 Sensibilidade da Margem de Lucro")

precos = np.linspace(preco_saca * 0.7, preco_saca * 1.3, 12)
margens = []

for p in precos:
    receita_total = receita_vendida + (qtd_a_vender * p)
    margem = ((receita_total - custo_total) / custo_total) * 100
    margens.append(margem)

fig_sens = go.Figure()

fig_sens.add_trace(go.Scatter(
    x=precos,
    y=margens,
    mode="lines+markers",
    name="Margem (%)"
))

fig_sens.add_hline(y=margem_desejada, line_dash="dash", line_color="white")
fig_sens.add_vline(x=preco_saca, line_dash="dash", line_color="cyan")

fig_sens.update_layout(
    xaxis_title="Preço da Saca (R$)",
    yaxis_title="Margem de Lucro (%)",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig_sens, use_container_width=True)

st.caption("⚠️ Margem abaixo da meta com exposição elevada sugere avanço de comercialização ou hedge.")
