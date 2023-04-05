
from binance import Client, AsyncClient, BinanceSocketManager

def gen_client(testnet=True): #TODO: move to utils
    if testnet:
        api_key = "61f1b8ba72db33f5685e2d280b49fd4dcdd43d0419112e325e27ed6c2805b76b"
        api_secret = '3a04aa40af1039286e92d1e1e59ec323fed94fbc934da1ce46d0348c3a6f68ac'

    client = Client(api_key, api_secret, testnet=testnet, tld='us')

    async_client = AsyncClient(api_key, api_secret, testnet=testnet)  # ,tld='us')


    return client, async_client

testnet = True
client,async_client = gen_client(testnet)
