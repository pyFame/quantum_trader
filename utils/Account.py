import pandas as pd

from conf import client


class Account():

    @staticmethod
    def Futures_wallet(no_zero_bal=True):
        df = pd.DataFrame(client.futures_account_balance())
        df['balance'] = pd.to_numeric(df['balance'])
        # df = df.reset_index(drop=True)
        # df.reset_index(drop=True)
        df = df.set_index('asset')

        if no_zero_bal:
            df = df.loc[df['balance'] > 0]
        df.drop(['accountAlias'], axis=1, inplace=True)
        return df
