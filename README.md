# moonbot

checks social media outlets for the most optimal coins to trade

## main todo

- [x] get bittrex all coins
- [x] check social for the symbol
- score the coin based on text sentiment analysis
- telegram it
- scale symbols and social integrations

## social integrations

- [x] dev.twitter.com/overview/api/
- https://steemit.github.io/steemit-docs/#discussions
- https://reddit.com/dev/api
- https://developers.google.com/youtube/v3/docs/search

## symbol integrations
- [x] https://github.com/ericsomdahl/python-bittrex
- https://pypi.python.org/pypi/Yahoo-ticker-downloader

## requirements

install requirements with the following:

```bash
make setup
```

- [telegram](https://github.com/python-telegram-bot/python-telegram-bot/)
- [dotenv](https://github.com/theskumar/python-dotenv)
- [bittrex](https://github.com/ericsomdahl/python-bittrex)