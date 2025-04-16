import pandas as pd
import argparse
from data_fetch import fetch_top_crypto_data, fetch_historical_data
from data_engineering import capitalization_categories


def main():
    #fetch_top_crypto_data()
    #df = pd.read_csv('top_crypto.csv')
    #df = capitalization_categories(df)
   # print(df)
    fetch_historical_data()

if __name__ == '__main__':
    main()