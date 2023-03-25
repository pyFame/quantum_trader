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


class Coin():
    coin = ""
    def __init__(self, coin: str):
        self.coin = coin
