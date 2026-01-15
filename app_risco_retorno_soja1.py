import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from datetime import datetime, date

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="AgroExposure | Intelligence Pro",
    layout="wide",
    page_icon="🌱"
)

# ---------------- ESTILO CSS PREMIUM ----------------
st.markdown("""
<style>
    /* GERAL */
    .stApp { background-color: #F8F9FA; color: #31333F; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] .block-container { padding-top: 1rem !important; padding-bottom: 2rem; }
    div[data-baseweb="input"] { background-color: #FFFFFF !important; border: 1px solid #CFD8DC !important; border-radius: 6px !important; }
    
    /* CARDS DE MÉTRICAS */
    div[data-testid="metric-container"] {
        background-color: #EFF3F6; 
        border: 1px solid #D1D5DB; 
        border-left: 5px solid #2E7D32; 
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px); 
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* TABELAS */
    .dataframe { font-size: 14px !important; font-family: 'Source Sans Pro', sans-serif; }
    
    /* RODAPÉ */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%; background-color: #FFFFFF;
        color: #90A4AE; text-align: center; padding: 8px; border-top: 1px solid #EEEEEE; font-size: 12px; z-index: 100;
    }
    .block-container { padding-bottom: 60px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 1. BARRA LATERAL (INPUTS)
# ==============================================================================
with st.sidebar:
    caminho_logo = "assets/logo.png"
    if os.path.exists(caminho_logo):
        st.image(caminho_logo, use_container_width=True)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)

    st.markdown("<h3 style='margin-top: 5px;'>⚙️ Parâmetros da Safra</h3>", unsafe_allow_html=True)
    
    # 1. Produção
    st.markdown("<p style='color:#2E7D32; font-weight:bold; margin-top:10px;'>1. Produção e Custo Operacional</p>", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        area_propria = st.number_input("Área Própria (ha)", value=2500, step=0)
    with col_a2:
        area_arrendada = st.number_input("Área Arrendada (ha)", value=500, step=0)
    
    area_total = area_propria + area_arrendada
    st.caption(f"📍 Área Plantada Total: **{area_total:,.0f} ha**")

    produtividade = st.number_input("Produtividade Est. (sc/ha)", value=65.0, step=1.0)
    producao_total = area_total * produtividade
    
    custo_ha_operacional = st.number_input("Custo Operacional (R$/ha)", value=6000.0, step=100.0)
    
    # 2. Comercialização
    st.markdown("<hr style='margin: 10px 0;'><p style='color:#2E7D32; font-weight:bold;'>2. Comercialização</p>", unsafe_allow_html=True)
    perc_comercializado = st.slider("% Já Travado (Hedge)", 0, 100, 30)
    
    vol_hedge = producao_total * (perc_comercializado/100)
    st.caption(f"📦 Volume Travado: {vol_hedge:,.0f} sc")
    
    preco_medio_venda = st.number_input("Preço Médio Travado (R$/sc)", value=111.0, step=0.5)
    
    # 3. Mercado
    st.markdown("<hr style='margin: 10px 0;'><p style='color:#2E7D32; font-weight:bold;'>3. Metas e Mercado</p>", unsafe_allow_html=True)
    preco_mercado = st.number_input("Preço Balcão/Spot (R$/sc)", value=105.0, step=0.5)
    margem_desejada = st.slider("Margem Alvo (%)", 0, 50, 20)

    # 4. Custeio
    st.markdown("<hr style='margin: 10px 0;'><p style='color:#2E7D32; font-weight:bold;'>4. Custeio (Financ. & Arrend.)</p>", unsafe_allow_html=True)
    
    perc_financiado = st.number_input("% Custeio Financiado", value=30.0, step=5.0)
    taxa_juros_ano = st.number_input("Taxa de Juros ao Ano (%)", value=8.0, step=0.5)
    col_d1, col_d2 = st.columns(2)
    data_desembolso = col_d1.date_input("Desembolso", value=date(2025, 8, 10))
    data_pagamento = col_d2.date_input("Pagamento", value=date(2026, 4, 30))
    
    st.markdown("<div style='margin-top:5px; font-weight:bold; font-size:12px; color:#555;'>Custo do Arrendamento</div>", unsafe_allow_html=True)
    arrendamento_sc_ha = st.number_input("Pagamento (sc/ha)", value=15.0, step=0.5)
    st.caption(f"Ref. Área Arrendada: {area_arrendada:,.0f} ha")

# ==============================================================================
# 2. CÁLCULOS PRINCIPAIS (CORE)
# ==============================================================================

# A. Cálculos Físicos
vol_arrendamento_sacas = area_arrendada * arrendamento_sc_ha
producao_liquida_sacas = producao_total - vol_arrendamento_sacas 

# B. Receitas
qtd_vendida = producao_total * (perc_comercializado / 100)
receita_hedge = qtd_vendida * preco_medio_venda
qtd_aberta = producao_total - qtd_vendida
receita_spot = qtd_aberta * preco_mercado
receita_bruta_total = receita_hedge + receita_spot
preco_medio_ponderado = receita_bruta_total / producao_total if producao_total > 0 else 0

# C. Custos
custo_operacional_total = area_total * custo_ha_operacional

valor_base_financiamento = custo_operacional_total * (perc_financiado / 100)
dias_financiamento = (data_pagamento - data_desembolso).days
dias_financiamento = max(0, dias_financiamento)
custo_financeiro_juros = valor_base_financiamento * ((taxa_juros_ano / 100) / 365) * dias_financiamento

custo_arrendamento_reais = vol_arrendamento_sacas * preco_mercado

custo_total_safra = custo_operacional_total + custo_financeiro_juros + custo_arrendamento_reais

# D. Resultados
lucro_operacional = receita_bruta_total - custo_operacional_total 
fluxo_caixa_operacional = lucro_operacional - custo_financeiro_juros 
lucro_liquido = receita_bruta_total - custo_total_safra
margem_liquida_perc = (lucro_liquido / receita_bruta_total) * 100 if receita_bruta_total > 0 else 0

# E. KPIs Avançados (Breakeven)
breakeven_sc_total = custo_total_safra / preco_medio_ponderado if preco_medio_ponderado > 0 else 0
breakeven_sc_ha = breakeven_sc_total / area_total
margem_seguranca_sc_ha = produtividade - breakeven_sc_ha

custo_sc_liquida = custo_total_safra / producao_liquida_sacas if producao_liquida_sacas > 0 else 0

receita_alvo_total = custo_total_safra * (1 + margem_desejada / 100)
receita_faltante = receita_alvo_total - receita_hedge
preco_breakeven_saldo = receita_faltante / qtd_aberta if qtd_aberta > 0 else 0

# NOVOS KPIs ESPECÍFICOS (CÁLCULOS EXTRAS)
custo_ha_medio_op_fin = (custo_operacional_total + custo_financeiro_juros) / area_total
custo_ha_area_arrendada = custo_ha_medio_op_fin + (arrendamento_sc_ha * preco_mercado)
custo_ha_area_propria = custo_ha_medio_op_fin # Na própria não tem custo terra

juros_por_saca_reais = custo_financeiro_juros / producao_total
juros_por_saca_fisico = custo_financeiro_juros / preco_medio_ponderado if preco_medio_ponderado > 0 else 0

breakeven_sc_ha_spot = (custo_total_safra / preco_mercado) / area_total 

# ==============================================================================
# 3. INTERFACE DASHBOARD
# ==============================================================================
st.title("📊 AgroExposure: Painel de Decisão Estratégica") 

# --- KPIs SUPERIORES ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🚜 Produção Líquida", f"{producao_liquida_sacas:,.0f} sc", delta=f"Total: {producao_total:,.0f} sc", help="Produção Total menos Pagamento de Arrendamento em produto")
with c2:
    st.metric("📉 Custo Real (Liq)", f"R$ {custo_sc_liquida:,.2f} /sc", delta="Op + Juros + Arr", delta_color="inverse", help="Custo Total dividido pelas sacas líquidas (que sobram)")
with c3:
    st.metric("🛑 Ponto de Equilíbrio", f"{breakeven_sc_ha:,.1f} sc/ha", delta=f"Margem: {margem_seguranca_sc_ha:.1f} sc/ha", delta_color="normal", help="Quanto você precisa colher para pagar TUDO (0x0)")
with c4:
    lbl_delta = "Venda Favorável" if preco_breakeven_saldo < preco_mercado else "Preço Abaixo da Meta"
    st.metric("🎯 Preço Alvo Saldo", f"R$ {preco_breakeven_saldo:,.2f}", delta=lbl_delta, delta_color="inverse")

st.markdown("---")

# --- SIMULADOR WHAT-IF ---
with st.expander("⚖️ Simulador de Negociação (What-If)", expanded=False):
    st.markdown("#### Simule impacto na Margem Global")
    col_s1, col_s2, col_s3 = st.columns([1,1,2])
    with col_s1:
        st.info(f"Travado: {perc_comercializado}% a R$ {preco_medio_venda}")
    with col_s2:
        n_perc = st.number_input("Nova Venda (%)", 0, 100, 10)
        n_preco = st.number_input("Preço (R$)", value=preco_mercado)
    with col_s3:
        q_nova = producao_total * (n_perc/100)
        rec_sim = receita_hedge + (q_nova * n_preco) + ((qtd_aberta - q_nova) * preco_mercado)
        lucro_sim = rec_sim - custo_total_safra
        margem_sim = (lucro_sim/rec_sim)*100
        delta_m = margem_sim - margem_liquida_perc
        st.metric("Nova Margem", f"{margem_sim:.2f}%", delta=f"{delta_m:+.2f}%")

st.markdown("---")

# --- GRÁFICOS (RISCO E PREÇO) ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎯 Matriz de Risco")
    exposicao_perc = 100 - perc_comercializado
    fig_rr = go.Figure()
    fig_rr.add_shape(type="rect", x0=50, x1=100, y0=-20, y1=margem_desejada, fillcolor="rgba(255, 0, 0, 0.1)", line_width=0)
    fig_rr.add_shape(type="rect", x0=50, x1=100, y0=margem_desejada, y1=60, fillcolor="rgba(255, 215, 0, 0.15)", line_width=0)
    fig_rr.add_shape(type="rect", x0=0, x1=50, y0=-20, y1=margem_desejada, fillcolor="rgba(0, 0, 255, 0.05)", line_width=0)
    fig_rr.add_shape(type="rect", x0=0, x1=50, y0=margem_desejada, y1=60, fillcolor="rgba(0, 128, 0, 0.1)", line_width=0)
    fig_rr.add_trace(go.Scatter(x=[exposicao_perc], y=[margem_liquida_perc], mode='markers+text',
        marker=dict(size=22, color='#2E7D32', line=dict(width=2, color='white')),
        text=["VOCÊ"], textposition="top center", textfont=dict(color='#1B5E20', size=14, family="Arial Black")))
    fig_rr.update_layout(xaxis_title="Exposição Spot (%)", yaxis_title="Margem Líquida (%)",
        xaxis=dict(range=[0, 100]), yaxis=dict(range=[-10, 50]), height=350, template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_rr, use_container_width=True)

with col_right:
    st.subheader("📉 Sensibilidade (Preço)")
    range_precos = np.linspace(preco_mercado * 0.75, preco_mercado * 1.25, 20)
    margens_sim = []
    for p in range_precos:
        rec_sim = receita_hedge + (qtd_aberta * p)
        custo_arr_sim = vol_arrendamento_sacas * p 
        custo_tot_sim = custo_operacional_total + custo_financeiro_juros + custo_arr_sim
        m = ((rec_sim - custo_tot_sim) / rec_sim) * 100
        margens_sim.append(m)
        
    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(x=range_precos, y=margens_sim, mode='lines', line=dict(color='#1565C0', width=4), name='Margem'))
    fig_sens.add_hline(y=margem_desejada, line_dash="dot", line_color="green", annotation_text="Meta")
    fig_sens.add_vline(x=preco_breakeven_saldo, line_dash="dash", line_color="#FF9800", annotation_text=f"Alvo: {preco_breakeven_saldo:.1f}")
    fig_sens.update_layout(xaxis_title="Preço Soja (R$)", yaxis_title="Margem Líquida (%)", height=350, template="plotly_white")
    st.plotly_chart(fig_sens, use_container_width=True)

# --- DRE GERENCIAL ---
st.markdown("### 📋 DRE Gerencial de Decisão (Visão Econômica)")

with st.expander("Ver Análise Vertical Detalhada (R$/ha e sc/ha)", expanded=True):
    # Construção dos Dados do DRE
    dados_dre_pro = [
        # GRUPO DE RECEITA
        {
            "Grupo": "1. RECEITA BRUTA",
            "Descrição": f"Venda Total ({produtividade} sc/ha x Preço Médio R$ {preco_medio_ponderado:.2f})",
            "Valor Total (R$)": receita_bruta_total,
            "Indicador (R$/ha)": receita_bruta_total / area_total,
            "Eqv. (sc/ha)": produtividade
        },
        # GRUPO CUSTO OPERACIONAL
        {
            "Grupo": "2. (-) CUSTO OPERACIONAL",
            "Descrição": f"Custo aplicado na Área Total ({area_total:,.0f} ha)",
            "Valor Total (R$)": -custo_operacional_total,
            "Indicador (R$/ha)": -custo_operacional_total / area_total,
            "Eqv. (sc/ha)": -(custo_operacional_total / area_total) / preco_medio_ponderado
        },
        # GRUPO MARGEM CONTRIBUIÇÃO
        {
            "Grupo": "3. (=) RESULTADO OPERACIONAL (EBITDA)",
            "Descrição": "Geração de Caixa da Atividade Agrícola",
            "Valor Total (R$)": lucro_operacional,
            "Indicador (R$/ha)": lucro_operacional / area_total,
            "Eqv. (sc/ha)": (lucro_operacional / area_total) / preco_medio_ponderado
        },
        # GRUPO CUSTO FINANCEIRO
        {
            "Grupo": "4. (-) CUSTO FINANCEIRO (JUROS)",
            "Descrição": f"Total de Juros do Período ({dias_financiamento} dias)",
            "Valor Total (R$)": -custo_financeiro_juros,
            "Indicador (R$/ha)": -custo_financeiro_juros / area_total,
            "Eqv. (sc/ha)": -juros_por_saca_fisico * (producao_total/area_total) 
        },
        # LINHA EXTRA DE DETALHE DE JUROS
        {
            "Grupo": "   ↳ Impacto dos Juros (Unitário)",
            "Descrição": "Custo financeiro por cada saca produzida",
            "Valor Total (R$)": f"R$ {juros_por_saca_reais:.2f} /sc",
            "Indicador (R$/ha)": "-",
            "Eqv. (sc/ha)": f"-{juros_por_saca_fisico:.2f} sc/sc" 
        },
        # FLUXO DE CAIXA OPERACIONAL
        {
            "Grupo": "5. (=) FLUXO DE CAIXA OPERACIONAL",
            "Descrição": "Resultado após pagar operação e bancos",
            "Valor Total (R$)": fluxo_caixa_operacional,
            "Indicador (R$/ha)": fluxo_caixa_operacional / area_total,
            "Eqv. (sc/ha)": (fluxo_caixa_operacional / area_total) / preco_medio_ponderado
        },
        # GRUPO CUSTO TERRA
        {
            "Grupo": "6. (-) CUSTO DA TERRA (ARRENDAMENTO)",
            "Descrição": f"Ref. {area_arrendada:.0f} ha arrendados ({arrendamento_sc_ha} sc/ha)",
            "Valor Total (R$)": -custo_arrendamento_reais,
            "Indicador (R$/ha)": -custo_arrendamento_reais / area_total,
            "Eqv. (sc/ha)": -(vol_arrendamento_sacas / area_total)
        },
        # GRUPO RESULTADO LÍQUIDO
        {
            "Grupo": "7. (=) LUCRO LÍQUIDO FINAL",
            "Descrição": "Resultado Final após Capital e Terra",
            "Valor Total (R$)": lucro_liquido,
            "Indicador (R$/ha)": lucro_liquido / area_total,
            "Eqv. (sc/ha)": (lucro_liquido / area_total) / preco_medio_ponderado
        },
        # KPI FINAL DE MARGEM
        {
            "Grupo": "MARGEM LÍQUIDA (%)",
            "Descrição": "Lucro Líquido / Receita Bruta",
            "Valor Total (R$)": f"{margem_liquida_perc:.1f}%",
            "Indicador (R$/ha)": "-",
            "Eqv. (sc/ha)": "-"
        },
        # SEÇÃO 8: INDICADORES DE EFICIÊNCIA (NOVOS)
        {
            "Grupo": "8. ANÁLISE DE EFICIÊNCIA (KPIs)",
            "Descrição": "--- INDICADORES DE CUSTO E VIABILIDADE ---",
            "Valor Total (R$)": "",
            "Indicador (R$/ha)": "",
            "Eqv. (sc/ha)": ""
        },
        {
            "Grupo": "   ⚫ Custo Total Área Própria",
            "Descrição": "Op + Juros (Sem Arrendamento)",
            "Valor Total (R$)": "-",
            "Indicador (R$/ha)": custo_ha_area_propria,
            "Eqv. (sc/ha)": custo_ha_area_propria / preco_medio_ponderado
        },
        {
            "Grupo": "   🔴 Custo Total Área Arrendada",
            "Descrição": "Op + Juros + Arrendamento (Só se paga se prod > custo)",
            "Valor Total (R$)": "-",
            "Indicador (R$/ha)": custo_ha_area_arrendada,
            "Eqv. (sc/ha)": custo_ha_area_arrendada / preco_medio_ponderado
        },
        {
            "Grupo": "   ⚖️ Breakeven (Preço Venda)",
            "Descrição": "Produtividade necessária para pagar a conta (Preço Real)",
            "Valor Total (R$)": "-",
            "Indicador (R$/ha)": "-",
            "Eqv. (sc/ha)": breakeven_sc_ha
        },
        {
            "Grupo": "   🔥 Breakeven (Preço Spot)",
            "Descrição": "Produtividade necessária se vendesse a Mercado Hoje",
            "Valor Total (R$)": "-",
            "Indicador (R$/ha)": "-",
            "Eqv. (sc/ha)": breakeven_sc_ha_spot
        }
    ]
    
    df_dre_pro = pd.DataFrame(dados_dre_pro)
    
    def style_rows(v):
        if isinstance(v, (int, float)) and v < 0: return 'color: red;'
        if isinstance(v, (int, float)) and v > 0: return 'color: #2E7D32;'
        if isinstance(v, str) and "%" in v: return 'font-weight: bold; color: #2E7D32;'
        if isinstance(v, str) and "R$" in v and "-" in v: return 'color: red;'
        return ''

    st.dataframe(
        df_dre_pro.style.format({
            "Valor Total (R$)": lambda x: f"R$ {x:,.2f}" if isinstance(x, (int, float)) else x,
            "Indicador (R$/ha)": lambda x: f"R$ {x:,.2f}" if isinstance(x, (int, float)) else x,
            "Eqv. (sc/ha)": lambda x: f"{x:,.1f}" if isinstance(x, (int, float)) else x
        }).applymap(style_rows, subset=["Valor Total (R$)", "Indicador (R$/ha)", "Eqv. (sc/ha)"]),
        use_container_width=True,
        hide_index=True,
        height=550
    )
    
    st.info(f"💡 **Análise Crítica:** Na Área Arrendada, seu custo total é de **{custo_ha_area_arrendada/preco_medio_ponderado:.1f} sc/ha**. Se sua produtividade for **{produtividade} sc/ha**, o lucro nesta área é de apenas **{(produtividade - (custo_ha_area_arrendada/preco_medio_ponderado)):.1f} sc/ha**.")

st.markdown("---")

# --- INTELIGÊNCIA (ABAS) ---
st.markdown("### 🧠 Inteligência & Analytics")
tab1, tab2, tab3 = st.tabs(["📅 Sazonalidade (CEPEA)", "🔮 Monte Carlo", "🤖 AI Advisor"])

with tab1:
    st.markdown("**Sazonalidade Histórica (Base Paranaguá)**")
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    indices_sazonais = [1.03, 1.01, 0.95, 0.94, 0.97, 0.99, 1.01, 1.03, 1.05, 1.07, 1.08, 1.05]
    mes_atual = datetime.now().month - 1
    fator_ajuste = preco_mercado / indices_sazonais[mes_atual]
    precos_projetados = [idx * fator_ajuste for idx in indices_sazonais]
    fig_saz = go.Figure()
    fig_saz.add_trace(go.Bar(x=meses, y=precos_projetados, name="Preço Projetado", marker_color='#81C784'))
    fig_saz.add_trace(go.Scatter(x=meses, y=precos_projetados, mode='lines+markers', line=dict(color='#2E7D32', width=2), name="Tendência"))
    fig_saz.update_layout(height=350, margin=dict(t=20, b=20), template="plotly_white", yaxis_tickprefix="R$ ")
    st.plotly_chart(fig_saz, use_container_width=True)

with tab2:
    st.markdown("**Simulação de Probabilidade (Monte Carlo)**")
    if st.button("🔄 Rodar Simulação"):
        cenarios_preco = np.random.normal(preco_mercado, preco_mercado * 0.18, 5000)
        custos_arr_cenarios = vol_arrendamento_sacas * cenarios_preco
        rec_cenarios = receita_hedge + (qtd_aberta * cenarios_preco)
        lucros = rec_cenarios - (custo_operacional_total + custo_financeiro_juros + custos_arr_cenarios)
        prob_lucro = np.mean(lucros > 0) * 100
        st.metric("Probabilidade de Lucro", f"{prob_lucro:.1f}%")
        fig_hist = px.histogram(lucros, nbins=50, title="Distribuição do Resultado (R$)")
        fig_hist.add_vline(x=0, line_color="red")
        st.plotly_chart(fig_hist, use_container_width=True)

with tab3:
    st.markdown("### 🤖 Advisor Financeiro")
    peso_divida = (custo_financeiro_juros / receita_bruta_total) * 100
    st.write(f"Os juros consomem **{peso_divida:.1f}%** da sua receita bruta.")
    if margem_seguranca_sc_ha < 5:
        st.warning("⚠️ **ALTO RISCO:** Margem de segurança < 5 sc/ha.")
    else:
        st.success("✅ **CONFORTÁVEL:** Boa margem de segurança produtiva.")

# ======================================================================
# HEATMAP (COM MARCADOR "VOCÊ ESTÁ AQUI")
# ======================================================================
st.markdown("### 🔥 Mapa de Sensibilidade: Margem Líquida (R$/ha)")

prod_range = np.arange(40, 90, 5)
preco_range = np.arange(90, 185, 5)

z_data = np.zeros((len(prod_range), len(preco_range)))

for i, p_prod in enumerate(prod_range):
    for j, p_price in enumerate(preco_range):
        rec = p_prod * p_price
        custo_arr_cenario = (area_arrendada * arrendamento_sc_ha * p_price)
        custo_total_cenario = custo_operacional_total + custo_financeiro_juros + custo_arr_cenario
        custo_ha_cenario = custo_total_cenario / area_total
        z_data[i, j] = rec - custo_ha_cenario

fig_heat = go.Figure(
    data=go.Heatmap(
        z=z_data, 
        x=preco_range, 
        y=prod_range, 
        colorscale="RdYlGn", 
        colorbar=dict(title="R$/ha")
    )
)

text_vals = [[f"{val:,.0f}" for val in row] for row in z_data]

# Texto nas células
fig_heat.add_trace(go.Scatter(
    x=np.repeat(preco_range, len(prod_range)), 
    y=np.tile(prod_range, len(preco_range)), 
    text=[v for r in text_vals for v in r], 
    mode="text", 
    textfont=dict(size=10, color="black"), 
    hoverinfo="skip"
))

# --- NOVO: MARCADOR DE POSIÇÃO ATUAL ---
# Adiciona o ponto onde o usuário está
fig_heat.add_trace(go.Scatter(
    x=[preco_medio_ponderado],
    y=[produtividade],
    mode='markers',
    marker=dict(symbol='circle', size=12, color='#2E7D32', line=dict(width=2, color='white')),
    name="Sua Posição",
    hoverinfo="text",
    hovertext=f"VOCÊ ESTÁ AQUI<br>Prod: {produtividade} sc/ha<br>Preço Médio: R$ {preco_medio_ponderado:.2f}<br>Margem: R$ {(lucro_liquido/area_total):,.2f}/ha"
))

# Adiciona a anotação com seta
fig_heat.add_annotation(
    x=preco_medio_ponderado,
    y=produtividade,
    text="VOCÊ",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#1B5E20",
    ax=0,
    ay=-30,
    bgcolor="rgba(255, 255, 255, 0.8)",
    bordercolor="#2E7D32",
    borderwidth=1,
    borderpad=4,
    font=dict(size=11, color="#1B5E20", family="Arial Black")
)

fig_heat.update_layout(
    title="Margem Líquida por Hectare (R$/ha)", 
    xaxis_title="Preço (R$/sc)", 
    yaxis_title="Produtividade (sc/ha)", 
    height=600
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("<div class='footer'>AgroExposure v3.6 (Heatmap Interativo & DRE Ultimate) · Powered by Intelligence</div>", unsafe_allow_html=True)