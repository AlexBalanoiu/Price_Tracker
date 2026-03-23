import requests
import psycopg2
import os
from dotenv import load_dotenv

def fetch_and_store():
    load_dotenv()

    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS")
    }

    API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_last_updated_at=true"

    try:
        print("Fetching data from CoinGecko...")
        response = requests.get(API_URL)
        data = response.json()

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for coin, values in data.items():
            cur.execute(
                """
                INSERT INTO coin_prices (coin_name, price_usd, last_updated_at)
                VALUES (%s, %s, TO_TIMESTAMP(%s))
                """,
                (coin, values['usd'], values['last_updated_at'])
            )

        conn.commit()
        print(f"Successfully stored {len(data)} coins.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()