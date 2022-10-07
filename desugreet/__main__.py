import os
import discord
from desugreet.bot import DesuGreetBot
from desugreet.config import JsonConfig


def main():
    home = os.path.expanduser('')
    configPath = os.path.join(home, ".desugreet")

    if os.path.isfile(configPath):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        jsonConfig = JsonConfig(configPath)
        bot = DesuGreetBot(jsonConfig, intents)
        bot.run()
    else:
        print("Please create the config file .desugreet in the directory you are running the bot from!")


if __name__ == "__main__":
    main()
