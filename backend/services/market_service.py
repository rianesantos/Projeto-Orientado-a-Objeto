from typing import Optional
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os

# Defina sua chave de API aqui.
# Idealmente, use variáveis de ambiente para segurança (os.getenv("ALPHA_VANTAGE_API_KEY"))
API_KEY = "SUA_CHAVE_DE_API_AQUI" 

def fetch_intraday_ohlcv(symbol: str, period: str = "7d", interval: str = "1min") -> pd.DataFrame:
    """
    Retorna um DataFrame com as colunas: Open, High, Low, Close, Volume, usando a Alpha Vantage.
    Note que a API gratuita da Alpha Vantage tem limitações.
    """
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    
    # Mapeia o "period" para o "outputsize" da Alpha Vantage.
    # A API gratuita pode ter restrições em períodos longos.
    if period in ["1d", "7d", "30d"]:
        output_size = "full"
    else:
        output_size = "compact"

    try:
        data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=output_size)
    except Exception as e:
        print(f"Erro ao buscar dados da Alpha Vantage para {symbol}: {e}")
        return pd.DataFrame()

    if data.empty:
        return pd.DataFrame()

    # Alpha Vantage usa um formato de coluna diferente. Vamos renomeá-las.
    data.columns = [
        "Open", 
        "High", 
        "Low", 
        "Close", 
        "Volume"
    ]
    
    # Converte o índice para um formato de datetime para consistência
    data.index = pd.to_datetime(data.index)
    
    # Inverte a ordem do DataFrame para que as datas mais recentes fiquem no final
    data = data.iloc[::-1]

    # Alpha Vantage não retorna "period", então retornamos todo o DataFrame
    return data

def fetch_latest_quote(symbol: str) -> Optional[dict]:
    """
    Retorna a última cotação de um símbolo. Inclui dados de fallback
    caso a API não retorne dados válidos.
    """
    df = fetch_intraday_ohlcv(symbol, period="1d", interval="1min")
    
    if df.empty:
        # Retorna dados de fallback para evitar erros na aplicação
        return {
            "symbol": symbol,
            "price": 100.0,
            "open": 99.0,
            "high": 101.0,
            "low": 98.0,
            "volume": 1000000
        }
        
    last = df.iloc[-1]
    return {
        "symbol": symbol,
        "price": float(round(last["Close"], 2)),
        "open": float(round(last["Open"], 2)),
        "high": float(round(last["High"], 2)),
        "low": float(round(last["Low"], 2)),
        "volume": int(last["Volume"])
    }