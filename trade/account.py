from conf.client import  client
import pandas as pd

from utils.pandas_ops import *

def status():
  import sys

  status_code = client.get_system_status()['status']
  if(status_code!=0):
     print("Exiting")
     sys.exit(1)

def permissions():
  return client.get_account_api_permissions()


def wallet():
  df = pd.DataFrame(client.futures_account_balance())
  df['balance'] = num_col(df['balance'])
  # df = df.loc[df['balance']>0]
  # df = df.reset_index(drop=True)
  df.drop(['accountAlias'],axis=1,inplace=True)
  return df

def wallet_spot(coin='USDT'):
  df = pd.DataFrame(client.get_asset_balance(asset=coin),index=[0])
  for i in ['free','locked']: df[i] = num_col(df[i])
  return df

def balance(coin='USDT',type='FUT'):
  b=0
  if type=='FUT':
    df = wallet()
    b = df.loc[df['asset']==coin]['balance'].iloc[0]
  elif type =='SPOT':
    b = wallet_spot(coin)['free'].iloc[0]
  return b


def transfer_to(dest='SPOT',amt=0,coin='USDT'):
  if dest=='SPOT':
    type =2
    src = 'FUT'
  else:
    type =1
    src = "SPOT"
  amt = amt or balance(coin,type=src)
  if amt>0:
    return client.futures_account_transfer(asset=coin,amount=amt,type=type)
  bLog.error(f"Transfer failed {src}->{dest} {amt}")
  return -1

def income(profit=True, pnl=True):
  df = pd.DataFrame(client.futures_income_history())
  df['income'] = num_col(df['income'])
  df['date'] = to_date(df['time'])
  drop_cols(df,'time','tranId','info')
  df = df.sort_values(by=['date'],ascending=False)
  df =  df.loc[df['incomeType']=='REALIZED_PNL'] if pnl else df
  df = df.loc[df['income']>0] if profit else df
  # df = df.loc[df['incomeType']!='TRANSFER']
  df['profit'] = df['income'].sum()
  return df

wallet()