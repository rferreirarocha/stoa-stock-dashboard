import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from data_fetcher import get_stock_data, calcular_performance, metricas_resumo

st.set_page_config(page_title="Ações 2025", page_icon="📈", layout="wide")

st.title("📈 Análise de Ações — 2025")
st.caption(
    f"Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3) · "
    f"Atualizado em {date.today().strftime('%d/%m/%Y')}"
)

with st.spinner("Buscando dados do Yahoo Finance..."):
    close, volume = get_stock_data(start="2025-01-01")

if close.empty:
    st.error("Não foi possível obter os dados. Verifique sua conexão e tente novamente.")
    st.stop()

performance = calcular_performance(close)
resumo = metricas_resumo(close)

# ── Métricas resumidas ─────────────────────────────────────────────────────────
st.subheader("Resumo do Ano")
cols = st.columns(3)
cores = {"Petrobras": "#009B3A", "Itaú": "#003087", "Vale": "#0066B3"}

for col, (nome, dados) in zip(cols, resumo.items()):
    variacao = dados["variacao_ano"]
    sinal = "+" if variacao >= 0 else ""
    with col:
        st.metric(
            label=nome,
            value=f"R$ {dados['preco_atual']:.2f}",
            delta=f"{sinal}{variacao:.2f}% no ano",
        )
        st.caption(f"Máx: R$ {dados['maximo']:.2f}  |  Mín: R$ {dados['minimo']:.2f}")

st.divider()

# ── Gráfico 1: Preço de Fechamento ────────────────────────────────────────────
st.subheader("Preço de Fechamento (R$)")
fig_preco = go.Figure()
for nome in close.columns:
    fig_preco.add_trace(
        go.Scatter(
            x=close.index,
            y=close[nome],
            name=nome,
            line=dict(color=cores[nome], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + nome + "</extra>",
        )
    )
fig_preco.update_layout(
    xaxis_title="Data",
    yaxis_title="R$",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    height=420,
    margin=dict(t=20),
)
st.plotly_chart(fig_preco, use_container_width=True)

# ── Gráfico 2: Performance Acumulada ──────────────────────────────────────────
st.subheader("Performance Acumulada (%)")
fig_perf = go.Figure()
fig_perf.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
for nome in performance.columns:
    fig_perf.add_trace(
        go.Scatter(
            x=performance.index,
            y=performance[nome],
            name=nome,
            line=dict(color=cores[nome], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>%{y:.2f}%<extra>" + nome + "</extra>",
        )
    )
fig_perf.update_layout(
    xaxis_title="Data",
    yaxis_title="Retorno (%)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    height=420,
    margin=dict(t=20),
)
st.plotly_chart(fig_perf, use_container_width=True)

# ── Gráfico 3: Volume Médio Mensal ────────────────────────────────────────────
st.subheader("Volume Médio Mensal Negociado")
volume_mensal = volume.resample("ME").mean()
volume_mensal.index = volume_mensal.index.strftime("%b/%Y")

fig_vol = go.Figure()
for nome in volume_mensal.columns:
    fig_vol.add_trace(
        go.Bar(
            x=volume_mensal.index,
            y=volume_mensal[nome],
            name=nome,
            marker_color=cores[nome],
            hovertemplate="%{x}<br>Vol médio: %{y:,.0f}<extra>" + nome + "</extra>",
        )
    )
fig_vol.update_layout(
    barmode="group",
    xaxis_title="Mês",
    yaxis_title="Volume médio (negociações)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=420,
    margin=dict(t=20),
)
st.plotly_chart(fig_vol, use_container_width=True)
