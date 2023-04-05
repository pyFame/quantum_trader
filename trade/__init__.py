import pandas as pd

from utils.time_ops import to_date

from conf import client
def my_trades():
  df = pd.DataFrame(client.futures_account_trades())
  df['time'] = to_date(df['time'])
  return df

def position(hedge=True):
  client.futures_change_position_mode(dualSidePosition = hedge)
  return client.futures_get_position_mode()