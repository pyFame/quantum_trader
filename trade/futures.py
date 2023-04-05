from utils.pandas_ops import to_date
from conf.binance_client import client
import pandas as pd
def my_trades():
  df = pd.DataFrame(client.futures_account_trades())
  df['time'] = to_date(df['time'])
  return df

def position(hedge=True):
  client.futures_change_position_mode(dualSidePosition = hedge)
  return client.futures_get_position_mode()

def open_orders(coin=''):
  data = client.futures_get_open_orders(symbol=symboler(coin))
  if len(data)==0: return -1
  df = pd.DataFrame(data)
  df['date'] = to_date(df['time'])
  # df.drop(['updateTime','time','cumQuote','price','avgPrice','origQty','executedQty','status'],axis=1,inplace=True)
  return df

def positions(coin='',pos=''):
  data = client.futures_position_information()
  df = pd.DataFrame(data)
  cols = ['positionAmt','entryPrice','markPrice','unRealizedProfit','liquidationPrice','leverage','isolatedWallet']
  drop_cols(df,'updateTime')
  for col in cols: df[col] = num_col(df[col])
  df = filter_df(df,'symbol',symboler(coin)) if coin else  df.loc[df['positionAmt']>0]
  df = filter_df(df,'positionSide',pos) if pos else df
  df['positionAmt'] = df['positionAmt'].apply(abs) #SHORT side amounts are neg
  return df