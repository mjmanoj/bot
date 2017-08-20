"""
the rex package is a bittrex exchange adapter.
"""
import bittrex
from operator import itemgetter
from config import env
Rex = bittrex.Bittrex(api_key="", api_secret="")


# blacklist is where coins who have too much non crypto currency meaning go. sorry :(
blacklist = ["GLD", "1ST"]


# get_cream gets the top 40% of the pack, no dregs please.
def get_cream(list_of_things):
    return int(len(list_of_things) * 0.4)


# get_market_summaries gets the top 40% highest volume market summaries for
# btc, eth and usdt based markets
# TODO: how can we automate the btc/eth/usdt lists into automated list generation based on the split[0] for the MarketName?
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

    summaries = btc_summaries[:get_cream(btc_summaries)] + eth_summaries[:get_cream(
        eth_summaries)] + usdt_summaries[:get_cream(usdt_summaries)]

    # get rid of blacklist terms
    for blacklisted in blacklist:
        if blacklisted in summaries:
            summaries.remove(blacklisted)

    # ensure no duplicates
    final = []
    for i in summaries:
        if i not in final:
            final.append(i)

    if env == "test":
        return final[:5]

    return final
