def apply_strategy_detection(df):
    df['Strategy'] = df.apply(lambda row: 'Breakout' if row['Prediction']=='Up' and row['Confidence']>85 else ('Reversal' if row['Prediction']=='Down' and row['Confidence']>75 else 'Observation'), axis=1)
    return df