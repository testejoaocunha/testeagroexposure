import streamlit as st

st.set_page_config(page_title="Calculadora Premium", layout="wide", page_icon="🧮")

st.title("🧮 Calculadora Premium")
st.caption("Página carregou corretamente ✅")

# ==============================================================================
# ESTILIZAÇÃO CSS (DESIGN SYSTEM PREMIUM)
# ==============================================================================
st.markdown("""
    <style>
    /* Fundo geral e container */
    .main { background-color: #f4f6f8; }
    .block-container { padding: 1.5rem 1rem !important; }
    
    /* Cabeçalho de Mês (Estilo Cartão Robusto) */
    .month-header {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        color: white; 
        padding: 10px; 
        text-align: center; 
        font-weight: 700; 
        font-size: 0.95rem; 
        border-radius: 6px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.15); 
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Rótulos (Labels) - Ajustados para não cortar */
    .field-label { 
        font-size: 10.5px; 
        font-weight: 700; 
        color: #37474f; 
        display: flex; 
        align-items: center; 
        height: 32px; /* Alinha verticalmente com o input */
        white-space: nowrap; /* Impede quebra de linha feia */
    }
    
    /* Seções com divisórias e Ícones */
    .section-tag {
        font-size: 10px; 
        font-weight: 800; 
        color: #1b5e20;
        border-bottom: 2px solid #e0e0e0; 
        margin: 15px 0 8px 0;
        padding-bottom: 4px; 
        display: flex; 
        align-items: center; 
        gap: 6px;
        text-transform: uppercase;
    }
    
    /* Inputs (Caixas de número) */
    div[data-testid="stNumberInput"] { margin-bottom: -16px !important; }
    div[data-testid="stNumberInput"] input { 
        height: 32px !important; 
        font-size: 12px !important; 
        border-radius: 4px !important;
        border: 1px solid #cfd8dc;
        background-color: #fff;
        font-weight: 600;
        color: #263238;
    }
    div[data-testid="stNumberInput"] input:focus {
        border-color: #2e7d32;
        box-shadow: 0 0 0 1px #2e7d32;
    }
    
    /* Cards de Resultado (Rodapé) */
    .result-card {
        background: white; 
        border-radius: 6px; 
        padding: 10px 12px; 
        margin-top: 10px; 
        border: 1px solid #eceff1; 
        border-left: 5px solid #1b5e20; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .result-card:hover { transform: translateY(-2px); box-shadow: 0 5px 10px rgba(0,0,0,0.1); }
    
    .res-title { 
        font-size: 9px; 
        color: #78909c; 
        text-transform: uppercase; 
        font-weight: 700; 
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    .res-value { 
        font-size: 15px; 
        font-weight: 800; 
        color: #1b5e20; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
    }
    .res-unit {
        font-size: 10px;
        color: #546e7a;
        background: #eceff1;
        padding: 2px 4px;
        border-radius: 4px;
    }

    /* Ajuste fino de colunas do Streamlit */
    [data-testid="column"] { padding: 0 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# Título
st.markdown("<h2 style='color: #1b5e20; margin-bottom: 25px; border-bottom: 1px solid #ddd; padding-bottom: 10px;'>🍃 Calculadora <span style='font-weight: 300; color: #555;'>Premium</span></h2>", unsafe_allow_html=True)

# Parâmetros de Cálculo
FATOR_SOJA = 36.74541
TAXA_FRETE_DESC = 0.0925

meses = ["JAN/26", "FEV/26", "MAR/26", "ABR/26", "MAI/26", "JUN/26"]
cols = st.columns(len(meses))

for i, mes in enumerate(meses):
    with cols[i]:
        st.markdown(f"<div class='month-header'>📅 {mes}</div>", unsafe_allow_html=True)
        
        # --- FUNÇÃO DE LAYOUT CORRIGIDA ---
        def row_input(label, key, val, fmt="%.4f"):
            # AQUI ESTÁ A CORREÇÃO: [1.9, 1] dá muito mais espaço para o texto
            c1, c2 = st.columns([1.9, 1])
            with c1: st.markdown(f"<div class='field-label'>{label}</div>", unsafe_allow_html=True)
            with c2: return st.number_input(label, value=val, format=fmt, key=key, label_visibility="collapsed")

        # --- MERCADO ---
        st.markdown("<div class='section-tag'>📈 MERCADO</div>", unsafe_allow_html=True)
        cbot = row_input("CBOT (Bu)", f"cb_{i}", 10.4350)
        premio = row_input("PRÊMIO", f"pr_{i}", 0.50)
        
        # --- LIQUIDAÇÃO ---
        st.markdown("<div class='section-tag'>🏦 LIQUIDAÇÃO</div>", unsafe_allow_html=True)
        dolar_entrega = row_input("DÓL. ENTREGA", f"de_{i}", 5.6400)
        dolar_pagamento = row_input("DÓL. PAGTO", f"dp_{i}", 5.8000)
        
        # --- CUSTOS R$ ---
        st.markdown("<div class='section-tag'>🚛 CUSTOS R$/t</div>", unsafe_allow_html=True)
        fob_rs = row_input("FOBBINGS", f"fbr_{i}", 10.00, "%.2f")
        q_rs = row_input("QUEBRA", f"qrr_{i}", 1.00, "%.2f")
        o_rs = row_input("OUTROS", f"otr_{i}", 1.00, "%.2f")
        frete_bruto = row_input("FRETE BRUTO", f"frt_{i}", 170.00, "%.2f")

        # --- CUSTOS U$ ---
        st.markdown("<div class='section-tag'>💵 CUSTOS U$/t</div>", unsafe_allow_html=True)
        fob_us = row_input("FOBBINGS", f"fbu_{i}", 5.00, "%.2f")
        q_us = row_input("QUEBRA", f"qru_{i}", 0.25, "%.2f")
        o_us = row_input("OUTROS", f"otu_{i}", 0.50, "%.2f")

        # --- MATEMÁTICA ---
        preco_mercado_us_t = (cbot + premio) * FATOR_SOJA
        frete_liquido_rs = frete_bruto * (1 - TAXA_FRETE_DESC)
        
        custos_rs_dolarizados = (fob_rs + q_rs + o_rs + frete_liquido_rs) / dolar_entrega
        custo_total_us_t = custos_rs_dolarizados + (fob_us + q_us + o_us)
        
        preco_us_sc = (preco_mercado_us_t - custo_total_us_t) * 0.06
        preco_rs_sc = preco_us_sc * dolar_pagamento

        # --- RESULTADOS ESTABILIZADOS ---
        st.markdown(f"""
            <div class='result-card' style='border-left-color: #2e7d32;'>
                <div class='res-title'>💰 Preço Final</div>
                <div class='res-value'>
                    <span class='res-unit'>R$/sc</span> 
                    <span>{preco_rs_sc:,.2f}</span>
                </div>
            </div>
            
            <div class='result-card' style='border-left-color: #0277bd;'>
                <div class='res-title'>💵 Margem Dólar</div>
                <div class='res-value' style='color: #0277bd;'>
                    <span class='res-unit'>U$/sc</span> 
                    <span>{preco_us_sc:,.3f}</span>
                </div>
            </div>
            
            <div class='result-card' style='border-left-color: #78909c; background-color: #fafafa;'>
                <div class='res-title'>📦 Custo Total</div>
                <div class='res-value' style='color: #546e7a;'>
                    <span class='res-unit'>U$/t</span> 
                    <span>{custo_total_us_t:,.2f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)