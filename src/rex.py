"""
bittrex adaptor to the bittrex exchange.
"""
import bittrex
import time
from operator import itemgetter
Rex = bittrex.Bittrex(api_key="", api_secret="")


def get_market_summaries():
    res = Rex.get_market_summaries()
    summaries = []

    for summary in reversed(sorted(res["result"], key=itemgetter("Volume"))):
        coin = summary["MarketName"].split("-")[0]
        if coin == "BTC" or coin == "USDT" or coin == "ETH":
            summaries.append(summary["MarketName"].split("-")[1])

    return summaries[:100]


# get_market_symbols returns active btc based symbols
def get_market_symbols():
    res = Rex.get_markets()
    coins = res["result"]
    coin_names = []

    print(coins)
    time.sleep(20)

    for coin in coins:
        base = coin["BaseCurrency"]
        is_active = coin["IsActive"]

        if is_active:
            if base == "BTC":
                name = coin["MarketCurrency"]
                coin_names.append(name)

    return coin_names
