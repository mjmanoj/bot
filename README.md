# moonbot

checks social media outlets for the most optimal coins to trade

## main todo

- [x] get bittrex all coins
- [x] check social for the symbol
- [x] score the coin based on text sentiment analysis
- [x] telegram it
- ensure it is even working :joy:
- scale symbols and social integrations

## social integrations

- [x] dev.twitter.com/overview/api/
- https://github.com/steemit/steem-python
- https://reddit.com/dev/api
- https://developers.google.com/youtube/v3/docs/search

## symbol integrations
- [x] https://github.com/ericsomdahl/python-bittrex
- https://pypi.python.org/pypi/Yahoo-ticker-downloader

## other integrations
- look into tracking top hashtags on twitter?
- http://aa.usno.navy.mil/data/docs/api.php -> python sdk

## getting started

install requirements with the following:

```bash
make setup
```

want to use your own .env? mimic the following:

```bash
bot_api_token=

rex_api_key=
rex_api_secret=

twitter_consumer_key=
twitter_consumer_secret=
twitter_access_token=
twitter_access_secret=
```