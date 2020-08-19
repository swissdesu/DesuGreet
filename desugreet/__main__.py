import os
import desugreet.bot as bot
import json

def main():
    home = os.path.expanduser('')
    config = os.path.join(home, ".desugreet")

    if os.path.isfile(config):
        with open(config) as data_file:
            data = json.load(data_file)

        bot.token = data["token"]
        bot.role = data["role"]
        bot.welcome_msg = data["message"]
        bot.log_channel_id = data["log"]
        bot.run()
    else:
        print("Please create the config file .desugreet in your home directory!")


if __name__ == "__main__":
    main()
