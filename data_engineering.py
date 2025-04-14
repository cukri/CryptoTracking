def capitalization_categories(df):
    df = df.copy()

    df['capitalization_category'] = df['market_cap'].apply(
        lambda x: ('mega-cap' if x > 10000000000 else
                   'large-cap' if x > 2000000000 else
                   'mid-cap' if x> 300000000 else
                   'small-cap')
    )

    return df