import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="AgroExposure | Intelligence",
    layout="wide",
    page_icon="🌱"
)

# ---------------- ESTILO CSS PREMIUM (COMPACTO) ----------------
st.markdown("""
<style>
    /* 1. CONFIGURAÇÕES GERAIS */
    .stApp { background-color: #F8F9FA; color: #31333F; }
    
    /* 2. SIDEBAR OTIMIZADA */
    section[data-testid="stSidebar"] .block-container { padding-top: 1rem !important; padding-bottom: 2rem; }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }

    /* 3. INPUTS ESTILIZADOS */
    div[data-baseweb="input"] {
        background-color: #F8F9FA !important; border: 1px solid #CFD8DC !important; border-radius: 6px !important; padding: 2px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border: 1px solid #2E7D32 !important; background-color: #FFFFFF !important; box-shadow: 0 0 0 1px rgba(46, 125, 50, 0.2);
    }
    div[data-testid="stWidgetLabel"] label {
        font-weight: 600 !important; color: #37474F !important; font-size: 13px !important; margin-bottom: 0px !important;
    }
    
    /* 4. CARDS E CONTAINERS */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 10px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    
    /* 5. RODAPÉ */
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
    # --- LOGOTIPO ---
    caminho_logo = r"C:\Users\João Carlos\Desktop\Aplicativo Custo\1.png"
    if os.path.exists(caminho_logo):
        st.image(caminho_logo, use_container_width=True)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Parâmetros da Safra")
    
    # Bloco 1: Produção
    st.markdown("<p style='color:#2E7D32; font-weight:bold; margin-bottom:5px; margin-top:10px;'>1. Produção e Custo</p>", unsafe_allow_html=True)
    area = st.number_input("Área (ha)", value=2000.0, step=100.0)
    produtividade = st.number_input("Produtividade Est. (sc/ha)", value=65.0, step=1.0)
    producao_total = area * produtividade
    custo_ha = st.number_input("Custo Total (R$/ha)", value=6200.0, step=100.0)

    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #E0E0E0;'>", unsafe_allow_html=True)

    # Bloco 2: Comercialização
    st.markdown("<p style='color:#2E7D32; font-weight:bold; margin-bottom:5px;'>2. Comercialização</p>", unsafe_allow_html=True)
    perc_comercializado = st.slider("% Já Travado (Hedge)", 0, 100, 30)
    vol_travado_sidebar = producao_total * (perc_comercializado / 100)
    st.markdown(f"<div style='background-color: #E8F5E9; padding: 8px; border-radius: 6px; border: 1px solid #C8E6C9; text-align: center; margin-bottom: 10px;'><span style='color: #1B5E20; font-weight: 600; font-size: 13px;'>📦 Volume: {vol_travado_sidebar:,.0f} sc</span></div>", unsafe_allow_html=True)
    preco_medio_venda = st.number_input("Preço Médio Travado (R$/sc)", value=125.0, step=0.5)
    
    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px solid #E0E0E0;'>", unsafe_allow_html=True)
    
    # Bloco 3: Mercado
    st.markdown("<p style='color:#2E7D32; font-weight:bold; margin-bottom:5px;'>3. Metas e Mercado</p>", unsafe_allow_html=True)
    preco_mercado = st.number_input("Preço Balcão/Spot (R$/sc)", value=115.0, step=0.5)
    margem_desejada = st.slider("Margem Alvo (%)", 0, 50, 20)

# ==============================================================================
# 2. CÁLCULOS PRINCIPAIS (CORE)
# ==============================================================================
# Totais
custo_total_safra = area * custo_ha
custo_sc = custo_ha / produtividade

# Posição Atual
qtd_vendida = producao_total * (perc_comercializado / 100)
receita_ja_garantida = qtd_vendida * preco_medio_venda
qtd_aberta = producao_total - qtd_vendida
exposicao_perc = 100 - perc_comercializado

# Margem Projetada (Blended)
receita_saldo_spot = qtd_aberta * preco_mercado
receita_total_projetada = receita_ja_garantida + receita_saldo_spot
lucro_projetado = receita_total_projetada - custo_total_safra
margem_projetada = (lucro_projetado / custo_total_safra) * 100

# Breakeven do Saldo
receita_alvo_total = custo_total_safra * (1 + margem_desejada / 100)
receita_faltante = receita_alvo_total - receita_ja_garantida
preco_breakeven_saldo = receita_faltante / qtd_aberta if qtd_aberta > 0 else 0

# ==============================================================================
# 3. INTERFACE DASHBOARD
# ==============================================================================
st.title("📊 AgroExposure: Gestão de Risco") 
st.markdown("### Visão Geral & Rentabilidade")

# --- KPIs SUPERIORES ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Produção Total", f"{producao_total:,.0f} sc", delta=f"{area:,.0f} ha")
with c2: st.metric("Custo Médio (Breakeven)", f"R$ {custo_sc:,.2f} /sc", help="Custo Operacional")
with c3:
    delta_margem = margem_projetada - margem_desejada
    st.metric("Margem Projetada", f"{margem_projetada:.1f}%", delta=f"{delta_margem:.1f}% vs Meta", delta_color="normal" if delta_margem >= 0 else "inverse")
with c4:
    lbl_delta = "Positivo (Abaixo do Mercado)" if preco_breakeven_saldo < preco_mercado else "Atenção (Acima do Mercado)"
    st.metric("Preço Alvo Saldo", f"R$ {preco_breakeven_saldo:,.2f}", delta=lbl_delta, delta_color="inverse")

st.markdown("---")

# --- FUNCIONALIDADE 2: COMPARADOR DE CENÁRIOS ("What-If") ---
with st.expander("⚖️ Simulador de Negociação: Comparar Cenários (What-If)", expanded=False):
    st.markdown("#### Simule uma nova venda e veja o impacto na margem global")
    
    col_sim1, col_sim2, col_sim3 = st.columns([1, 1, 2])
    
    with col_sim1:
        st.info(f"**Cenário Atual:**\n\nTravado: {perc_comercializado}%\n\nMédia: R$ {preco_medio_venda:.2f}")
    
    with col_sim2:
        # Inputs da Simulação
        novo_perc_venda = st.number_input("Vender mais quanto (%)?", 0, int(exposicao_perc), 10)
        novo_preco_venda = st.number_input("A qual preço (R$)?", value=preco_mercado, step=0.5)
        
    with col_sim3:
        # Cálculo do Cenário Simulado
        qtd_nova_venda = producao_total * (novo_perc_venda / 100)
        nova_receita_travada = receita_ja_garantida + (qtd_nova_venda * novo_preco_venda)
        nova_qtd_aberta = qtd_aberta - qtd_nova_venda
        
        # Novo Blended
        nova_receita_total = nova_receita_travada + (nova_qtd_aberta * preco_mercado)
        novo_lucro = nova_receita_total - custo_total_safra
        nova_margem = (novo_lucro / custo_total_safra) * 100
        
        diff_margem = nova_margem - margem_projetada
        
        st.metric(
            label="Nova Margem Projetada (Após Venda)",
            value=f"{nova_margem:.2f}%",
            delta=f"{diff_margem:+.2f}% de ganho na margem global"
        )
        if diff_margem > 0:
            st.success(f"Recomendação: Vender {novo_perc_venda}% a R$ {novo_preco_venda} melhora seu resultado final!")

st.markdown("---")

# --- ÁREA DE GRÁFICOS PRINCIPAIS ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎯 Matriz de Risco")
    fig_rr = go.Figure()
    # Quadrantes
    fig_rr.add_shape(type="rect", x0=50, x1=100, y0=-20, y1=margem_desejada, fillcolor="rgba(255, 0, 0, 0.1)", line_width=0)
    fig_rr.add_shape(type="rect", x0=50, x1=100, y0=margem_desejada, y1=60, fillcolor="rgba(255, 215, 0, 0.15)", line_width=0)
    fig_rr.add_shape(type="rect", x0=0, x1=50, y0=-20, y1=margem_desejada, fillcolor="rgba(0, 0, 255, 0.05)", line_width=0)
    fig_rr.add_shape(type="rect", x0=0, x1=50, y0=margem_desejada, y1=60, fillcolor="rgba(0, 128, 0, 0.1)", line_width=0)
    # Ponto
    fig_rr.add_trace(go.Scatter(x=[exposicao_perc], y=[margem_projetada], mode='markers+text',
        marker=dict(size=22, color='#2E7D32', line=dict(width=2, color='white')),
        text=["VOCÊ"], textposition="top center", textfont=dict(color='#1B5E20', size=14, family="Arial Black")))
    fig_rr.update_layout(xaxis_title="Exposição Spot (%)", yaxis_title="Margem Projetada (%)",
        xaxis=dict(range=[0, 100]), yaxis=dict(range=[-10, 50]), height=350, template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_rr, use_container_width=True)

with col_right:
    st.subheader("📉 Sensibilidade")
    range_precos = np.linspace(preco_mercado * 0.7, preco_mercado * 1.3, 30)
    margens_simuladas = [(((receita_ja_garantida + (qtd_aberta * p)) - custo_total_safra) / custo_total_safra) * 100 for p in range_precos]
    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(x=range_precos, y=margens_simuladas, mode='lines', line=dict(color='#1565C0', width=4), name='Curva'))
    fig_sens.add_hline(y=margem_desejada, line_dash="dot", line_color="green", annotation_text="Meta")
    fig_sens.add_vline(x=preco_breakeven_saldo, line_dash="dash", line_color="#FF9800", annotation_text=f"Alvo: R${preco_breakeven_saldo:.1f}")
    fig_sens.update_layout(xaxis_title="Preço Venda Saldo (R$)", yaxis_title="Margem Final (%)", height=350, template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_sens, use_container_width=True)

# ==============================================================================
# 4. INTELIGÊNCIA DE MERCADO (ABAS AVANÇADAS)
# ==============================================================================
st.markdown("### 🧠 Inteligência & Analytics")
tab1, tab2, tab3 = st.tabs(["🔮 Monte Carlo (Probabilidade)", "📅 Sazonalidade & Basis", "🤖 AI Advisor (Relatório)"])

# --- TAB 1: MONTE CARLO ---
with tab1:
    col_mc1, col_mc2 = st.columns([1, 2])
    with col_mc1:
        st.markdown("**Parâmetros da Simulação**")
        volatilidade = st.slider("Volatilidade do Mercado (%)", 10, 40, 18, help="O quanto o preço oscila historicamente")
        n_sim = 5000
        
        if st.button("🔄 Rodar Simulação (5.000 cenários)"):
            cenarios = np.random.normal(preco_mercado, preco_mercado * (volatilidade/100), n_sim)
            resultados = []
            for p in cenarios:
                rec_total = receita_ja_garantida + (qtd_aberta * p)
                lucro = rec_total - custo_total_safra
                m = (lucro / custo_total_safra) * 100
                resultados.append(m)
            
            resultados = np.array(resultados)
            prob_lucro = np.mean(resultados > 0) * 100
            prob_meta = np.mean(resultados >= margem_desejada) * 100
            
            st.session_state['mc_results'] = resultados
            st.session_state['prob_lucro'] = prob_lucro
            st.session_state['prob_meta'] = prob_meta
            st.session_state['mc_run'] = True

    with col_mc2:
        if 'mc_run' in st.session_state:
            # Cards de Probabilidade
            kpi1, kpi2 = st.columns(2)
            kpi1.metric("Probabilidade de Lucro", f"{st.session_state['prob_lucro']:.1f}%")
            kpi2.metric("Chance de Bater a Meta", f"{st.session_state['prob_meta']:.1f}%", delta="Risco calculado" if st.session_state['prob_meta'] > 50 else "Alto Risco")
            
            # Histograma
            fig_hist = px.histogram(st.session_state['mc_results'], nbins=50, title="Distribuição de Probabilidade da Margem Final")
            fig_hist.add_vline(x=margem_desejada, line_dash="dash", line_color="green", annotation_text="Meta")
            fig_hist.add_vline(x=0, line_color="red", annotation_text="Zero")
            fig_hist.update_layout(showlegend=False, xaxis_title="Margem Final (%)", template="plotly_white", height=300)
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Clique em 'Rodar Simulação' para ver as probabilidades.")

# --- TAB 2: SAZONALIDADE ---
with tab2:
    st.markdown("**Comportamento Histórico (Sazonalidade de Preços - Soja Brasil)**")
    
    # Gerando dados sintéticos realistas para Soja (Safra BR: Baixa em Março, Alta em Nov)
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    # Curva padrão de sazonalidade (Indexada: 100 = média)
    # Março/Abril = Colheita (Preço cai) -> Index ~90
    # Out/Nov = Entressafra (Preço sobe) -> Index ~110
    sazonalidade_index = [102, 98, 92, 90, 93, 97, 100, 103, 105, 108, 110, 106]
    
    # Aplicando ao preço atual para projetar
    preco_medio_ref = preco_mercado
    projecao_sazonal = [p * (preco_medio_ref/100) for p in sazonalidade_index] # Ajuste grosseiro apenas visual
    
    fig_saz = go.Figure()
    fig_saz.add_trace(go.Bar(x=meses, y=sazonalidade_index, name="Índice Sazonal", marker_color='#81C784'))
    fig_saz.add_trace(go.Scatter(x=meses, y=sazonalidade_index, mode='lines+markers', line=dict(color='#2E7D32', width=3), name="Tendência"))
    
    # Linha do momento atual (Mês atual fictício ou real)
    mes_atual_idx = datetime.now().month - 1
    fig_saz.add_vline(x=mes_atual_idx, line_dash="dash", line_color="red", annotation_text="Estamos Aqui")
    
    fig_saz.update_layout(
        title="Índice de Sazonalidade (5 Anos)",
        yaxis_title="Força do Preço (Index 100 = Média)",
        template="plotly_white",
        height=350
    )
    st.plotly_chart(fig_saz, use_container_width=True)
    st.caption("Nota: Dados ilustrativos baseados no comportamento padrão da soja no Brasil (Pressão de colheita vs Entressafra).")

# --- TAB 3: AI ADVISOR ---
with tab3:
    st.markdown("### 🤖 AgroStrategy AI Advisor")
    st.markdown("_Análise automática gerada com base nos seus parâmetros._")
    
    # LÓGICA DO "MOCK AI" (Gerador de texto condicional)
    recomendacao = ""
    status_risco = ""
    
    # 1. Análise de Exposição
    if exposicao_perc > 70:
        texto_exposicao = "Sua exposição ao mercado spot está **muito alta (>70%)**. Isso aumenta drasticamente a volatilidade do seu resultado."
        acao_exposicao = "Recomendamos fortemente avançar travas de hedge para reduzir incerteza."
    elif exposicao_perc > 40:
        texto_exposicao = "Sua exposição está moderada. Você tem espaço para participar de altas, mas já garantiu parte dos custos."
        acao_exposicao = "Monitore o 'Basis' para oportunidades pontuais de venda."
    else:
        texto_exposicao = "Você está em uma posição conservadora (Hedge alto). Seu risco de baixa de preços é mínimo."
        acao_exposicao = "Aguarde picos de mercado para vender o saldo restante."

    # 2. Análise de Preço Alvo
    if preco_breakeven_saldo < preco_mercado:
        texto_preco = f"Boas notícias: O mercado atual (R$ {preco_mercado}) está **acima** do seu preço alvo (R$ {preco_breakeven_saldo:.2f})."
        conclusao = "🟢 **CENÁRIO FAVORÁVEL:** Você tem a faca e o queijo na mão. Vender agora garante sua meta e ainda gera lucro excedente."
    else:
        diff = preco_breakeven_saldo - preco_mercado
        texto_preco = f"Atenção: O mercado atual paga R$ {preco_mercado}, mas você precisa de R$ {preco_breakeven_saldo:.2f} para bater a meta. Gap de R$ {diff:.2f}."
        conclusao = "🔴 **CENÁRIO DESAFIADOR:** Vender tudo hoje frustraria sua meta de lucro. Considere usar Opções (Calls) se for vender o físico, ou aguarde a entressafra."

    # Renderizando o Relatório
    box_style = """
    background-color: #F1F8E9; border-left: 5px solid #2E7D32; padding: 15px; border-radius: 5px; margin-bottom: 10px;
    """
    
    st.markdown(f"""
    <div style="{box_style}">
        <h4>📋 Diagnóstico Executivo</h4>
        <p>{texto_exposicao} {texto_preco}</p>
        <p><strong>Ação Recomendada:</strong> {acao_exposicao}</p>
        <hr>
        <h3>{conclusao}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Este relatório foi gerado por lógica algorítmica baseada nos seus inputs. Para integrar com GPT-4 real, seria necessário uma chave de API.")

# ==============================================================================
# 5. RODAPÉ
# ==============================================================================
st.markdown("""
<div class="footer">
    AgroExposure v2.0 Beta · Powered by Intelligence · João Cunha
</div>
""", unsafe_allow_html=True)