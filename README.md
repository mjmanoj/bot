# moonbot

checks social media outlets for the most optimal coins to trade

## project roadmap

Please view the [ROADMAP.md](ROADMAP.md) to see what has been accomplished and what is upcoming!

## development

### testing

I prefer to do an e2e style test at the moment, so all scripts in the `Makefile` for testing are listed below to test the main functionalities of the code.

I plan on adding unit testing into the mix, but just haven't gotten around to it at the moment :shrug:

#### test_moon_call

This will run the entire moon call with limited output, and post the results to the moonbot dev channel at https://t.me/joinchat/AAAAAEPIqtTv8hJkWBxeFA

### contributing to moonbot

If you'd like to be part of the project and even earn BTC from the tip service based on your commit activity, please write awitherow for information and we can discuss things.

### run your own

If you'd like to run your own standalone moon bot, you'll need

1) twitter application
2) your own telegram bot
3) working `.env` variables listed below

```bash
bot_api_token=XXX
telegram_chat_prod=XXX
telegram_chat_dev=XXX
bittrex_api_key=XXX
bittrex_api_secret=XXX
twitter_consumer_key=XXX
twitter_consumer_secret=XXX
twitter_access_token=XXX
twitter_access_secret=XXX
tip_jar=XXX
```