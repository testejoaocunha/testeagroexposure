import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components
import os
from datetime import datetime, date, timedelta

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="AgroExposure | Intelligence Pro",
    layout="wide",
    page_icon="🌱"
)

# ---------------- DESIGN SYSTEM PREMIUM (UI CARRY STYLE - BLUE / PREMIUM) ----------------
st.markdown("""
<style>
    /* Fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: #F6F8FC;
        --surface: #FFFFFF;
        --surface-2: #F8FAFF;
        --border: #E6EAF2;
        --text: #0F172A;
        --muted: #64748B;
        --primary: #2F6FED;
        --primary-600: #245CE0;
        --primary-100: #EAF2FF;
        --success: #16A34A;
        --danger: #DC2626;
        --warning: #F59E0B;
        --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        --shadow-sm: 0 6px 18px rgba(15, 23, 42, 0.06);
        --radius: 16px;
    }

    /* --- APP --- */
    .stApp {
        background: linear-gradient(180deg, var(--primary-100) 0%, var(--bg) 28%, var(--bg) 100%) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* --- CONTAINER --- */
    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 5rem !important;
        max-width: 1400px;
    }

    /* --- HERO HEADER --- */
    .hero {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
        padding: 22px 24px;
        margin: 0 0 14px 0;
    }
    .hero-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--text);
        margin: 0;
        line-height: 1.1;
    }
    .hero-subtitle {
        margin-top: 6px;
        color: var(--muted);
        font-size: 14px;
        font-weight: 500;
    }

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 2.4rem !important;
    }

    /* --- INPUTS (BASEWEB) --- */
    div[data-baseweb="input"],
    div[data-baseweb="select"] > div {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: rgba(47,111,237,0.55) !important;
        box-shadow: 0 0 0 3px rgba(47,111,237,0.14) !important;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1rem !important;
        border: 1px solid var(--border) !important;
    }
    .stButton > button:active { transform: translateY(1px); }

    button[kind="primary"] {
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
        color: #FFFFFF !important;
        box-shadow: 0 8px 18px rgba(47,111,237,0.18) !important;
    }
    button[kind="primary"]:hover {
        background: var(--primary-600) !important;
        border-color: var(--primary-600) !important;
    }

    /* Botão HTML (print) */
    .btn-primary {
        background: var(--primary);
        color: #FFFFFF;
        border: 1px solid var(--primary);
        padding: 12px 18px;
        border-radius: 12px;
        width: 100%;
        font-weight: 800;
        cursor: pointer;
        box-shadow: 0 10px 20px rgba(47,111,237,0.18);
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    .btn-primary:hover { background: var(--primary-600); border-color: var(--primary-600); }

    /* --- TABS (PILLS) --- */
    div[data-baseweb="tab-list"] { gap: 8px !important; }
    div[data-baseweb="tab-list"] button {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 999px !important;
        padding: 8px 14px !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        background: var(--primary) !important;
        border-color: var(--primary) !important;
        color: #FFFFFF !important;
        box-shadow: 0 10px 20px rgba(47,111,237,0.18) !important;
    }
    div[data-baseweb="tab-list"] button p { font-weight: 700 !important; }

    /* --- METRIC CARDS --- */
    div[data-testid="metric-container"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 16px 16px !important;
        box-shadow: var(--shadow-sm) !important;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    div[data-testid="metric-container"] label {
        color: var(--muted) !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 26px !important;
        font-weight: 800 !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        font-size: 12px !important;
        font-weight: 700 !important;
        background: #F1F5F9 !important;
        padding: 5px 9px !important;
        border-radius: 999px !important;
        width: fit-content !important;
        margin-top: 10px !important;
    }

    /* --- TABLES / DATAFRAMES --- */
    div[data-testid="stDataFrame"] {
        border-radius: var(--radius);
        overflow: hidden;
        border: 1px solid var(--border);
        background: var(--surface);
        box-shadow: var(--shadow-sm);
    }
    .dataframe thead th {
        background: #F1F5F9 !important;
        color: var(--muted) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        text-transform: uppercase;
        font-size: 0.78rem !important;
        padding: 12px 15px !important;
        border: none !important;
    }
    .dataframe tbody td {
        padding: 12px 15px !important;
        border-bottom: 1px solid #F1F5F9 !important;
        color: #334155 !important;
        font-size: 0.92rem !important;
    }
    .dataframe tbody tr:nth-of-type(even) { background-color: #FAFBFF !important; }
    .dataframe tbody tr:hover { background-color: #EFF6FF !important; }

    /* --- EXPANDERS --- */
    div[data-testid="stExpander"] {
        background: var(--surface) !important;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow-sm);
        overflow: hidden;
    }
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        font-weight: 700 !important;
    }

    /* --- FOOTER --- */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border-top: 1px solid var(--border);
        color: var(--muted);
        text-align: center;
        padding: 10px 12px;
        font-size: 11px;
        z-index: 999;
    }

    /* --- PRINT --- */
    @media print {
        section[data-testid="stSidebar"], header, .footer, .stButton, button, .stDeployButton { display: none !important; }
        body, .stApp { background-color: white !important; }
        .block-container { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
        div[data-testid="metric-container"] { border: 1px solid #000 !important; box-shadow: none !important; }
    }
</style>
""", unsafe_allow_html=True)
# ---------------- FUNÇÕES UTILITÁRIAS DE FORMATAÇÃO ----------------
def fmt_brl(valor):
    if isinstance(valor, (int, float)):
        prefix = "- " if valor < 0 else ""
        val_abs = abs(valor)
        return f"{prefix}R$ {val_abs:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor

def fmt_dec(valor, suffix=""):
    if isinstance(valor, (int, float)):
        return f"{valor:,.2f}{suffix}".replace(",", "X").replace(".", ",").replace("X", ".")
    return valor

# ---------------- JAVASCRIPT PARA IMPRESSÃO ----------------
def print_button():
    js = """
    <script>
        function printPage() { window.print(); }
    </script>
    <button onclick="printPage()" class="btn-primary">🖨️ Gerar Relatório PDF</button>
    """
    components.html(js, height=70)

# ==============================================================================
# 1. BARRA LATERAL (INPUTS)
# ==============================================================================
with st.sidebar:
    print_button()
    
    st.markdown("<h2 style='text-align: center; color: #1D4ED8; margin-bottom: 20px; border-bottom: 2px solid #DBEAFE; padding-bottom: 10px;'>AGRO EXPOSURE</h2>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Parâmetros da Safra")
    
    with st.container():
        st.markdown("##### 🚨 Stress Test (Quebra)")
        simular_quebra = st.toggle("Ativar Simulação de Quebra")
        fator_quebra = 0.0
        if simular_quebra:
            perc_quebra = st.slider("% de Quebra da Safra", 0, 90, 20, step=5)
            fator_quebra = perc_quebra / 100.0
            st.warning(f"Simulando uma perda de {perc_quebra}% na produção.")

    st.markdown("---")

    # 1. Produção
    st.markdown("<p style='color:#1D4ED8; font-weight:bold; margin-top:10px; font-size:1.1rem;'>1. Produção e Custo</p>", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        area_propria = st.number_input("Área Própria (ha)", value=1000, step=0) 
    with col_a2:
        area_arrendada = st.number_input("Área Arrendada (ha)", value=500, step=0) 
    
    area_total = area_propria + area_arrendada
    if area_total == 0: area_total = 1 
    
    perc_propria = (area_propria / area_total) * 100
    perc_arrendada = (area_arrendada / area_total) * 100
    
    st.markdown(f"<div style='margin-bottom:10px;'>📍 Total: <b>{area_total:,.0f} ha</b> <span style='color:#78909C; font-size:12px;'>({perc_propria:.0f}% Próp. | {perc_arrendada:.0f}% Arr.)</span></div>", unsafe_allow_html=True)

    produtividade_base = st.number_input("Produtividade Est. (sc/ha)", value=60.0, step=1.0, format="%.1f")
    
    if simular_quebra:
        produtividade = produtividade_base * (1 - fator_quebra)
        st.markdown(f"**Produtividade Efetiva:** <span style='color:#D32F2F; font-weight:bold;'>{produtividade:.1f} sc/ha</span>", unsafe_allow_html=True)
    else:
        produtividade = produtividade_base
        
    vol_propria = area_propria * produtividade
    vol_arrendada = area_arrendada * produtividade
    producao_total = area_total * produtividade

    st.markdown(f"""
    <div style='background-color: #F1F8E9; padding: 12px; border-radius: 8px; margin-top: 8px; font-size: 13px; color: #33691E; border: 1px solid #DCEDC8;'>
        <div style='display:flex; justify-content:space-between;'><span>🌱 Própria:</span> <b>{fmt_dec(vol_propria, ' sc')}</b></div>
        <div style='display:flex; justify-content:space-between;'><span>🌱 Arrendada:</span> <b>{fmt_dec(vol_arrendada, ' sc')}</b></div>
        <hr style='margin: 6px 0; border-top: 1px solid #C5E1A5;'>
        <div style='display:flex; justify-content:space-between; font-size:14px;'><span>🚜 <b>Total:</b></span> <b>{fmt_dec(producao_total, ' sc')}</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    custo_ha_operacional = st.number_input("Custo Operacional (R$/ha)", value=6000.0, step=100.0, format="%.2f")
    
    # 2. Comercialização
    st.markdown("<hr style='margin: 15px 0; border-color:#E0E0E0;'><p style='color:#1D4ED8; font-weight:bold; font-size:1.1rem;'>2. Comercialização</p>", unsafe_allow_html=True)
    perc_comercializado = st.slider("% Já Travado (Hedge)", 0, 100, 25) 
    vol_hedge = producao_total * (perc_comercializado/100)
    st.caption(f"📦 Volume Travado: {fmt_dec(vol_hedge, ' sc')}")
    preco_medio_venda = st.number_input("Preço Médio Travado (R$/sc)", value=115.0, step=0.5, format="%.2f") 
    
    # 3. Mercado
    st.markdown("<hr style='margin: 15px 0; border-color:#E0E0E0;'><p style='color:#1D4ED8; font-weight:bold; font-size:1.1rem;'>3. Metas e Mercado</p>", unsafe_allow_html=True)
    preco_mercado = st.number_input("Preço de Mercado (atual) R$/sc", value=105.0, step=0.5, format="%.2f") 
    margem_desejada = st.slider("Margem Alvo (%)", 0, 50, 20)

    # 4. Custeio
    st.markdown("<hr style='margin: 15px 0; border-color:#E0E0E0;'><p style='color:#1D4ED8; font-weight:bold; font-size:1.1rem;'>4. Financiamento & Terra</p>", unsafe_allow_html=True)
    perc_financiado = st.number_input("% Custeio Financiado", value=30.0, step=5.0) 
    taxa_juros_ano = st.number_input("Taxa de Juros ao Ano (%)", value=12.0, step=0.5, format="%.2f")
    col_d1, col_d2 = st.columns(2)
    data_tomada = col_d1.date_input("Desembolso", value=date(2025, 8, 30))
    data_pagamento = col_d2.date_input("Pagamento", value=date(2026, 4, 30))
    
    st.markdown("<div style='margin-top:10px; font-weight:600; font-size:13px; color:#455A64;'>Custo do Arrendamento</div>", unsafe_allow_html=True)
    arrendamento_sc_ha = st.number_input("Pagamento (sc/ha)", value=15.0, step=0.5, format="%.2f") 
    st.caption(f"Ref. Área Arrendada: {area_arrendada:,.0f} ha")

    # 5. PERFIL DE PAGAMENTOS
    st.markdown("<hr style='margin: 15px 0; border-color:#E0E0E0;'><p style='color:#1D4ED8; font-weight:bold; font-size:1.1rem;'>5. Perfil de Pagamentos</p>", unsafe_allow_html=True)
    st.info("Distribuição do Custo Operacional (R$):")
    
    perc_insumos = st.slider("1. Insumos (Sementes/Quím/Fert)", 0, 100, 60)
    val_insumos_ha = custo_ha_operacional * (perc_insumos/100)
    st.markdown(f"<div style='text-align:right; font-size:12px; color:#546E7A; margin-top:-10px; margin-bottom:10px;'><b>{perc_insumos}% = {fmt_brl(val_insumos_ha)}/ha</b></div>", unsafe_allow_html=True)
    
    max_colheita = 100 - perc_insumos
    perc_colheita = st.slider("2. Colheita & Frete", 0, max_colheita, min(20, max_colheita))
    val_colheita_ha = custo_ha_operacional * (perc_colheita/100)
    st.markdown(f"<div style='text-align:right; font-size:12px; color:#546E7A; margin-top:-10px;'><b>{perc_colheita}% = {fmt_brl(val_colheita_ha)}/ha</b></div>", unsafe_allow_html=True)
    
    perc_manutencao = 100 - perc_insumos - perc_colheita
    val_manut_ha = custo_ha_operacional * (perc_manutencao/100)
    
    st.markdown(f"""
    <div style='background-color:#E1F5FE; padding:12px; border-radius:8px; border:1px solid #B3E5FC; margin-top:15px;'>
        <small style='color:#0277BD; font-weight:bold; text-transform:uppercase;'>3. Manutenção (Saldo)</small><br>
        <span style='font-size:18px; font-weight:800; color:#01579B;'>{perc_manutencao}%</span> <span style='font-size:12px; color:#0277BD;'>restantes</span><br>
        <div style='margin-top:4px; font-size:13px; color:#0277BD;'><b>= {fmt_brl(val_manut_ha)}/ha</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📅 Escalonar Pagto Insumos", expanded=True):
        st.write("Do valor dos Insumos (Item 1), como pagar a parte **não financiada**?")
        c_p1, c_p2 = st.columns(2)
        pct_entrada_insumo = c_p1.number_input("% Entrada", 0, 100, 50, step=10) 
        st.markdown("---")
        c_p2a, c_p2b = st.columns([1, 1.5])
        pct_parc2 = c_p2a.number_input("% P2", 0, 100, 25, step=5) 
        data_parc2 = c_p2b.date_input("Data P2", value=date(2026, 4, 30)) 
        c_p3a, c_p3b = st.columns([1, 1.5])
        pct_parc3 = c_p3a.number_input("% P3", 0, 100, 25, step=5) 
        data_parc3 = c_p3b.date_input("Data P3", value=date(2026, 5, 30)) 
        
        if (pct_entrada_insumo + pct_parc2 + pct_parc3) != 100:
            st.error("A soma das parcelas deve ser 100%")

    c_op1, c_op2 = st.columns(2)
    mes_plantio = c_op1.selectbox("Plantio", [9, 10, 11, 12], index=0, format_func=lambda x: f"Mês {x}") 
    mes_colheita = c_op2.selectbox("Colheita", [1, 2, 3, 4], index=3, format_func=lambda x: f"Mês {x}") 

# ==============================================================================
# ==============================================================================
# 2. CÁLCULOS PRINCIPAIS (AUDITORIA: CONSISTÊNCIA ECONÔMICA + EVITAR DUPLA CONTAGEM)
# ==============================================================================

# A. Físico e Receita
# Arrendamento é em SACAS (produto) -> reduz o volume comercializável
vol_arrendamento_sacas = area_arrendada * arrendamento_sc_ha
producao_liquida_sacas = producao_total - vol_arrendamento_sacas

# Hedge / Venda antecipada (percentual sobre a produção TOTAL projetada)
qtd_vendida = producao_total * (perc_comercializado / 100)
receita_hedge = qtd_vendida * preco_medio_venda

# Volume físico disponível para venda (já líquido de arrendamento)
qtd_aberta_fisica = max(0, producao_liquida_sacas - qtd_vendida)

# Receita Spot (saldo vendido ao preço atual)
receita_spot = qtd_aberta_fisica * preco_mercado
receita_bruta_total = receita_hedge + receita_spot

# Preço Médio Ponderado (BLENDED) sobre o volume COMERCIALIZÁVEL
preco_medio_blended = receita_bruta_total / producao_liquida_sacas if producao_liquida_sacas > 0 else 0

# B. Custos (Caixa) + Terra (Econômico)
custo_operacional_total = area_total * custo_ha_operacional
valor_base_financiamento = custo_operacional_total * (perc_financiado / 100)
dias_financiamento = max(0, (data_pagamento - data_tomada).days)
custo_financeiro_juros = valor_base_financiamento * ((taxa_juros_ano / 100) / 365) * dias_financiamento

# Custo da Terra (arrendamento) em R$ (referência de valor econômico)
# IMPORTANTE (AUDITORIA): Como o arrendamento é pago em SACAS, ele já reduz o volume de venda.
# Portanto, NÃO deve ser subtraído novamente no lucro de vendas (senão dupla contagem).
custo_arrendamento_reais_hoje = vol_arrendamento_sacas * preco_mercado

# Total CAIXA (o que precisa ser coberto por vendas): Operação + Juros
custo_total_caixa = custo_operacional_total + custo_financeiro_juros

# Total ECONÔMICO (inclui Terra ao preço de referência) - útil para indicadores de custo/barter
custo_total_safra = custo_total_caixa + custo_arrendamento_reais_hoje

# C. Resultados (consistentes)
# Lucro operacional e fluxo de caixa operacional já são consistentes (arrendamento em sacas está no volume líquido).
lucro_operacional = receita_bruta_total - custo_operacional_total
fluxo_caixa_operacional = lucro_operacional - custo_financeiro_juros

# LUCRO LÍQUIDO (AUDITORIA): usa apenas custos de CAIXA porque o arrendamento já foi descontado no volume vendido
lucro_liquido = receita_bruta_total - custo_total_caixa

# Margem líquida sobre a RECEITA DE VENDA
margem_liquida_perc = (lucro_liquido / receita_bruta_total) * 100 if receita_bruta_total > 0 else 0

# D. ROI E BARTER
# ROI (incluindo Terra como capital econômico)
roi_perc = (lucro_liquido / custo_total_safra) * 100 if custo_total_safra > 0 else 0
# ROI (somente caixa)
roi_caixa_perc = (lucro_liquido / custo_total_caixa) * 100 if custo_total_caixa > 0 else 0

barter_operacional_sc_ha = custo_ha_operacional / preco_mercado if preco_mercado > 0 else 0
barter_total_sc_ha = (custo_total_safra / area_total) / preco_mercado if preco_mercado > 0 else 0

# -------------------------------------------------------------------------
# PREÇOS-CHAVE (BREAKEVEN E META)
# -------------------------------------------------------------------------
# 1) Breakeven do SALDO (0x0): preço mínimo no saldo para pagar custos de CAIXA (Op + Juros)
saldo_a_cobrir = custo_total_caixa - receita_hedge
vol_disponivel_pgto = producao_liquida_sacas - qtd_vendida
preco_breakeven_saldo = saldo_a_cobrir / vol_disponivel_pgto if vol_disponivel_pgto > 0 else 0

# 2) Breakeven de PRODUTIVIDADE (duas visões)
# 2.1 Conservador: considera 100% do saldo ao preço de mercado (sem prêmio do hedge)
custo_op_fin_sc = custo_total_caixa / preco_mercado if preco_mercado > 0 else 0
breakeven_sc_total_conserv = custo_op_fin_sc + vol_arrendamento_sacas
breakeven_sc_ha_conservador = breakeven_sc_total_conserv / area_total if area_total > 0 else 0

# 2.2 Plano atual (considera prêmio do hedge no preço médio da produção total)
preco_medio_total_producao = ((perc_comercializado/100) * preco_medio_venda) + ((1 - (perc_comercializado/100)) * preco_mercado)
breakeven_sc_ha_plano = (custo_total_caixa + custo_arrendamento_reais_hoje) / (area_total * preco_medio_total_producao) if (area_total > 0 and preco_medio_total_producao > 0) else 0

# Mantém a variável original como a versão mais realista (plano)
breakeven_sc_ha = breakeven_sc_ha_plano

# 3) Preço Alvo do SALDO (para atingir margem desejada sobre receita de venda)
# Receita alvo: R * (1 - m) = custos_caixa => R = custos_caixa / (1 - m)
receita_alvo_total = custo_total_caixa / (1 - (margem_desejada/100)) if margem_desejada < 100 else custo_total_caixa * 1.5
receita_faltante_para_meta = receita_alvo_total - receita_hedge
preco_alvo_restante_meta = receita_faltante_para_meta / qtd_aberta_fisica if qtd_aberta_fisica > 0 else 0

# Indicadores auxiliares
margem_seguranca_sc_ha = produtividade - breakeven_sc_ha

# Custo por saca (CAIXA) no volume comercializável
custo_sc_liquida = custo_total_caixa / producao_liquida_sacas if producao_liquida_sacas > 0 else 0
# Custo por saca (ECONÔMICO) incluindo terra ao preço de referência
custo_sc_total = custo_total_safra / producao_liquida_sacas if producao_liquida_sacas > 0 else 0

# KPIs por hectare
custo_ha_medio_op_fin = (custo_total_caixa) / area_total if area_total > 0 else 0
custo_ha_area_arrendada = custo_ha_medio_op_fin + (arrendamento_sc_ha * preco_mercado)
custo_ha_area_propria = custo_ha_medio_op_fin

juros_por_saca_reais = custo_financeiro_juros / producao_total if producao_total > 0 else 0
juros_sc_ha = (custo_financeiro_juros / area_total) / preco_medio_blended if (area_total > 0 and preco_medio_blended > 0) else 0
# 3. INTERFACE DASHBOARD (LAYOUT PREMIUM)
# ==============================================================================
st.markdown("""
<div class="hero">
  <div class="hero-title">AgroExposure: Painel de Decisão Estratégica</div>
  <div class="hero-subtitle">Simule preço, hedge, risco e liquidez com visual premium no estilo "Análise do Carry".</div>
</div>
""", unsafe_allow_html=True) 

# KPI CARDS (AGORA COM 5 COLUNAS)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("🚜 Produção Líquida", f"{producao_liquida_sacas:,.0f} sc", delta=f"Total: {producao_total:,.0f} sc", help="Volume total MENOS arrendamento.")
with c2:
    st.metric("📉 Custo (Caixa/Liq)", fmt_brl(custo_sc_liquida) + " /sc", delta=f"Terra eqv: {fmt_brl(custo_sc_total)} /sc", delta_color="inverse", help="AUDITORIA: custo por saca comercializável (Operação + Juros). Terra (arrendamento em sacas) aparece como equivalente no delta.")
with c3:
    # NOVO KPI: PREÇO MÉDIO BLENDED
    delta_pm = preco_medio_blended - preco_mercado
    lbl_pm = "Acima do Mercado" if delta_pm > 0 else "Abaixo do Mercado"
    st.metric("⚖️ Preço Médio (Atual)", fmt_brl(preco_medio_blended), delta=f"{lbl_pm} ({fmt_brl(delta_pm)})", help="Média ponderada: (Volume Travado * Preço Travado) + (Volume Aberto * Preço Hoje).")
with c4:
    # NIVELAMENTO DO SALDO (0x0)
    lbl_delta = "Venda Favorável" if preco_breakeven_saldo < preco_mercado else "Preço Abaixo do Nivelamento"
    cor_delta = "normal" if preco_breakeven_saldo < preco_mercado else "inverse"
    st.metric("🛑 Nivelamento (0x0)", fmt_brl(preco_breakeven_saldo), delta=lbl_delta, delta_color=cor_delta, help="Preço mínimo de venda do SALDO para pagar as contas (Lucro Zero).")
with c5:
    # NOVO KPI: PREÇO ALVO META
    lbl_meta = f"Alvo para {margem_desejada}% Margem"
    delta_meta = preco_alvo_restante_meta - preco_mercado
    cor_meta = "inverse" if delta_meta > 0 else "normal"
    msg_meta = "✅ Spot atinge Meta" if delta_meta <= 0 else f"Falta {fmt_brl(delta_meta)}"
    st.metric("🎯 Preço Alvo (Saldo)", fmt_brl(preco_alvo_restante_meta), delta=msg_meta, delta_color=cor_meta, help=f"Por quanto vender as sacas restantes para garantir {margem_desejada}% de Margem Líquida Final.")

# GAUGE DE META (VELOCÍMETRO)
fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = margem_liquida_perc,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "<b>Status da Meta de Margem</b>", 'font': {'size': 18, 'color': '#263238', 'family': 'Inter'}},
    delta = {'reference': margem_desejada, 'increasing': {'color': "#2E7D32"}},
    gauge = {
        'axis': {'range': [None, max(50, margem_desejada + 20)], 'tickwidth': 1, 'tickcolor': "#37474F"},
        'bar': {'color': "#2F6FED"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "#CFD8DC",
        'steps': [
            {'range': [0, 0], 'color': '#FFEBEE'},
            {'range': [0, margem_desejada], 'color': '#E8F5E9'}],
        'threshold': {
            'line': {'color': "#FF9800", 'width': 4},
            'thickness': 0.75,
            'value': margem_desejada}
    }
))
fig_gauge.update_layout(height=200, margin=dict(l=20,r=20,t=40,b=20), paper_bgcolor="rgba(0,0,0,0)", font={'family': "Inter"})
st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")

# --- SIMULADOR WHAT-IF ---
with st.expander("⚖️ Simulador de Negociação (What-If)", expanded=False):
    st.markdown("#### Simule impacto na Margem Global")
    col_s1, col_s2, col_s3 = st.columns([1,1,2])
    with col_s1: st.info(f"Travado: {perc_comercializado}% a {fmt_brl(preco_medio_venda)}")
    with col_s2:
        n_perc = st.number_input("Nova Venda (%)", 0, 100, 10)
        n_preco = st.number_input("Preço (R$)", value=preco_mercado, format="%.2f")
    with col_s3:
        # AUDITORIA: Arrendamento é pago em SACAS e já reduz o volume líquido.
        # Portanto, não entra novamente como custo em R$ neste What-If (evita dupla contagem).
        q_nova_bruta = producao_total * (n_perc/100)
        q_nova = min(qtd_aberta_fisica, max(0, q_nova_bruta))

        # Receita simulada: hedge fixo + parte do saldo ao novo preço + restante ao preço atual
        rec_sim = receita_hedge + (q_nova * n_preco) + ((qtd_aberta_fisica - q_nova) * preco_mercado)

        # Custos simulados (CAIXA)
        custo_tot_sim = custo_total_caixa

        lucro_sim = rec_sim - custo_tot_sim
        margem_sim = (lucro_sim/rec_sim)*100 if rec_sim > 0 else 0
        delta_m = margem_sim - margem_liquida_perc
        st.metric("Nova Margem Estimada", f"{margem_sim:.2f}%", delta=f"{delta_m:+.2f}%")

st.markdown("---")

# --- GRÁFICOS PRINCIPAIS ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎯 Matriz de Risco")
    exposicao_perc = 100 - perc_comercializado
    
    # Ajuste dinâmico do eixo Y para garantir visualização
    y_min = min(-20, margem_liquida_perc - 15)
    y_max = max(60, margem_liquida_perc + 15)

    fig_rr = go.Figure()
    # Zonas
    fig_rr.add_shape(type="rect", x0=50, x1=100, y0=y_min, y1=margem_desejada, fillcolor="rgba(211, 47, 47, 0.1)", line_width=0)
    fig_rr.add_shape(type="rect", x0=50, x1=100, y0=margem_desejada, y1=y_max, fillcolor="rgba(251, 192, 45, 0.15)", line_width=0)
    fig_rr.add_shape(type="rect", x0=0, x1=50, y0=y_min, y1=margem_desejada, fillcolor="rgba(25, 118, 210, 0.05)", line_width=0)
    fig_rr.add_shape(type="rect", x0=0, x1=50, y0=margem_desejada, y1=y_max, fillcolor="rgba(56, 142, 60, 0.1)", line_width=0)
    
    # CORREÇÃO VISUAL: Texto preto e negrito, posição ajustada
    fig_rr.add_trace(go.Scatter(
        x=[exposicao_perc], 
        y=[margem_liquida_perc], 
        mode='markers+text',
        marker=dict(size=25, color='#2F6FED', line=dict(width=3, color='white')), 
        text=[f"<b>VOCÊ<br>{margem_liquida_perc:.1f}%</b>"], 
        textposition="top center", 
        textfont=dict(family="Inter", size=14, color="black") # Cor preta forçada
    ))
    
    fig_rr.update_layout(xaxis_title="Exposição Spot (%)", yaxis_title="Margem Líquida (%)",
        xaxis=dict(range=[0, 100]), yaxis=dict(range=[y_min, y_max]), height=350, template="plotly_white", margin=dict(l=20, r=20, t=20, b=20), font={'family': 'Inter'})
    st.plotly_chart(fig_rr, use_container_width=True)

with col_right:
    st.subheader("📉 Sensibilidade (Preço)")
    range_precos = np.linspace(preco_mercado * 0.75, preco_mercado * 1.25, 20)
    margens_sim = []
    
    for p in range_precos:
        # Receita Sim: Hedge + (Físico Aberto * p)
        rec_sim = receita_hedge + (qtd_aberta_fisica * p)

        # AUDITORIA: custos de caixa (arrendamento já está no volume líquido)
        custo_tot_sim = custo_total_caixa
        
        m = ((rec_sim - custo_tot_sim) / rec_sim) * 100
        margens_sim.append(m)
        
    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(x=range_precos, y=margens_sim, mode='lines', line=dict(color='#1565C0', width=4), name='Margem'))
    fig_sens.add_hline(y=margem_desejada, line_dash="dot", line_color="green", annotation_text="Meta")
    
    # Linha vertical no Breakeven de Saldo (Onde a curva cruza zero ou margem mínima)
    fig_sens.add_vline(x=preco_breakeven_saldo, line_dash="dash", line_color="#FF9800", annotation_text=f"0x0: {fmt_brl(preco_breakeven_saldo)}")
    
    fig_sens.update_layout(xaxis_title="Preço Soja (R$)", yaxis_title="Margem Líquida (%)", height=350, template="plotly_white", font={'family': 'Inter'})
    st.plotly_chart(fig_sens, use_container_width=True)

# --- FLUXO DE CAIXA INTELIGENTE (CORRIGIDO 50/25/25) ---
st.markdown("### 💸 Fluxo de Caixa Projetado (Liquidez)")
with st.expander("Ver Gráfico e Detalhes de Entradas/Saídas", expanded=True):
    meses_fluxo = pd.date_range(start=date(2025, 9, 1), periods=12, freq='M')
    nomes_meses = [d.strftime("%b/%y") for d in meses_fluxo]
    entradas = np.zeros(12)
    saidas = np.zeros(12) 
    
    # Custos Insumos
    custo_insumos_total = custo_operacional_total * (perc_insumos/100)
    # Parte financiada
    valor_insumos_financiado = min(custo_insumos_total, valor_base_financiamento)
    # Parte do bolso
    custo_insumos_proprio = custo_insumos_total - valor_insumos_financiado
    
    # Saldo do financiamento disponível para outras coisas
    saldo_financiamento = max(0, valor_base_financiamento - custo_insumos_total)
    
    # 1. Entrada Insumos (Mês Plantio ou Imediato) - Setembro/25 (Index 0)
    idx_plantio = 0 # Setembro
    saidas[idx_plantio] += custo_insumos_proprio * (pct_entrada_insumo/100)
    
    # 2. Parcelas Insumos (30/04 e 30/05)
    for i, m in enumerate(meses_fluxo):
        if m.month == data_parc2.month and m.year == data_parc2.year:
            saidas[i] += custo_insumos_proprio * (pct_parc2/100)
        if m.month == data_parc3.month and m.year == data_parc3.year:
            saidas[i] += custo_insumos_proprio * (pct_parc3/100)

    # Manutenção (Diluído)
    custo_manut_total = custo_operacional_total * (perc_manutencao/100)
    idx_colheita_arr = (mes_colheita - 9) if mes_colheita >= 9 else (mes_colheita + 3)
    duracao = max(1, idx_colheita_arr - idx_plantio + 1)
    mensal_manut = custo_manut_total / duracao
    for i in range(idx_plantio, idx_plantio + duracao):
        if 0 <= i < 12:
            pago_banco = min(mensal_manut, saldo_financiamento)
            pago_bolso = mensal_manut - pago_banco
            saidas[i] += pago_bolso
            saldo_financiamento -= pago_banco

    # Colheita
    custo_colheita_total = custo_operacional_total * (perc_colheita/100)
    if 0 <= idx_colheita_arr < 12:
        pago_banco = min(custo_colheita_total, saldo_financiamento)
        pago_bolso = custo_colheita_total - pago_banco
        saidas[idx_colheita_arr] += pago_bolso
        saldo_financiamento -= pago_banco

    # Pagamento Financiamento (Principal + Juros)
    if valor_base_financiamento > 0:
        mes_pg = data_pagamento.month
        ano_pg = data_pagamento.year
        for i, m in enumerate(meses_fluxo):
            if m.month == mes_pg and m.year == ano_pg:
                saidas[i] += (valor_base_financiamento + custo_financeiro_juros)
                break
    # Arrendamento (AUDITORIA): pago em SACAS (produto) -> já reduz a produção líquida e a receita de venda.
    # Para fluxo de CAIXA, não há desembolso em R$ aqui (evita dupla contagem).
    # Entradas
    # Hedge (Liquidação Financeira)
    if 0 <= idx_colheita_arr < 12:
        entradas[idx_colheita_arr] += receita_hedge
    
    # Spot (Venda do Saldo)
    idx_spot = min(11, idx_colheita_arr + 2)
    entradas[idx_spot] += receita_spot

    saldo_acumulado = np.cumsum(entradas - saidas)
    
    fig_fluxo = go.Figure()
    fig_fluxo.add_trace(go.Bar(x=nomes_meses, y=entradas, name='Entradas (Vendas)', marker_color='#66BB6A'))
    fig_fluxo.add_trace(go.Bar(x=nomes_meses, y=-saidas, name='Saídas (Desembolso)', marker_color='#EF5350'))
    fig_fluxo.add_trace(go.Scatter(x=nomes_meses, y=saldo_acumulado, name='Saldo Acumulado', mode='lines+markers', line=dict(color='#1565C0', width=3)))
    fig_fluxo.add_shape(type="line", x0=-0.5, x1=11.5, y0=0, y1=0, line=dict(color="black", width=1))
    fig_fluxo.update_layout(title="Fluxo de Caixa (Considerando Insumos 50/25/25)", barmode='relative', height=400, template="plotly_white", font={'family': 'Inter'})
    st.plotly_chart(fig_fluxo, use_container_width=True)
    
    st.markdown("#### 📉 Necessidade de Venda para Cobertura de Caixa")
    nec_venda = []
    total_deficit = 0
    total_sacas_nec = 0
    
    for i in range(12):
        gap = saidas[i] - entradas[i]
        if gap > 0:
            sc_nec = gap / preco_mercado
            perc = (sc_nec / producao_total) * 100 if producao_total > 0 else 0
            nec_venda.append([nomes_meses[i], fmt_brl(gap), f"{sc_nec:,.0f} sc", f"{perc:.1f}%"])
            total_deficit += gap
            total_sacas_nec += sc_nec
    
    if nec_venda:
        total_perc_safra = (total_sacas_nec / producao_total * 100) if producao_total > 0 else 0
        nec_venda.append(["TOTAL ACUMULADO", fmt_brl(total_deficit), f"{total_sacas_nec:,.0f} sc", f"{total_perc_safra:.1f}%"])
        df_nec = pd.DataFrame(nec_venda, columns=["Mês", "Déficit a Cobrir", "Sacas Necessárias", "% da Safra"])
        def style_total_row(row):
            if row.name == len(df_nec) - 1: return ['font-weight: bold; background-color: #E8F5E9; color: #1D4ED8; border-top: 2px solid #1D4ED8'] * len(row)
            return [''] * len(row)
        st.dataframe(df_nec.style.apply(style_total_row, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info("✅ Fluxo de caixa coberto. Nenhuma venda forçada necessária.")

st.markdown("---")

# --- DRE GERENCIAL DETALHADO ---
st.markdown("### 📋 DRE Gerencial de Decisão (Visão Econômica)")

with st.expander("Ver Análise Vertical Detalhada (R$/ha e sc/ha)", expanded=True):
    desc_custo_terra = f"Ref. {area_arrendada:.0f} ha arrendados ({arrendamento_sc_ha} sc/ha)" if area_arrendada > 0 else "Sem área arrendada"
    custo_arr_indicador = custo_ha_area_arrendada if area_arrendada > 0 else 0
    custo_arr_eqv = (custo_ha_area_arrendada / preco_medio_blended) if area_arrendada > 0 else 0
    
    # AUDITORIA (Arrendamento em sacas): para evitar dupla contagem, a DRE é apresentada em 2 níveis:
    # - VBP (Valor Bruto da Produção): inclui o valor econômico das sacas entregues no arrendamento (a preço de mercado)
    # - Receita Líquida Comercializável: receita efetiva de venda (volume líquido)
    vbp_total = receita_bruta_total + custo_arrendamento_reais_hoje
    prod_liq_sc_ha = producao_liquida_sacas / area_total if area_total > 0 else 0

    dados_dre_pro = [
        {"Grupo": "1. VALOR BRUTO DA PRODUÇÃO (VBP)", "Descrição": "Produção total valorizada (inclui arrendamento em sacas a preço mercado)", "Valor Total (R$)": vbp_total, "Indicador (R$/ha)": vbp_total / area_total, "Eqv. (sc/ha)": produtividade},
        {"Grupo": "2. (-) CUSTO DA TERRA (ARRENDAMENTO)", "Descrição": desc_custo_terra, "Valor Total (R$)": -custo_arrendamento_reais_hoje, "Indicador (R$/ha)": -custo_arrendamento_reais_hoje / area_total, "Eqv. (sc/ha)": -(vol_arrendamento_sacas / area_total)},
        {"Grupo": "3. (=) RECEITA LÍQUIDA COMERCIALIZÁVEL", "Descrição": f"Venda do volume líquido (média {fmt_brl(preco_medio_blended)})", "Valor Total (R$)": receita_bruta_total, "Indicador (R$/ha)": receita_bruta_total / area_total, "Eqv. (sc/ha)": prod_liq_sc_ha},
        {"Grupo": "4. (-) CUSTO OPERACIONAL", "Descrição": f"Custo aplicado na Área Total ({area_total:,.0f} ha)", "Valor Total (R$)": -custo_operacional_total, "Indicador (R$/ha)": -custo_operacional_total / area_total, "Eqv. (sc/ha)": -(custo_operacional_total / area_total) / preco_medio_blended if preco_medio_blended > 0 else 0},
        {"Grupo": "5. (=) RESULTADO OPERACIONAL (EBITDA)", "Descrição": "Geração de caixa da atividade agrícola", "Valor Total (R$)": lucro_operacional, "Indicador (R$/ha)": lucro_operacional / area_total, "Eqv. (sc/ha)": (lucro_operacional / area_total) / preco_medio_blended if preco_medio_blended > 0 else 0},
        {"Grupo": "6. (-) CUSTO FINANCEIRO (JUROS)", "Descrição": f"Total de juros do período ({dias_financiamento} dias)", "Valor Total (R$)": -custo_financeiro_juros, "Indicador (R$/ha)": -custo_financeiro_juros / area_total, "Eqv. (sc/ha)": -juros_sc_ha},
        {"Grupo": "  ↳ Impacto dos Juros (Unitário)", "Descrição": "Custo financeiro por saca produzida", "Valor Total (R$)": f"{fmt_brl(juros_por_saca_reais)} /sc", "Indicador (R$/ha)": "-", "Eqv. (sc/ha)": "-"},
        {"Grupo": "7. (=) RESULTADO FINAL (APÓS JUROS)", "Descrição": "Resultado final após operação e bancos", "Valor Total (R$)": lucro_liquido, "Indicador (R$/ha)": lucro_liquido / area_total, "Eqv. (sc/ha)": (lucro_liquido / area_total) / preco_medio_blended if preco_medio_blended > 0 else 0},
        {"Grupo": "MARGEM LÍQUIDA (%)", "Descrição": "Lucro Líquido / Receita de Venda", "Valor Total (R$)": f"{margem_liquida_perc:.1f}%", "Indicador (R$/ha)": "-", "Eqv. (sc/ha)": "-"},
        {"Grupo": "ROI (%)", "Descrição": "Lucro Líquido / (Custo Total incl. Terra)", "Valor Total (R$)": f"{roi_perc:.1f}%", "Indicador (R$/ha)": "-", "Eqv. (sc/ha)": "-"},
        {"Grupo": "ROI Caixa (%)", "Descrição": "Lucro Líquido / (Custo Caixa)", "Valor Total (R$)": f"{roi_caixa_perc:.1f}%", "Indicador (R$/ha)": "-", "Eqv. (sc/ha)": "-"},
        {"Grupo": "8. ANÁLISE DE EFICIÊNCIA (KPIs)", "Descrição": "--- INDICADORES DE CUSTO E VIABILIDADE ---", "Valor Total (R$)": "", "Indicador (R$/ha)": "", "Eqv. (sc/ha)": ""},
        {"Grupo": "  ⚫ Custo Total Área Própria", "Descrição": "Op + Juros (sem arrendamento)", "Valor Total (R$)": "-", "Indicador (R$/ha)": custo_ha_area_propria, "Eqv. (sc/ha)": (custo_ha_area_propria / preco_medio_blended) if preco_medio_blended > 0 else 0},
        {"Grupo": "  🔴 Custo Total Área Arrendada", "Descrição": "Op + Juros + Arrendamento (eqv)", "Valor Total (R$)": "-", "Indicador (R$/ha)": custo_arr_indicador if area_arrendada > 0 else "-", "Eqv. (sc/ha)": custo_arr_eqv if area_arrendada > 0 else "-"},
        {"Grupo": "  ⚖️ Breakeven (Produtividade)", "Descrição": "Produtividade mínima p/ 0x0 (Plano atual vs Conservador)", "Valor Total (R$)": "-", "Indicador (R$/ha)": "-", "Eqv. (sc/ha)": f"{breakeven_sc_ha_plano:.1f} (Plano) | {breakeven_sc_ha_conservador:.1f} (Mkt)"},
    ]

    df_dre_pro = pd.DataFrame(dados_dre_pro)
    df_dre_pro = pd.DataFrame(dados_dre_pro)
    
    def style_rows_dre(v):
        if isinstance(v, (int, float)) and v < 0: return 'color: #D32F2F; font-weight: 700;'
        if isinstance(v, str):
            if "- R$" in v: return 'color: #D32F2F; font-weight: 700;'
            if "-" in v and "%" in v: return 'color: #D32F2F; font-weight: 700;'
            if "%" in v: return 'font-weight: bold; color: #1D4ED8;'
        return ''

    st.dataframe(
        df_dre_pro.style.format({
            "Valor Total (R$)": lambda x: fmt_brl(x) if isinstance(x, (int, float)) else x,
            "Indicador (R$/ha)": lambda x: fmt_brl(x) if isinstance(x, (int, float)) else x,
            "Eqv. (sc/ha)": lambda x: f"{x:,.1f}" if isinstance(x, (int, float)) else x
        }).applymap(style_rows_dre, subset=["Valor Total (R$)", "Indicador (R$/ha)", "Eqv. (sc/ha)"]),
        use_container_width=True,
        hide_index=True,
        height=550
    )

st.markdown("### 🔥 Mapa de Sensibilidade: Margem Líquida (R$/ha)")
prod_range = np.arange(40, 90, 5)
preco_range = np.arange(90, 185, 5)
z_data = np.zeros((len(prod_range), len(preco_range)))

# Recalcular sensibilidade fixando custo fixo e variando receita e custo arr
for i, p_prod in enumerate(prod_range):
    for j, p_price in enumerate(preco_range):
        rec_ha = p_prod * p_price
        custo_arr_ha_cenario = (area_arrendada * arrendamento_sc_ha * p_price) / area_total
        custo_fixo_ha = (custo_operacional_total + custo_financeiro_juros) / area_total
        margem_ha = rec_ha - custo_fixo_ha - custo_arr_ha_cenario
        z_data[i, j] = margem_ha

fig_heat = go.Figure(data=go.Heatmap(z=z_data, x=preco_range, y=prod_range, colorscale="RdYlGn", colorbar=dict(title="R$/ha")))
text_vals = [[f"{val:,.0f}" for val in row] for row in z_data]
fig_heat.add_trace(go.Scatter(x=np.repeat(preco_range, len(prod_range)), y=np.tile(prod_range, len(preco_range)), text=[v for r in text_vals for v in r], mode="text", textfont=dict(size=10, color="black"), hoverinfo="skip"))
fig_heat.add_trace(go.Scatter(x=[preco_medio_blended], y=[produtividade], mode='markers', marker=dict(symbol='circle', size=12, color='#2F6FED', line=dict(width=2, color='white')), name="Sua Posição", hoverinfo="text", hovertext=f"VOCÊ ESTÁ AQUI<br>Prod: {produtividade:.1f} sc/ha<br>Preço Médio: {fmt_brl(preco_medio_blended)}<br>Resultado: {fmt_brl(lucro_liquido/area_total)}/ha"))
fig_heat.update_layout(title="Margem Líquida por Hectare (R$/ha)", xaxis_title="Preço (R$/sc)", yaxis_title="Produtividade (sc/ha)", height=600)
st.plotly_chart(fig_heat, use_container_width=True)

# --- INTELIGÊNCIA (ABAS ATUALIZADAS) ---
st.markdown("### 🧠 Inteligência & Analytics")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔄 Barter & ROI", "📦 Decisão Armazenagem", "📅 Sazonalidade", "🔮 Monte Carlo", "🤖 AI Advisor (Avançado)"])

with tab1:
    st.markdown("#### 📊 Eficiência Financeira (Barter & ROI)")
    col_br1, col_br2 = st.columns(2)
    with col_br1:
        st.markdown("**ROI (Retorno Sobre Investimento)**")
        st.metric("ROI Estimado", f"{roi_perc:.1f}%", help="Para cada R$ 100,00 investidos, quanto retorna de lucro.")
        if roi_perc > 15: st.success("🚀 ROI Excelente (>15%)")
        elif roi_perc > 0: st.info("📈 ROI Positivo (Operação Saudável)")
        else: st.error("📉 ROI Negativo (Atenção)")
    with col_br2:
        st.markdown("**Monitor de Barter (Relação de Troca)**")
        st.metric("Custo Operacional (Barter)", f"{barter_operacional_sc_ha:.1f} sc/ha", help="Sacas necessárias para pagar apenas o custo operacional.")
        st.metric("Custo Total (Barter)", f"{barter_total_sc_ha:.1f} sc/ha", help="Sacas necessárias para pagar TUDO (Op + Fin + Arr).")

    st.markdown("---")
    
    # --- CALCULADORA DE BARTER REFORMULADA ---
    st.markdown("#### 🔢 Calculadora Rápida de Barter")
    
    col_calc1, col_calc2, col_calc3 = st.columns([1.5, 1, 1])
    
    with col_calc1:
        valor_compra = st.number_input("Valor da Compra/Insumo (R$)", value=930000.00, format="%.2f")
    
    with col_calc2:
        preco_base_barter = st.number_input("Preço Mercado (Atual) R$/sc", value=preco_mercado, format="%.2f")
    
    with col_calc3:
        sacas_necessarias = valor_compra / preco_base_barter if preco_base_barter > 0 else 0
        st.metric("Custo em Sacas", fmt_dec(sacas_necessarias, " sc"), f"Base: {fmt_brl(preco_base_barter)}")

with tab2:
    st.markdown("#### 📉 Calculadora de Carry (Vender Agora vs. Segurar)")
    col_c1, col_c2, col_c3 = st.columns(3)
    custo_arm = col_c1.number_input("Custo Armazém (R$/sc/mês)", 0.0, 5.0, 0.80, format="%.2f")
    taxa_opp = col_c2.number_input("Custo Oportunidade (% a.m.)", 0.0, 5.0, 1.0, help="Quanto seu dinheiro renderia no banco (CDI)", format="%.2f")
    meses_carry = col_c3.slider("Meses Guardado", 1, 12, 4)
    preco_futuro_est = st.number_input(f"Preço Estimado Daqui a {meses_carry} Meses (R$/sc)", value=preco_mercado + 12.0, format="%.2f")
    custo_fisico = custo_arm * meses_carry
    custo_financeiro = preco_mercado * (taxa_opp/100) * meses_carry
    custo_total_carry = custo_fisico + custo_financeiro
    preco_net_futuro = preco_futuro_est - custo_total_carry
    resultado_carry = preco_net_futuro - preco_mercado
    st.markdown("---")
    cm1, cm2, cm3 = st.columns(3)
    cm1.metric("Custo Total de Carregar", fmt_brl(custo_total_carry) + "/sc", delta="Armazém + Juros", delta_color="inverse")
    cm2.metric("Preço Net Futuro", fmt_brl(preco_net_futuro) + "/sc", help="Preço Futuro - Custo de Carregar")
    if resultado_carry > 0:
        cm3.metric("Resultado da Decisão", f"GANHO DE {fmt_brl(resultado_carry)}", delta="✅ Segurar Compensa")
        st.success(f"**Recomendação:** O mercado futuro paga o custo de carregar e sobra **{fmt_brl(resultado_carry)}** por saca.")
    else:
        cm3.metric("Resultado da Decisão", f"PERDA DE {fmt_brl(abs(resultado_carry))}", delta="❌ Venda Agora", delta_color="inverse")
        st.error(f"**Recomendação:** Não compensa guardar. O custo de carregar ({fmt_brl(custo_total_carry)}) é maior que a valorização esperada.")

with tab3:
    st.markdown("**Sazonalidade Histórica (Base Paranaguá)**")
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    indices_sazonais = [1.03, 1.01, 0.95, 0.94, 0.97, 0.99, 1.01, 1.03, 1.05, 1.07, 1.08, 1.05]
    fator_ajuste = preco_mercado / indices_sazonais[datetime.now().month - 1]
    precos_projetados = [idx * fator_ajuste for idx in indices_sazonais]
    st.plotly_chart(go.Figure([go.Bar(x=meses, y=precos_projetados, marker_color='#81C784')]).update_layout(height=300), use_container_width=True)

with tab4:
    if st.button("🔄 Rodar Simulação Monte Carlo"):
        cenarios = np.random.normal(preco_mercado, preco_mercado*0.18, 5000)
        lucros = (receita_hedge + (qtd_aberta_fisica * cenarios)) - custo_total_caixa
        st.metric("Probabilidade de Lucro", f"{(np.mean(lucros > 0) * 100):.1f}%")
        st.plotly_chart(px.histogram(lucros, title="Distribuição de Resultados"), use_container_width=True)

with tab5:
    st.markdown("### 🤖 Advisor Financeiro")
    if roi_perc < 0:
        st.error(f"🚨 **ALERTA DE PREJUÍZO:** Sua operação está destruindo valor. O ROI é de **{roi_perc:.1f}%**. Isso significa que para cada R$ 100 investidos, você perde R$ {abs(roi_perc):.1f}. Revise urgentemente o Custo Operacional (atualmente {fmt_brl(custo_ha_operacional)}/ha) ou sua estratégia de vendas.")
    elif roi_perc < 10:
        st.warning(f"⚠️ **MARGEM APERTADA:** O ROI de **{roi_perc:.1f}%** é positivo, mas baixo para o risco agrícola. Qualquer quebra de safra ou queda de preço pode levar ao prejuízo. Considere travar custos ou aumentar o Hedge.")
    else:
        st.success(f"✅ **OPERAÇÃO SAUDÁVEL:** Excelente ROI de **{roi_perc:.1f}%**. Sua eficiência está acima da média. Aproveite para criar caixa.")
    
    margem_sc = produtividade - breakeven_sc_ha_plano
    if margem_sc < 0:
        st.markdown(f"""📉 **PONTO DE EQUILÍBRIO CRÍTICO:** Você precisa de **{breakeven_sc_ha_plano:.1f} sc/ha** para pagar a conta, mas sua estimativa é colher apenas **{produtividade:.1f} sc/ha**. O déficit é de **{abs(margem_sc):.1f} sc/ha**.

> Referência conservadora (100% a mercado): **{breakeven_sc_ha_conservador:.1f} sc/ha**.""")
    elif margem_sc < 5:
        st.markdown(f"🔸 **RISCO DE PRODUTIVIDADE:** Sua 'gordura' é muito fina. Você só tem **{margem_sc:.1f} sc/ha** de margem de segurança. Uma seca moderada pode comprometer o lucro.")
    else:
        st.markdown(f"🛡️ **SEGURANÇA PRODUTIVA:** Você tem uma folga confortável de **{margem_sc:.1f} sc/ha** acima do custo. Isso protege sua operação contra intempéries leves.")

    peso_juros = (custo_financeiro_juros / receita_bruta_total) * 100
    if peso_juros > 15:
        st.markdown(f"💸 **ALAVANCAGEM ALTA:** Cuidado. Os juros bancários estão consumindo **{peso_juros:.1f}%** da sua receita bruta total. Tente reduzir a exposição financiada ou buscar taxas menores.")
    else:
        st.markdown(f"💰 **ALAVANCAGEM CONTROLADA:** O custo financeiro representa apenas **{peso_juros:.1f}%** da receita, o que é saudável.")

st.markdown("""
<div class="footer">
    AgroExposure v10.3 (Fixed Visuals & KPI Strategy) · <b>Desenvolvido por João Cunha</b>
</div>
""", unsafe_allow_html=True)
