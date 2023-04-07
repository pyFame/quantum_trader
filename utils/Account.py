from ctypes import Union
from typing import Optional

import pandas as pd
from icecream import ic

from conf import client, alog
from enums.Binance import FUTURES, SPOT
from utils import Pandas


def permissions():
    return client.get_account_api_permissions()


def wallet_futures(no_zero_bal=True):
    df = pd.DataFrame(client.futures_account_balance())
    df['balance'] = pd.to_numeric(df['balance'])
    # df = df.reset_index(drop=True)
    # df.reset_index(drop=True)
    df = df.set_index('asset')

    if no_zero_bal:
        df = df.loc[df['balance'] > 0]
    df.drop(['accountAlias'], axis=1, inplace=True)
    return df


def wallet_spot(coin='USDT'):
    df = pd.DataFrame(client.get_asset_balance(asset=coin), index=[0])
    for i in ['free', 'locked']: df[i] = pd.to_numeric(df[i])
    return df


def balance(coin: str = 'USDT', wallet_type: Union[FUTURES, SPOT] = FUTURES) -> float:
    b = 0.
    if wallet_type is FUTURES:
        df = wallet_futures()
        b = df.loc[df['asset'] == coin]['balance'].iloc[0]
    elif wallet_type is SPOT:
        b = wallet_spot(coin)['free'].iloc[0]
    else:
        raise ValueError(f"unsupported wallet_type {wallet_type}")
    return b


# Futures

def trades_futures():
    df = pd.DataFrame(client.futures_account_trades())
    df['time'] = Pandas.to_date(df['time'])
    return df


def position(hedge=True):
    client.futures_change_position_mode(dualSidePosition=hedge)
    return client.futures_get_position_mode()


def transfer_futures(amt: float = None, coin: str = 'USDT') -> Optional[dict, None]:
    """
    :param amt:float
    :param coin:str
    :return:
    if amt is None or 0 then the entire balance is transfered
    """
    src: Union[SPOT, FUTURES] = SPOT if amt > 0 else FUTURES

    src_mapping = {
        SPOT: 1,
        FUTURES: 2
    }

    amt = amt or balance(coin, src)

    if amt is None or amt == 0.:
        alog.warn(f"{src}-> amount must be greater than 0")
        ic(f"Transfer failed {src}: {amt}")
        return

    amt = abs(amt)
    # if amt is None or amt == 0:
    #     raise ValueError("amount must be greater than 0")

    res = client.futures_account_transfer(asset=coin, amount=amt, type=type)

    alog.debug(res)

    return res


def income_futures(profit: bool = True, pnl: bool = True) -> pd.DataFrame:
    df = pd.DataFrame(client.futures_income_history())
    df['income'] = pd.to_numeric(df['income'])
    df['date'] = Pandas.to_date(df['time'])
    df.drop(['time', 'tranId', 'info'], axis=1, inplace=True)
    df = df.sort_values(by=['date'], ascending=False)
    df = df.loc[df['incomeType'] == 'REALIZED_PNL'] if pnl else df
    df = df.loc[df['income'] > 0] if profit else df
    # df = df.loc[df['incomeType']!='TRANSFER']
    df['profit'] = df['income'].sum()
    return df
