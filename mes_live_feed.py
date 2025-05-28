import pandas as pd
def get_live_mes_data():
    data = {'Time': pd.date_range(start=pd.Timestamp.now(), periods=15, freq='T'),'Open': [4170+i for i in range(15)],'High': [4171+i for i in range(15)],'Low': [4169+i for i in range(15)],'Close': [4170.5+i for i in range(15)],'Volume': [100 + i*10 for i in range(15)]}
    return pd.DataFrame(data)