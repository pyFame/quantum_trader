from utils.coin import symboler
from . import client
import pandas as pd

get_price = lambda coin: float(client.futures_symbol_ticker(symbol=symboler(coin))['price'])
market_price = lambda coin: float(client.get_symbol_ticker(symbol=symboler(coin))['price'])
min_q = lambda coin: precision(coin)[-1]
_min_q = lambda coin, notional, qP: round(notional / get_price(coin), qP) or pow(10, -qP)  # .001


def leverage_bracket(coin):
    data = client.futures_leverage_bracket(symbol=coin)[0]
    df = pd.DataFrame(data['brackets'])
    return df


def max_leverage(coin):
    df = leverage_bracket(coin)
    return df['initialLeverage'].max()


def leverage(coin, lev=''):
    lev = lev if lev else max_leverage(coin)
    return client.futures_change_leverage(symbol=coin, leverage=lev)


def order_book(coin='BTC'):
    data = client.futures_order_book(symbol=coin)
    return data


def recent_trades(coin):  # aggrefate
    data = client.futures_aggregate_trades(symbol=coin, limit=1000)
    df = pd.DataFrame(data)
    df['price'] = num_col(df['p'])
    return df


def precision(coin):
    e = exchange(coin)
    res = [int(i) for i in
           e.iloc[0, 4:8].to_list()]  # pricePrecision   quantityPrecision   baseAssetPrecision  quotePrecision

    filter = pd.DataFrame(e['filters'].iloc[0])
    num_cols = [i for i in filter.columns if i != 'filterType']
    for i in num_cols: filter[i] = num_col(filter[i])
    filter['notional'] = filter['notional'].apply(lambda x: _min_q(coin, x, res[1]))
    d = {'PRICE_FILTER': ['minPrice', 'maxPrice'], 'MIN_NOTIONAL': ['notional']}
    for name, filters in d.items():
        f_df = filter_df(filter, 'filterType', name)
        res += pluck_row(f_df, *filters)
    return res


def exchange(coin=''):
    info = client.futures_exchange_info()
    df = pd.DataFrame(info['symbols'])
    df = filter_df(df, 'contractType', 'PERPETUAL')
    df = filter_df(df, 'quoteAsset', 'USDT')
    drop_cols(df, 'pair', 'deliveryDate', 'onboardDate', 'contractType', 'status', 'quoteAsset', 'marginAsset',
              'timeInForce', 'orderTypes', 'settlePlan', 'underlyingSubType', 'underlyingType', 'liquidationFee')
    x = df.loc[df['symbol'] == symboler(coin)] if coin else df
    return x


class Coin():
    coin = ""

    def __init__(self, coin: str):
        self.coin = coin
