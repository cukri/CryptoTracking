from datetime import datetime
import pandas as pd
import os
import requests
import json
import time

def load_config(config_path = 'config.json'):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"No configuration file: {config_path}")
    with open('config.json', 'r') as config_f:
        config = json.load(config_f)
    return config

config = load_config()
BASE_URL = config.get('url')
COINS_URL = config.get("coins_url")


def load_request_params():
    with open('top_params.json', 'r') as params_f:
        return json.load(params_f)

def load_crypto_list(path='crypto_list.json'):
    with open(path, 'r') as crypto_list_f:
        list = json.load(crypto_list_f)
    return list['cryptocurrencies']




def fetch_top_crypto_data():

    url = f'{BASE_URL}'
    params = load_request_params()

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame([{"name": coin["name"],
            "symbol": coin['symbol'],
            "current_price": coin["current_price"],'market_cap': coin['market_cap'],
            'price_change_percentage_24h': coin['price_change_percentage_24h']
        }for coin in data])

        df.sort_values(by='market_cap', ascending=False, inplace=True)
        df.to_csv('top_crypto.csv', index=False)
        print('Data saved to top_crypto.csv')
        print(df.head())

    else:
        print(f'Error request: {response.status_code}')
        print(response.text)


def fetch_historical_data(start = None, end = None):
    crypto_ids = load_crypto_list()

    if start is None or end is None:
        today = datetime.today().strftime('%Y-%m-%d')
        start = end = today
    else:
        if isinstance(start, str):
                start = datetime.strptime(start, "%Y-%m-%d")
        if isinstance(end, str):
                end = datetime.strptime(end, "%Y-%m-%d")

    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')
    start_timestamp = int(start_dt.timestamp())
    end_timestamp = int(end_dt.timestamp())


    for coin_id in crypto_ids:
        url = f'{COINS_URL}/{coin_id}/market_chart/range'
        params = {
            "vs_currency" : "usd",
            "from": start_timestamp,
            "to": end_timestamp
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            prices = data.get('prices', [])
            df = pd.DataFrame(prices, columns=['timestamp','price'])
            df.to_csv(f'{coin_id}_historical.csv', index=False)
            print(f'{coin_id} data saved.')
        else:
            print(f'Failed to fetch data for {coin_id}: {response.status_code}')

        time.sleep(1.5)
