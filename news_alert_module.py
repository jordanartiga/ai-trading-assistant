import pandas as pd
def get_today_news():
    data = {'Title': ['No Major News'], 'Impact': ['Low'], 'Time': ['--']}
    return pd.DataFrame(data)

def format_news_alert(news_df):
    return "<p>Sample News Alert</p>"