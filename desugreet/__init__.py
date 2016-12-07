import os
import desugreet.bot as bot
import json

home = os.path.expanduser('~')
config = os.path.join(home, ".desugreet")

if os.path.isfile(config):
    with open(config) as data_file:
        data = json.load(data_file)

    bot.token = data["token"]
    bot.role = data["role"]
    bot.run()
else:
    print("Please create the config file .desugreet in your home directory!")
