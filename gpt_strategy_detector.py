def apply_strategy_detection(df):
    df['Strategy'] = df['Prediction'].apply(lambda x: 'Sample Strategy')
    return df