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
        bot.member_role_str = data["member-role"]
        bot.welcome_msg = data["welcome-message"]
        bot.log_channel_id = int(data["log-channel-id"])
        bot.entrance_role_str = data["entrance-role"]
        bot.entrance_channel_id = int(data["entrance-channel-id"])
        bot.entrance_msg = data["entrance-message"]
        bot.run()
    else:
        print("Please create the config file .desugreet in the directory you are running the bot from!")


if __name__ == "__main__":
    main()
