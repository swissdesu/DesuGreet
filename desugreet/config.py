from dataclasses import dataclass
import json
import discord

class JsonConfig:
    def __init__(self, filePath) -> None:
        with open(filePath) as fileData:
            data = json.load(fileData)

        self.token = data["token"]
        self.member_role_str = data["member-role"]
        self.welcome_msg = data["welcome-message"]
        self.log_channel_id = int(data["log-channel-id"])
        self.entrance_role_str = data["entrance-role"]
        self.entrance_channel_id = int(data["entrance-channel-id"])
        self.entrance_msg = data["entrance-message"]

class ObjConfig:
    def __init__(self, client, guild, jsonConfig) -> None:
        self.logChannel = client.get_channel(jsonConfig.log_channel_id)
        self.entranceChannel = client.get_channel(jsonConfig.entrance_channel_id)
        self.memberRole = discord.utils.get(guild.roles, name=jsonConfig.member_role_str)
        self.entranceRole = discord.utils.get(guild.roles, name=jsonConfig.entrance_role_str)
        self.boostRole = discord.utils.get(guild.roles, name='Nitro Booster')