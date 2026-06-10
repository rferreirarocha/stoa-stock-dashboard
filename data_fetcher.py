import yfinance as yf
import pandas as pd

TICKERS = {
    "Petrobras": "PETR4.SA",
    "Itaú": "ITUB4.SA",
    "Vale": "VALE3.SA",
}


def get_stock_data(start="2025-01-01", end=None):
    tickers = list(TICKERS.values())
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)

    close = raw["Close"].copy()
    close.columns = list(TICKERS.keys())

    volume = raw["Volume"].copy()
    volume.columns = list(TICKERS.keys())

    return close, volume


def calcular_performance(close: pd.DataFrame) -> pd.DataFrame:
    primeiro_valor = close.iloc[0]
    return ((close - primeiro_valor) / primeiro_valor * 100).round(2)


def metricas_resumo(close: pd.DataFrame) -> dict:
    resumo = {}
    for nome in close.columns:
        serie = close[nome].dropna()
        primeiro = serie.iloc[0]
        ultimo = serie.iloc[-1]
        resumo[nome] = {
            "preco_atual": round(ultimo, 2),
            "variacao_ano": round((ultimo - primeiro) / primeiro * 100, 2),
            "maximo": round(serie.max(), 2),
            "minimo": round(serie.min(), 2),
        }
    return resumo
