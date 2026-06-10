# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Streamlit dashboard for Brazilian stock market analysis (PETR4, ITUB4, VALE3), tracking data since January 2025 via Yahoo Finance.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Architecture

Two-file structure with a clear separation of concerns:

- **`data_fetcher.py`** — data layer. Fetches OHLCV data from Yahoo Finance (`yfinance`), computes cumulative performance, and produces per-ticker summary metrics (price, YTD return, high/low). The `TICKERS` dict maps display names to Yahoo Finance symbols (`*.SA` suffix for B3).
- **`app.py`** — presentation layer. Streamlit app that calls `data_fetcher` functions and renders three Plotly charts: closing price, cumulative performance (%), and monthly average volume.

## GitHub Repository

- **Repositório:** https://github.com/rferreirarocha/stoa-stock-dashboard
- **Branch principal:** `main`

### Sync automático

Toda alteração feita via Claude Code (Edit ou Write) é automaticamente commitada e enviada ao GitHub. O hook está configurado em `.claude/settings.json` e executa:

```
git add -A → git commit -m "Auto-sync: <timestamp>" → git push
```

Para commits manuais fora do Claude Code:
```bash
git add -A
git commit -m "mensagem"
git push
```

## Key Conventions

- Ticker display names (`"Petrobras"`, `"Itaú"`, `"Vale"`) are defined once in `data_fetcher.TICKERS` and flow through both layers — columns are renamed at fetch time so `app.py` never references raw Yahoo symbols.
- Brand colors are defined in `app.py`'s `cores` dict and applied consistently across all three charts.
- Data is fetched fresh on every page load (no caching). If performance becomes an issue, `@st.cache_data` can be added to `get_stock_data`.
