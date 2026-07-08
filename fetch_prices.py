import requests
import psycopg2
import os
from datetime import datetime
import time

# Настройки подключения к PostgreSQL (из переменных окружения)
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "crypto_db")
DB_USER = os.getenv("DB_USER", "crypto_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "crypto_pass")

def get_db_connection():
    """Создаёт подключение к PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def create_table_if_not_exists():
    """Создаёт таблицу для хранения цен, если её нет."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            btc_usd NUMERIC(10, 2),
            eth_usd NUMERIC(10, 2)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def fetch_crypto_prices():
    """Запрашивает текущие цены с CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "btc_usd": data.get("bitcoin", {}).get("usd"),
            "eth_usd": data.get("ethereum", {}).get("usd")
        }
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None

def save_prices_to_db(btc_price, eth_price):
    """Сохраняет цены в базу данных."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO crypto_prices (btc_usd, eth_usd) VALUES (%s, %s);",
        (btc_price, eth_price)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"[{datetime.now()}] Данные сохранены: BTC={btc_price}, ETH={eth_price}")

if __name__ == "__main__":
    # Создаём таблицу, если её нет
    create_table_if_not_exists()
    
    # Получаем цены
    prices = fetch_crypto_prices()
    if prices and prices["btc_usd"] and prices["eth_usd"]:
        save_prices_to_db(prices["btc_usd"], prices["eth_usd"])
    else:
        print("Не удалось получить данные, пропускаем сохранение.")
