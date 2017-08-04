import ConfigParser
import telegram

Config = ConfigParser.ConfigParser()
Config.read('.env')


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


token = ConfigSectionMap("main")["http_api_token"]

bot = telegram.Bot(token=token)

print(bot.get_me())
