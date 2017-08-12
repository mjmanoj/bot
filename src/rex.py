"""
bittrex adaptor to the bittrex exchange.
"""
import bittrex
import time
from operator import itemgetter
Rex = bittrex.Bittrex(api_key="", api_secret="")


blacklist = ["GLD", "1ST"]


def cream_only(list):
    return int(len(list) * 0.4)


def get_market_summaries():
    res = Rex.get_market_summaries()

    btc_summaries = []
    eth_summaries = []
    usdt_summaries = []

    for summary in reversed(sorted(res["result"], key=itemgetter("Volume"))):
        market = summary["MarketName"].split("-")[0]
        coin = summary["MarketName"].split("-")[1]
        volume = summary["Volume"]

        # low volume trimming
        if market == "BTC":
            btc_summaries.append(coin)

        if market == "ETH":
            eth_summaries.append(coin)

        if market == "USDT":
            usdt_summaries.append(coin)

    summaries = btc_summaries[:cream_only(btc_summaries)] + eth_summaries[:cream_only(
        eth_summaries)] + usdt_summaries[:cream_only(usdt_summaries)]

    # get rid of blacklist terms (I have found these overlap and pollute data, sorry!)
    for blacklisted in blacklist:
        if blacklisted in summaries:
            summaries.remove(blacklisted)

    # ensure no duplicates
    final = []
    for i in summaries:
        if i not in final:
            final.append(i)

    return final


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
