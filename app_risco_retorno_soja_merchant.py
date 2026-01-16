import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ---------------- CONFIG PAGE ----------------
st.set_page_config(
    page_title="Análise de Risco x Retorno – Soja",
    layout="wide"
)

# ---------------- SAFE PREMIUM STYLE ----------------
st.markdown("""
<style>
.block {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
}
.big {
    font-size: 34px;
    font-weight: 800;
}
.medium {
    font-size: 22px;
    font-weight: 600;
}
.footer {
    text-align: center;
    margin-top: 40px;
    color: #9CA3AF;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📊 Análise de Risco x Retorno – Soja")
st.caption("Versão Merchant / Trading Desk – Simulação de margem, risco e breakeven")

# ---------------- INPUTS ----------------
st.subheader("🔧 Parâmetros")

c1, c2, c3 = st.columns(3)

with c1:
    area = st.number_input("Área (ha)", 0.0, 100000.0, 2000.0)
    produtividade = st.number_input("Produtividade (sc/ha)", 0.0, 150.0, 65.0)
    custo_ha = st.number_input("Custo por hectare (R$)", 0.0, 20000.0, 6200.0)

with c2:
    perc_vendido = st.slider("% Comercializado", 0, 100, 67)
    preco_venda = st.number_input("Preço Médio Vendido (R$/sc)", 0.0, 300.0, 108.0)

with c3:
    margem_alvo = st.slider("Margem Desejada (%)", 0, 40, 15)

# ---------------- CALCULATIONS ----------------
producao = area * produtividade
vendido = producao * perc_vendido / 100
saldo = producao - vendido

custo_total = area * custo_ha
receita_vendida = vendido * preco_venda

receita_alvo = custo_total * (1 + margem_alvo / 100)
receita_faltante = receita_alvo - receita_vendida

preco_breakeven = receita_faltante / saldo if saldo > 0 else 0

receita_total = receita_vendida + saldo * preco_venda
margem_atual = ((receita_total - custo_total) / custo_total) * 100
gap = margem_atual - margem_alvo
exposicao = 100 - perc_vendido

# ---------------- KPIs ----------------
st.subheader("📌 Resultados")

k1, k2, k3, k4, k5 = st.columns(5)

k1.markdown(f"<div class='block'><div class='medium'>Produção Total</div><div class='big'>{producao:,.0f} sc</div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='block'><div class='medium'>Qtd. Vendida</div><div class='big'>{vendido:,.0f} sc</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='block'><div class='medium'>Exposição</div><div class='big'>{exposicao:.1f}%</div></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='block'><div class='medium'>Margem Atual</div><div class='big'>{margem_atual:.1f}%</div></div>", unsafe_allow_html=True)
k5.markdown(f"<div class='block'><div class='medium'>Gap vs Meta</div><div class='big'>{gap:.1f}%</div></div>", unsafe_allow_html=True)

# ---------------- BREAKEVEN HIGHLIGHT ----------------
cor = "#16A34A" if preco_breakeven <= preco_venda else "#DC2626"

st.markdown(
    f"""
    <div class='block'>
        <div class='medium'>Preço Breakeven do Saldo</div>
        <div class='big' style='color:{cor};'>R$ {preco_breakeven:,.2f} / sc</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- IA SUGGESTION ----------------
st.subheader("🤖 Sugestão Inteligente")

sugestao_venda = round(min(100, max(perc_vendido, perc_vendido + abs(gap) * 1.5)), 1)

st.info(
    f"""
    **Sugestão da IA:**  
    Para atingir a margem alvo de **{margem_alvo}%**, recomenda-se elevar a posição vendida
    para aproximadamente **{sugestao_venda}% da produção**, reduzindo a exposição ao risco
    e aumentando previsibilidade de margem.
    """
)

# ---------------- CHART ----------------
st.subheader("📈 Risco x Retorno")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[exposicao],
    y=[margem_atual],
    mode="markers",
    marker=dict(size=16, color="cyan"),
    name="Posição Atual"
))

fig.add_hline(y=margem_alvo, line_dash="dash", line_color="white")
fig.add_vline(x=exposicao, line_dash="dash", line_color="cyan")

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Exposição (%)",
    yaxis_title="Margem (%)",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("<div class='footer'>Versão em Teste – João Cunha</div>", unsafe_allow_html=True)
