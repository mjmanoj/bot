"""
bittrex adaptor to the bittrex exchange.
"""
import bittrex
Rex = bittrex.Bittrex(api_key="", api_secret="")


# get_market_symbols returns active btc based symbols
def get_market_symbols():
    res = Rex.get_markets()
    coins = res["result"]
    coin_names = []

    for coin in coins:
        base = coin["BaseCurrency"]
        is_active = coin["IsActive"]

        if is_active:
            if base == "BTC":
                name = coin["MarketCurrency"]
                coin_names.append(name)

    return coin_names
