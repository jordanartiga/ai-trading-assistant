import pandas as pd
def get_today_news():
    data = {'Title': ['FOMC Rate Decision'], 'Impact': ['High'], 'Time': ['14:00 ET']}
    return pd.DataFrame(data)
def format_news_alert(news_df):
    return f"<div style='color:red;'><b>Breaking News:</b> {news_df.iloc[0]['Title']} (Impact: {news_df.iloc[0]['Impact']}) at {news_df.iloc[0]['Time']}</div>"