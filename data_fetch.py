import pandas as pd
import os
import requests
import json

def load_api_key():
    with open('config.json', 'r') as config_f:
        return json.load(config_f).get('api_key')

def load_request_params():
    with open('params.json', 'r') as params_f:
        return json.load(params_f)

def fetch_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
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

if __name__ == '__main__':
    fetch_crypto_data()