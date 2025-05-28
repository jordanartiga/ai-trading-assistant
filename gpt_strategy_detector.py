def apply_strategy_detection(df):
    df['Strategy'] = df['Prediction'].apply(lambda x: 'Final Sample Strategy')
    return df