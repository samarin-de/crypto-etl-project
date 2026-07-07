import requests
import json
from datetime import datetime

def fetch_crypto_prices():
    """
    Запрашивает текущие цены BTC и ETH с CoinGecko API.
    Возвращает словарь с ценами и временем запроса.
    """
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=usd"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Если статус не 200  вызовет исключение
        data = response.json()
        
        prices = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "btc_usd": data.get("bitcoin", {}).get("usd", None),
            "eth_usd": data.get("ethereum", {}).get("usd", None)
        }
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None

if __name__ == "__main__":
    prices = fetch_crypto_prices()
    if prices:
        print(f"[{prices['timestamp']}] BTC: {prices['btc_usd']} USD, ETH: {prices['eth_usd']} USD")
    else:
        print("Не удалось получить данные.")
