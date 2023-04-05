from . import client
import pandas as pd
from utils.coin import *
def history(coin,interval='1m',start_str='7 day ago'):
  data = client.futures_historical_klines(
    symbol=symboler(coin),
    interval=interval,  # can play with this e.g. '1h', '4h', '1w', etc.
    start_str = start_str,
    # end_str='2021-06-30'
)
  df = pd.DataFrame(data)
  # crop unnecessary columns
  df = df.iloc[:, :6]
  # ascribe names to columns
  df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
  # convert timestamp to date format and ensure ohlcv are all numeric
  df['date'] = to_date(df['date'])
  for col in df.columns[1:]:
      df[col] = pd.to_numeric(df[col])
  return df

def make_history(df): #multable so no issues
  df['cap']= df['high'].mean()  #cap can be increasing sequence...
  df['floor'] = df['low'].min()
  df.drop(['volume','open','high','low','volume'],axis=1,inplace=True)     #only low
  df.columns = ['ds','y','cap','floor']
  return df