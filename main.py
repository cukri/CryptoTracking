import pandas as pd

from data_fetch import fetch_crypto_data
from data_engineering import capitalization_categories


def main():
    fetch_crypto_data()
    df = pd.read_csv('top_crypto.csv')
    df = capitalization_categories(df)
    print(df)

if __name__ == '__main__':
    main()