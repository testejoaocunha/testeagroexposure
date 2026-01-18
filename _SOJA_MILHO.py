# pages/_SOJA_MILHO.py
# AgroExposure | Agro Premium — Consolidado Soja + Milho Safrinha
# Objetivo: visão executiva AUTOMÁTICA (sem campos editáveis), consolidando tudo que o usuário
# ajustou nas páginas SOJA e MILHO.
#
# Persistência: Session + JSON (agro_state.json)
# - Qualquer alteração feita em SOJA/MILHO fica gravada e aparece aqui automaticamente.
# - Se o app reiniciar, os últimos valores salvos são carregados.
#
# Conceito de área:
# - Área Física (ha)  = MAIOR área ocupada em uma safra (max(área soja, área milho))
# - Área Plantada no Ano (ha) = soma das duas (soja + milho), pois é 2ª safra (mesma área pode “rodar” 2x)

import json
import re
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ============================================================
# CONFIG + ESTILO GLOBAL (Premium Agro)
# ============================================================
st.set_page_config(page_title="SOJA + MILHO | Consolidado", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: #f6f3ee; }

.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

.premium-header{
  background: linear-gradient(135deg, #f7f3ea 0%, #ffffff 60%);
  border: 1px solid rgba(42,61,47,0.12);
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 10px 26px rgba(0,0,0,0.06);
  margin-bottom: 12px;
}
.premium-title{
  font-size: 34px; font-weight: 800; color:#1e2a24; margin:0;
}
.premium-sub{
  color:#4b5a52; margin-top:4px; font-size: 14px;
}

.kpi-grid{
  display: grid;
  grid-template-columns: repeat(6, minmax(160px, 1fr));
  gap: 12px;
  margin-top: 10px;
}
.kpi-card{
  background: #ffffff;
  border: 1px solid rgba(42,61,47,0.14);
  border-left: 6px solid #1b5e20;
  border-radius: 16px;
  padding: 12px 14px;
  box-shadow: 0 10px 18px rgba(0,0,0,0.06);
  min-height: 92px;
}
.kpi-top{ display:flex; align-items:center; gap:8px; color:#3a4a41; font-size: 12px; font-weight:700; }
.kpi-val{ font-size: 24px; font-weight: 900; color:#1e2a24; margin-top: 4px; }
.kpi-hint{ color:#5a6a61; font-size: 12px; margin-top: 4px; }

.section-card{
  background:#fff;
  border: 1px solid rgba(42,61,47,0.12);
  border-radius: 18px;
  padding: 14px 16px;
  box-shadow: 0 10px 22px rgba(0,0,0,0.05);
  margin-top: 12px;
}
.section-title{
  font-size: 18px; font-weight: 900; color:#1e2a24; margin: 0 0 8px 0;
}
.badge{
  display:inline-block;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(42,61,47,0.16);
  background: #f7f3ea;
  color:#2a3d2f;
  font-weight: 700;
}
.divider{ height:1px; background: rgba(42,61,47,0.10); margin: 10px 0 12px 0; }

.insight{
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid rgba(42,61,47,0.14);
  background: #fbfaf7;
}
.insight b{ color:#1e2a24; }
.positive{ color:#1b5e20; font-weight: 800; }
.negative{ color:#8b2c2c; font-weight: 800; }

.small{ font-size: 12px; color:#5a6a61; }

.footer{
  margin-top: 18px;
  color:#6a7a70;
  font-size: 12px;
  text-align:center;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ============================================================
# PERSISTÊNCIA (SESSÃO + JSON)
# ============================================================
STATE_FILE_NAME = "agro_state.json"


def _root_dir() -> Path:
    p = Path(__file__).resolve()
    if p.parent.name.lower() == "pages":
        return p.parent.parent
    return p.parent


STATE_FILE = _root_dir() / STATE_FILE_NAME


def _parse_date_like(v):
    if isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", v):
        try:
            return date.fromisoformat(v)
        except Exception:
            return v
    return v


def load_persisted_state():
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for k, v in data.items():
                    if k not in st.session_state:
                        st.session_state[k] = _parse_date_like(v)
        except Exception:
            pass
load_persisted_state()

# =======================
# Sidebar (Consolidado)
# =======================
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 6px 0;'>
            <div style='font-weight:900; letter-spacing:1px;'>AGROEXPOSURE</div>
            <div style='font-size:0.85rem; opacity:0.85;'>Gestão de Risco</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📊 Consolidado")
    if st.button("🔄 Recalcular (puxar dados salvos)", use_container_width=True, key="sm_recalc_btn"):
        for k in list(st.session_state.keys()):
            if k.startswith("soja_") or k.startswith("milho_"):
                del st.session_state[k]
        st.rerun()

    st.markdown("---")

# ============================================================
# FORMATADORES BR
# ============================================================

def fmt_brl(x: float) -> str:
    try:
        return "R$ " + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def fmt_int(x: float) -> str:
    try:
        return f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"


def fmt_ha(x: float) -> str:
    return f"{fmt_int(x)} ha"

def fmt_pct(x: float) -> str:
    try:
        return f"{x*100:,.1f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0,0%"


def _safe_float(x, default=0.0) -> float:
    try:
        if x is None:
            return float(default)
        return float(x)
    except Exception:
        return float(default)


def get(k: str, default):
    return st.session_state.get(k, default)


# ============================================================
# LEITURA DE INPUTS (SOJA / MILHO) — SEM CAMPOS EDITÁVEIS AQUI
# ============================================================

def read_soja() -> dict:
    return {
        "cultura": "SOJA",
        "simular_quebra": bool(get("soja_simular_quebra", False)),
        "perc_quebra": _safe_float(get("soja_perc_quebra", 20)) / 100.0,
        "area_propria": _safe_float(get("soja_area_propria_ha", 1000.0)),
        "area_arrendada": _safe_float(get("soja_area_arrendada_ha", 500.0)),
        "prod_sc_ha": _safe_float(get("soja_produtividade_sc_ha", 60.0)),
        "custo_op_ha": _safe_float(get("soja_custo_operacional_ha", 6000.0)),
        "pct_travado": _safe_float(get("soja_perc_travado_pct", 25.0)) / 100.0,
        "preco_travado": _safe_float(get("soja_preco_travado", 115.0)),
        "preco_mercado": _safe_float(get("soja_preco_mercado", 105.0)),
        "margem_alvo": _safe_float(get("soja_margem_alvo_pct", 20.0)) / 100.0,
        "fin_pct": _safe_float(get("soja_perc_financiado_pct", 30.0)) / 100.0,
        "juros_aa": _safe_float(get("soja_taxa_juros_aa_pct", 12.0)) / 100.0,
        "data_desembolso": get("soja_data_desembolso", date(2025, 8, 30)),
        "data_pagamento": get("soja_data_pagamento", date(2026, 4, 30)),
        "arr_sc_ha": _safe_float(get("soja_arrendamento_sc_ha", 15.0)),
        "insumos_pct": _safe_float(get("soja_perc_insumos_pct", 60.0)) / 100.0,
        "colheita_pct": _safe_float(get("soja_perc_colheita_pct", 20.0)) / 100.0,
        "p_entrada_pct": _safe_float(get("soja_pct_entrada_insumo_pct", 50.0)) / 100.0,
        "p2_pct": _safe_float(get("soja_pct_parc2_pct", 25.0)) / 100.0,
        "p2_data": get("soja_data_parc2", date(2026, 4, 30)),
        "p3_pct": _safe_float(get("soja_pct_parc3_pct", 25.0)) / 100.0,
        "p3_data": get("soja_data_parc3", date(2026, 5, 30)),
        "mes_plantio": int(_safe_float(get("soja_mes_plantio", 9), 9)),
        "mes_colheita": int(_safe_float(get("soja_mes_colheita", 4), 4)),
    }


def read_milho() -> dict:
    return {
        "cultura": "MILHO SAFRINHA",
        "simular_quebra": bool(get("milho_simular_quebra", False)),
        "perc_quebra": _safe_float(get("milho_perc_quebra", 20)) / 100.0,
        "area_propria": _safe_float(get("milho_area_propria_ha", 1000.0)),
        "area_arrendada": _safe_float(get("milho_area_arrendada_ha", 500.0)),
        "prod_sc_ha": _safe_float(get("milho_produtividade_sc_ha", 105.0)),
        "custo_op_ha": _safe_float(get("milho_custo_operacional_ha", 5400.0)),
        "pct_travado": _safe_float(get("milho_perc_travado_pct", 25.0)) / 100.0,
        "preco_travado": _safe_float(get("milho_preco_travado", 60.0)),
        "preco_mercado": _safe_float(get("milho_preco_mercado", 55.0)),
        "margem_alvo": _safe_float(get("milho_margem_alvo_pct", 20.0)) / 100.0,
        "fin_pct": _safe_float(get("milho_perc_financiado_pct", 30.0)) / 100.0,
        "juros_aa": _safe_float(get("milho_taxa_juros_aa_pct", 12.0)) / 100.0,
        "data_desembolso": get("milho_data_desembolso", date(2026, 1, 30)),
        "data_pagamento": get("milho_data_pagamento", date(2026, 8, 30)),
        # No milho, normalmente arrendamento = 0 (já pago na soja/ano). Campo existe, mas default 0.
        "arr_sc_ha": _safe_float(get("milho_arrendamento_sc_ha", 0.0)),
        "insumos_pct": _safe_float(get("milho_perc_insumos_pct", 60.0)) / 100.0,
        "colheita_pct": _safe_float(get("milho_perc_colheita_pct", 20.0)) / 100.0,
        "p_entrada_pct": _safe_float(get("milho_pct_entrada_insumo_pct", 50.0)) / 100.0,
        "p2_pct": _safe_float(get("milho_pct_parc2_pct", 25.0)) / 100.0,
        "p2_data": get("milho_data_parc2", date(2026, 7, 30)),
        "p3_pct": _safe_float(get("milho_pct_parc3_pct", 25.0)) / 100.0,
        "p3_data": get("milho_data_parc3", date(2026, 8, 30)),
        "mes_plantio": int(_safe_float(get("milho_mes_plantio", 2), 2)),
        "mes_colheita": int(_safe_float(get("milho_mes_colheita", 7), 7)),
    }


# ============================================================
# CÁLCULOS
# ============================================================

def blended_price(pct_travado: float, preco_travado: float, preco_mercado: float) -> float:
    pct_travado = max(0.0, min(1.0, pct_travado))
    return pct_travado * preco_travado + (1.0 - pct_travado) * preco_mercado


def days_between(d1: date, d2: date) -> int:
    try:
        return max(0, int((d2 - d1).days))
    except Exception:
        return 0


def compute_crop(inp: dict) -> dict:
    area_total = max(0.0, inp["area_propria"] + inp["area_arrendada"])

    prod_sc_ha = max(0.0, inp["prod_sc_ha"])
    if inp["simular_quebra"]:
        prod_sc_ha = prod_sc_ha * (1.0 - max(0.0, min(0.95, inp["perc_quebra"])))

    producao_sc = area_total * prod_sc_ha

    preco_med = blended_price(inp["pct_travado"], inp["preco_travado"], inp["preco_mercado"])
    receita = producao_sc * preco_med

    # Arrendamento (econômico) em reais (sc/ha * área arrendada * preço médio)
    arr_sc_total = max(0.0, inp["area_arrendada"]) * max(0.0, inp["arr_sc_ha"])
    arr_custo = arr_sc_total * preco_med

    custo_op_total = area_total * max(0.0, inp["custo_op_ha"])
    custo_insumos = custo_op_total * max(0.0, min(1.0, inp["insumos_pct"]))
    custo_colheita = custo_op_total * max(0.0, min(1.0, inp["colheita_pct"]))
    custo_outros = max(0.0, custo_op_total - custo_insumos - custo_colheita)

    # Financiamento (custeio) — base simplificada: % do custo operacional
    principal_fin = custo_op_total * max(0.0, min(1.0, inp["fin_pct"]))
    dias = days_between(inp["data_desembolso"], inp["data_pagamento"])
    juros = principal_fin * max(0.0, inp["juros_aa"]) * (dias / 365.0)

    custo_total = custo_op_total + arr_custo + juros
    lucro = receita - custo_total

    margem = (lucro / receita) if receita > 0 else 0.0
    lucro_ha = (lucro / area_total) if area_total > 0 else 0.0

    custo_sc = (custo_total / producao_sc) if producao_sc > 0 else 0.0
    breakeven = custo_sc  # R$/sc para ficar 0x0

    # Preço necessário para atingir a margem alvo
    m_alvo = max(0.0, min(0.8, inp["margem_alvo"]))
    receita_req = custo_total / max(1e-9, (1.0 - m_alvo))
    preco_req = (receita_req / producao_sc) if producao_sc > 0 else 0.0

    # Exposição spot
    pct_spot = max(0.0, 1.0 - max(0.0, min(1.0, inp["pct_travado"])))

    return {
        "cultura": inp["cultura"],
        "area_total": area_total,
        "area_propria": inp["area_propria"],
        "area_arrendada": inp["area_arrendada"],
        "prod_sc_ha": prod_sc_ha,
        "producao_sc": producao_sc,
        "preco_medio": preco_med,
        "receita": receita,
        "arr_sc_total": arr_sc_total,
        "arr_custo": arr_custo,
        "custo_op_total": custo_op_total,
        "custo_insumos": custo_insumos,
        "custo_colheita": custo_colheita,
        "custo_outros": custo_outros,
        "principal_fin": principal_fin,
        "juros": juros,
        "dias": dias,
        "custo_total": custo_total,
        "lucro": lucro,
        "lucro_ha": lucro_ha,
        "margem": margem,
        "custo_sc": custo_sc,
        "breakeven": breakeven,
        "preco_req_margem": preco_req,
        "pct_travado": inp["pct_travado"],
        "pct_spot": pct_spot,
        "preco_travado": inp["preco_travado"],
        "preco_mercado": inp["preco_mercado"],
        "margem_alvo": inp["margem_alvo"],
        "data_desembolso": inp["data_desembolso"],
        "data_pagamento": inp["data_pagamento"],
        "mes_plantio": inp["mes_plantio"],
        "mes_colheita": inp["mes_colheita"],
        "p_entrada_pct": inp["p_entrada_pct"],
        "p2_pct": inp["p2_pct"],
        "p2_data": inp["p2_data"],
        "p3_pct": inp["p3_pct"],
        "p3_data": inp["p3_data"],
    }


def build_dre_table(res: dict) -> pd.DataFrame:
    receita = res["receita"]
    custo_op = res["custo_op_total"]
    arr = res["arr_custo"]
    juros = res["juros"]
    lucro = res["lucro"]

    # DRE Caixa (contábil simplificado)
    dre = [
        ("Receita Bruta (Vendas)", receita),
        ("(-) Custos Operacionais", -custo_op),
        ("(-) Arrendamento (econômico)", -arr),
        ("= Resultado Operacional (EBITDA*)", receita - custo_op - arr),
        ("(-) Juros do Custeio", -juros),
        ("= Lucro Líquido", lucro),
    ]

    df = pd.DataFrame(dre, columns=["Linha", "Valor (R$)"])
    return df


def kpi_card(title: str, value: str, hint: str = "", color: str = "#1b5e20"):
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color:{color};">
          <div class="kpi-top">{title}</div>
          <div class="kpi-val">{value}</div>
          <div class="kpi-hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_box(title: str, body_html: str):
    st.markdown(
        f"""
        <div class="insight">
          <div style="font-weight:900; margin-bottom:6px;">{title}</div>
          <div>{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# EXECUÇÃO
# ============================================================

inp_soja = read_soja()
inp_milho = read_milho()

res_soja = compute_crop(inp_soja)
res_milho = compute_crop(inp_milho)

# Consolidado
area_fisica = max(res_soja["area_total"], res_milho["area_total"])
area_plantada_ano = res_soja["area_total"] + res_milho["area_total"]

producao_total = res_soja["producao_sc"] + res_milho["producao_sc"]
receita_total = res_soja["receita"] + res_milho["receita"]
arr_total = res_soja["arr_custo"] + res_milho["arr_custo"]

custo_op_total = res_soja["custo_op_total"] + res_milho["custo_op_total"]
juros_total = res_soja["juros"] + res_milho["juros"]
custo_total = res_soja["custo_total"] + res_milho["custo_total"]
lucro_total = res_soja["lucro"] + res_milho["lucro"]

margem_total = (lucro_total / receita_total) if receita_total > 0 else 0.0
preco_medio_pond = (receita_total / producao_total) if producao_total > 0 else 0.0

# Métricas adicionais
roi_sobre_custo = (lucro_total / custo_total) if custo_total > 0 else 0.0
juros_pct_receita = (juros_total / receita_total) if receita_total > 0 else 0.0

# Meta consolidada (ponderada por receita)
meta_margem_pond = 0.0
if receita_total > 0:
    meta_margem_pond = (
        res_soja["margem_alvo"] * res_soja["receita"] + res_milho["margem_alvo"] * res_milho["receita"]
    ) / receita_total

# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="premium-header">
      <div class="premium-title">AgroExposure: Consolidado Soja + Milho Safrinha</div>
      <div class="premium-sub">
        Visão executiva automática (sem campos editáveis): KPIs, custos, financiamentos, DRE, risco e insights.
        <br/>
        <span class="small">Área Física = maior área ocupada em uma safra. Área Plantada no Ano = soma (2 safras). Tudo puxado automaticamente das páginas SOJA e MILHO.</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ============================================================
# KPI GRID (Consolidado)
# ============================================================

r1c1, r1c2, r1c3 = st.columns(3)
with r1c1:
    kpi_card(
        "📍 Área Física (máx.)",
        fmt_ha(area_fisica),
        f"Soja: {fmt_ha(res_soja['area_total'])} | Milho: {fmt_ha(res_milho['area_total'])}",
    )
with r1c2:
    kpi_card("🧾 Área Plantada no Ano", fmt_ha(area_plantada_ano), "Soja + Milho (2ª safra)", "#2a3d2f")
with r1c3:
    kpi_card(
        "🌾 Produção Total",
        f"{fmt_int(producao_total)} sc",
        f"Soja: {fmt_int(res_soja['producao_sc'])} | Milho: {fmt_int(res_milho['producao_sc'])}",
        "#1b5e20",
    )

r2c1, r2c2, r2c3 = st.columns(3)
with r2c1:
    kpi_card("💰 Preço Médio Ponderado", f"R$ {fmt_brl(preco_medio_pond)}/sc", "Receita / Produção", "#0b7285")
with r2c2:
    kpi_card(
        "📈 Receita Bruta",
        f"R$ {fmt_brl(receita_total)}",
        f"Soja: R$ {fmt_brl(res_soja['receita'])} | Milho: R$ {fmt_brl(res_milho['receita'])}",
        "#1f7a1f",
    )
with r2c3:
    kpi_card(
        "🧠 Lucro Líquido",
        f"R$ {fmt_brl(lucro_total)}",
        f"Margem: {fmt_pct(margem_total)} | ROI: {fmt_pct(roi_sobre_custo)}",
        "#14532d" if lucro_total >= 0 else "#8b2c2c",
    )

st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)


# ============================================================
# SEÇÃO: KPIs por cultura + comparativos
# ============================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📌 KPIs por Cultura</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

kpi_df = pd.DataFrame([
    {
        "Cultura": res_soja["cultura"],
        "Área (ha)": res_soja["area_total"],
        "Produtividade (sc/ha)": res_soja["prod_sc_ha"],
        "Produção (sc)": res_soja["producao_sc"],
        "Preço Médio (R$/sc)": res_soja["preco_medio"],
        "Receita (R$)": res_soja["receita"],
        "Custo Operacional (R$)": res_soja["custo_op_total"],
        "Arrendamento (R$)": res_soja["arr_custo"],
        "Juros (R$)": res_soja["juros"],
        "Custo Total (R$)": res_soja["custo_total"],
        "Lucro (R$)": res_soja["lucro"],
        "Lucro/ha (R$/ha)": res_soja["lucro_ha"],
        "Margem": res_soja["margem"],
        "Breakeven 0x0 (R$/sc)": res_soja["breakeven"],
        "Preço p/ Meta (R$/sc)": res_soja["preco_req_margem"],
        "% Travado": res_soja["pct_travado"],
    },
    {
        "Cultura": res_milho["cultura"],
        "Área (ha)": res_milho["area_total"],
        "Produtividade (sc/ha)": res_milho["prod_sc_ha"],
        "Produção (sc)": res_milho["producao_sc"],
        "Preço Médio (R$/sc)": res_milho["preco_medio"],
        "Receita (R$)": res_milho["receita"],
        "Custo Operacional (R$)": res_milho["custo_op_total"],
        "Arrendamento (R$)": res_milho["arr_custo"],
        "Juros (R$)": res_milho["juros"],
        "Custo Total (R$)": res_milho["custo_total"],
        "Lucro (R$)": res_milho["lucro"],
        "Lucro/ha (R$/ha)": res_milho["lucro_ha"],
        "Margem": res_milho["margem"],
        "Breakeven 0x0 (R$/sc)": res_milho["breakeven"],
        "Preço p/ Meta (R$/sc)": res_milho["preco_req_margem"],
        "% Travado": res_milho["pct_travado"],
    },
])

# Format friendly
show_df = kpi_df.copy()
for c in ["Área (ha)", "Produtividade (sc/ha)", "Produção (sc)"]:
    show_df[c] = show_df[c].apply(lambda v: fmt_int(v))
for c in ["Preço Médio (R$/sc)", "Breakeven 0x0 (R$/sc)", "Preço p/ Meta (R$/sc)"]:
    show_df[c] = show_df[c].apply(lambda v: fmt_brl(v))
for c in ["Receita (R$)", "Custo Operacional (R$)", "Arrendamento (R$)", "Juros (R$)", "Custo Total (R$)", "Lucro (R$)", "Lucro/ha (R$/ha)"]:
    show_df[c] = show_df[c].apply(lambda v: fmt_brl(v))
show_df["Margem"] = show_df["Margem"].apply(fmt_pct)
show_df["% Travado"] = show_df["% Travado"].apply(fmt_pct)

st.dataframe(show_df, use_container_width=True, hide_index=True)

# Comparativos
col_a, col_b = st.columns(2)

with col_a:
    fig = go.Figure(data=[
        go.Bar(name="Lucro/ha", x=["SOJA", "MILHO"], y=[res_soja["lucro_ha"], res_milho["lucro_ha"]]),
    ])
    fig.update_layout(title="Comparativo: Lucro Líquido por Hectare (R$/ha)", height=360, margin=dict(l=10,r=10,t=50,b=10))
    fig.update_yaxes(title="R$/ha")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    fig2 = go.Figure(data=[
        go.Bar(name="Margem", x=["SOJA", "MILHO"], y=[res_soja["margem"]*100, res_milho["margem"]*100]),
    ])
    fig2.update_layout(title="Comparativo: Margem Líquida (%)", height=360, margin=dict(l=10,r=10,t=50,b=10))
    fig2.update_yaxes(title="%")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# SEÇÃO: DRE CONSOLIDADO + DRE POR CULTURA
# ============================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📒 DRE (Contábil Simplificado) e Resultado Econômico</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# DRE consolidado
EBITDA = receita_total - custo_op_total - arr_total
juros = juros_total
lucro = lucro_total

# Indicadores
cobertura_juros = (EBITDA / juros) if juros > 0 else None

row = [
    ("Receita Bruta (Vendas)", receita_total),
    ("(-) Custos Operacionais (Soja+Milho)", -custo_op_total),
    ("(-) Arrendamento (econômico)", -arr_total),
    ("= EBITDA* (simplificado)", EBITDA),
    ("(-) Juros do Custeio", -juros_total),
    ("= Lucro Líquido Consolidado", lucro_total),
]

df_dre = pd.DataFrame(row, columns=["Linha", "Valor (R$)"])
show_dre = df_dre.copy()
show_dre["Valor (R$)"] = show_dre["Valor (R$)"].apply(fmt_brl)

c1, c2 = st.columns([1.2, 1])

with c1:
    st.dataframe(show_dre, use_container_width=True, hide_index=True)

with c2:
    # Waterfall
    figw = go.Figure(go.Waterfall(
        name="DRE",
        orientation="v",
        measure=["absolute", "relative", "relative", "total", "relative", "total"],
        x=["Receita", "Custos Op", "Arrendamento", "EBITDA", "Juros", "Lucro"],
        y=[receita_total, -custo_op_total, -arr_total, EBITDA, -juros_total, lucro_total],
        connector={"line": {"width": 1}},
    ))
    figw.update_layout(title="Waterfall do Resultado", height=420, margin=dict(l=10,r=10,t=50,b=10))
    st.plotly_chart(figw, use_container_width=True)

st.markdown(
    f"<div class='small'>*EBITDA aqui = Receita - Custos Operacionais - Arrendamento (não inclui depreciação/impostos). Juros total = {fmt_brl(juros_total)} ({fmt_pct(juros_pct_receita)} da receita).</div>",
    unsafe_allow_html=True,
)

# DRE por cultura (tabs)
t1, t2 = st.tabs(["DRE SOJA", "DRE MILHO"])
with t1:
    df = build_dre_table(res_soja).copy()
    df["Valor (R$)"] = df["Valor (R$)"].apply(fmt_brl)
    st.dataframe(df, use_container_width=True, hide_index=True)
with t2:
    df = build_dre_table(res_milho).copy()
    df["Valor (R$)"] = df["Valor (R$)"].apply(fmt_brl)
    st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# SEÇÃO: FINANCIAMENTO, JUROS E CALENDÁRIO
# ============================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏦 Financeiro & Liquidez (Custeio + Insumos)</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

fin_df = pd.DataFrame([
    {
        "Cultura": res_soja["cultura"],
        "Principal (base)": res_soja["principal_fin"],
        "Juros": res_soja["juros"],
        "Dias": res_soja["dias"],
        "Desembolso": res_soja["data_desembolso"].isoformat() if isinstance(res_soja["data_desembolso"], date) else str(res_soja["data_desembolso"]),
        "Pagamento": res_soja["data_pagamento"].isoformat() if isinstance(res_soja["data_pagamento"], date) else str(res_soja["data_pagamento"]),
        "% Travado": res_soja["pct_travado"],
        "Spot (exposição)": res_soja["pct_spot"],
    },
    {
        "Cultura": res_milho["cultura"],
        "Principal (base)": res_milho["principal_fin"],
        "Juros": res_milho["juros"],
        "Dias": res_milho["dias"],
        "Desembolso": res_milho["data_desembolso"].isoformat() if isinstance(res_milho["data_desembolso"], date) else str(res_milho["data_desembolso"]),
        "Pagamento": res_milho["data_pagamento"].isoformat() if isinstance(res_milho["data_pagamento"], date) else str(res_milho["data_pagamento"]),
        "% Travado": res_milho["pct_travado"],
        "Spot (exposição)": res_milho["pct_spot"],
    },
])

show_fin = fin_df.copy()
show_fin["Principal (base)"] = show_fin["Principal (base)"].apply(fmt_brl)
show_fin["Juros"] = show_fin["Juros"].apply(fmt_brl)
show_fin["% Travado"] = show_fin["% Travado"].apply(fmt_pct)
show_fin["Spot (exposição)"] = show_fin["Spot (exposição)"].apply(fmt_pct)

st.dataframe(show_fin, use_container_width=True, hide_index=True)

# Calendário (eventos)

def add_event(events, cultura, tipo, data_evt, valor):
    if not isinstance(data_evt, date):
        return
    events.append({"Data": data_evt, "Cultura": cultura, "Tipo": tipo, "Valor (R$)": valor})


def build_events(res: dict) -> list:
    events = []
    # Insumos pagos em 3 parcelas sobre o custo de insumos (aproximação)
    insumos_total = res["custo_insumos"]
    # Entrada: usamos 1º dia do mês de plantio no ano do desembolso
    try:
        ano_base = res["data_desembolso"].year if isinstance(res["data_desembolso"], date) else date.today().year
        data_plantio = date(ano_base, int(res["mes_plantio"]), 1)
    except Exception:
        data_plantio = None

    add_event(events, res["cultura"], "Insumos - Entrada", data_plantio, insumos_total * res["p_entrada_pct"])
    add_event(events, res["cultura"], "Insumos - P2", res["p2_data"], insumos_total * res["p2_pct"])
    add_event(events, res["cultura"], "Insumos - P3", res["p3_data"], insumos_total * res["p3_pct"])

    # Custeio: pagamento (principal + juros) na data de pagamento
    add_event(events, res["cultura"], "Custeio - Principal", res["data_pagamento"], res["principal_fin"])
    add_event(events, res["cultura"], "Custeio - Juros", res["data_pagamento"], res["juros"])

    return events


events = build_events(res_soja) + build_events(res_milho)

df_evt = pd.DataFrame(events)
if not df_evt.empty:
    df_evt = df_evt.sort_values("Data")
    df_evt["Data"] = df_evt["Data"].apply(lambda d: d.strftime("%d/%m/%Y") if isinstance(d, date) else str(d))
    df_evt["Valor (R$)"] = df_evt["Valor (R$)"].apply(fmt_brl)
    st.markdown("<div class='small'>Calendário aproximado de saídas (insumos + custeio). Serve como visão macro; detalhes finos permanecem nas páginas individuais.</div>", unsafe_allow_html=True)
    st.dataframe(df_evt, use_container_width=True, hide_index=True)
else:
    st.info("Ainda não há eventos suficientes para montar o calendário (abra as páginas SOJA e MILHO pelo menos uma vez).")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# SEÇÃO: RISCO, STRESS E INSIGHTS ("IA")
# ============================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧠 Inteligência & Analytics (insights automáticos)</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Ranking por rentabilidade
melhor = res_soja if res_soja["lucro_ha"] >= res_milho["lucro_ha"] else res_milho
pior = res_milho if melhor is res_soja else res_soja

# Drivers
msg_rank = (
    f"<b>Produto mais rentável por hectare:</b> <span class='positive'>{melhor['cultura']}</span><br/>"
    f"Diferença aproximada: <b>{fmt_brl(melhor['lucro_ha'] - pior['lucro_ha'])}/ha</b>."
)

# Alertas consolidados
alerts = []
if margem_total < meta_margem_pond:
    alerts.append(f"Margem consolidada ({fmt_pct(margem_total)}) abaixo da meta ponderada ({fmt_pct(meta_margem_pond)}).")

if juros_pct_receita > 0.03:
    alerts.append(f"Juros relevantes ({fmt_pct(juros_pct_receita)} da receita). Avalie prazo/volume financiado.")

# Break-even vs mercado
if res_soja["breakeven"] > res_soja["preco_medio"]:
    alerts.append(f"SOJA: preço médio ({fmt_brl(res_soja['preco_medio'])}/sc) abaixo do 0x0 ({fmt_brl(res_soja['breakeven'])}/sc).")
if res_milho["breakeven"] > res_milho["preco_medio"]:
    alerts.append(f"MILHO: preço médio ({fmt_brl(res_milho['preco_medio'])}/sc) abaixo do 0x0 ({fmt_brl(res_milho['breakeven'])}/sc).")

# Exposição spot
if res_soja["pct_spot"] > 0.6:
    alerts.append(f"SOJA: alta exposição ao spot ({fmt_pct(res_soja['pct_spot'])}).")
if res_milho["pct_spot"] > 0.6:
    alerts.append(f"MILHO: alta exposição ao spot ({fmt_pct(res_milho['pct_spot'])}).")

alert_html = "<ul>" + "".join([f"<li>{a}</li>" for a in alerts]) + "</ul>" if alerts else "<span class='positive'>Sem alertas críticos nos indicadores principais.</span>"

# Stress rápido: choque de preço -5% e produtividade -5%

def stress(res: dict, choque_preco=-0.05, choque_prod=-0.05):
    # aplica choques em preço médio e produtividade/produção (mantendo custos)
    receita_stress = res["receita"] * (1.0 + choque_preco) * (1.0 + choque_prod)
    lucro_stress = receita_stress - res["custo_total"]
    return lucro_stress

lucro_stress_p = stress({**res_soja, "receita": receita_total, "custo_total": custo_total}, -0.05, 0.0)
# acima: consolidado (apenas preço), depois preço+prod
lucro_stress_pp = stress({**res_soja, "receita": receita_total, "custo_total": custo_total}, -0.05, -0.05)

insights_left, insights_right = st.columns([1.2, 1])

with insights_left:
    insight_box("✅ Rank de Rentabilidade", msg_rank)

    insight_box(
        "🔎 Alertas & Pontos de Atenção",
        alert_html,
    )

with insights_right:
    insight_box(
        "⚡ Stress rápido (macro)",
        (
            f"<b>Preço -5%:</b> lucro estimado {fmt_brl(lucro_stress_p)}<br/>"
            f"<b>Preço -5% + Prod -5%:</b> lucro estimado {fmt_brl(lucro_stress_pp)}<br/>"
            "<span class='small'>Modelo linear: aplica choques apenas na receita (custos mantidos). Use o Stress Test completo nas páginas individuais.</span>"
        ),
    )

# Sensibilidade (mini) — qual driver pesa mais?
# Aproximação: variação de +R$1/sc no preço -> delta lucro = produção total
# variação de +1 sc/ha produtividade -> delta lucro = área total * preço médio

delta_preco_1 = producao_total * 1.0
avg_price = preco_medio_pond
avg_area = area_fisica if area_fisica > 0 else (res_soja["area_total"] + res_milho["area_total"])
delta_prod_1 = avg_area * avg_price

st.markdown(
    f"<div class='small'><b>Elasticidades (aprox.):</b> +R$ 1/sc no preço médio → +{fmt_brl(delta_preco_1)} no lucro; +1 sc/ha de produtividade média → +{fmt_brl(delta_prod_1)} no lucro.</div>",
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    """
    <div class="footer">
      AgroExposure • Agro Premium UI • Consolidado automático (SOJA + MILHO SAFRINHA) • Persistência: Sessão + JSON
    </div>
    """,
    unsafe_allow_html=True,
)
