from binance import Client, AsyncClient, BinanceSocketManager


def gen_client(testnet=True, asyn=False):
    napi_key = "e6geB7TFiaM4FTACiiP2Slk9QFQyYuCt37KH7ht5nwrYcJCvdkloyHAzh4ImtSQh"
    napi_secret = "dC25QStiRNVlGrHJk8ajK9fQhmUCCDfGwSjTvqCFP0Fsdyw3nKtmkZjgKrmmwGIZ2"

    api_key = "9Cc4lp3DlqB9sh7Si2a63sktrhAUiPmtRTMTh22v2OOaNweYSXcHoKzEcPtlLX5i"
    api_secret = "xbw7wRuGvNjDXFS1rM5BTkoRToJfWW8StEUvO0tct9Ibwz3dj9vXThQTzF1iIEeE"

    if testnet:
        api_key = "17decb9a46f67558c5088856ee8c3fa28c20c72de37bb8cffc9924a2a9cc0a12"
        api_secret = '7e27cf5baa00ab22734a4781d5050d20be40ab0c2289567769eb2a789d3a294e'

    if asyn:
        client = AsyncClient(api_key, api_secret, testnet=testnet)  # ,tld='us')
    else:
        client = Client(api_key, api_secret, testnet=testnet, tld='us')

    return client

testnet = True
client = gen_client(testnet)
async_client = gen_client(testnet,True)