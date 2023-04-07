from typing import Tuple, Union
import pandas as pd
import numpy as np

from . import Pandas
from .cache import Cache

from conf import client

from enums.Symbol import Symbol

from typing import Optional

from conf import client
import pandas as pd

from enums import Symbol
from enums.position import SHORT, LONG
from utils import Pandas

cache_precision = Cache(ttl=60 * 30, maxsize=50)  # TODO: change when scale,make this private

get_price = lambda symbol: float(client.futures_symbol_ticker(symbol=symbol)['price'])
market_price = lambda symbol: float(client.get_symbol_ticker(symbol=symbol)['price'])
min_q = lambda symbol: precision(symbol)[-1]
min_notional_q = lambda symbol, notional, qP: round(notional / get_price(symbol), qP) or pow(10, -qP)


def history(symbol: Symbol, interval='1m', start_str='1 day ago', end_str=None) -> pd.DataFrame:
    data = client.futures_historical_klines(
        symbol=symbol,
        interval=interval,  # can play with this e.g. '1h', '4h', '1w', etc.
        start_str=start_str,
        end_str=end_str
    )
    df = pd.DataFrame(data)
    df = df.iloc[:, :6]

    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    # convert timestamp to date format and ensure ohlcv are all numeric
    df['date'] = Pandas.to_date(df['date'])

    df.set_index('date', inplace=True)

    # df['date'] = df.index #TODO: is this required!
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col])
    return df


def exchange(symbol: Symbol = None) -> pd.DataFrame:
    quote = symbol.quote if symbol else "USDT"

    info = client.futures_exchange_info()
    df = pd.DataFrame(info['symbols'])
    df = Pandas.filter_df(df, 'contractType', 'PERPETUAL')  # TODO: should be flexible
    df = Pandas.filter_df(df, 'quoteAsset', quote)

    df.drop(['pair', 'deliveryDate', 'onboardDate', 'contractType', 'status', 'quoteAsset', 'marginAsset',
             'timeInForce', 'orderTypes', 'settlePlan', 'underlyingSubType', 'underlyingType', 'liquidationFee'],
            axis=1, inplace=True)

    if symbol is None:
        return df

    return df.loc[df['symbol'] == symbol]


def precision(symbol: Symbol, cache=True) -> Tuple[int, int, int, int, float, float, float]:
    if cache:
        _precision = cache_precision.get(symbol)

        if isinstance(_precision, (tuple, list)):
            return _precision

    e = exchange(symbol)

    res = [int(i) for i in
           e.iloc[0, 4:8].to_list()]  # pricePrecision   quantityPrecision   baseAssetPrecision  quotePrecision

    _filter_df = pd.DataFrame(e['filters'].iloc[0])
    num_cols = [i for i in _filter_df.columns if i != 'filterType']
    for i in num_cols:
        _filter_df[i] = Pandas.pd.to_numeric(_filter_df[i])

    _filter_df['notional'] = _filter_df['notional'].apply(lambda x: min_notional_q(symbol, x, res[1]))

    d = {'PRICE_FILTER': ['minPrice', 'maxPrice'], 'MIN_NOTIONAL': ['notional']}

    for name, filters in d.items():
        f_df = Pandas.filter_df(_filter_df, 'filterType', name)
        res += Pandas.pluck_row(f_df, *filters)

    cache_precision.set(symbol, res)

    return res


def positions(symbol: Symbol = None, pos: Union[LONG, SHORT] = None) -> pd.DataFrame:
    data = client.futures_position_information()
    df = pd.DataFrame(data)
    cols = ['positionAmt', 'entryPrice', 'markPrice', 'unRealizedProfit', 'liquidationPrice', 'leverage',
            'isolatedWallet']

    df.drop(['updateTime'], axis=1, inplace=True)

    for col in cols:
        df[col] = pd.to_numeric(df[col])

    df = Pandas.filter_df(df, 'symbol', symbol) if symbol else df.loc[df['positionAmt'] > 0]
    df = Pandas.filter_df(df, 'positionSide', pos) if pos else df
    df['positionAmt'] = df['positionAmt'].apply(abs)
    return df


def open_orders(symbol: Symbol) -> Optional[pd.DataFrame]:
    data = client.futures_get_open_orders(symbol=symbol)
    if len(data) == 0:
        return
    df = pd.DataFrame(data)
    df['date'] = pd.to_numeric(df['time'])
    # df.drop(['updateTime','time','cumQuote','price','avgPrice','origQty','executedQty','status'],axis=1,inplace=True)
    return df
