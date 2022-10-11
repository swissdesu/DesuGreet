import discord

class EntranceService:
    def __init__(self) -> None:
        self.entrance_track_buffer = {}


    async def create_new_entrance_person(self, member, entranceRole, entranceChannel, entranceMsg):
        # give entrance role to the new member
        if entranceRole is not None:
            await member.add_roles(entranceRole)
        else:
            print("check your config file, the role does not exist!")
        
        # create new entry in track buffer
        self.entrance_track_buffer[member] = []  # create list buffer with a member obj key
        # store bot message into the new buffer
        self.entrance_track_buffer[member].append(await entranceChannel.send(entranceMsg))

        
    async def add_member(self, member, memberRole, welcomeMsg, logChannel):
        if memberRole is not None:
            await member.add_roles(memberRole)
        else:
            print("check your config file, the role does not exist!")
        # detect when member does not accept DM
        try:
            await member.send(welcomeMsg)
        except discord.errors.Forbidden:
            await logChannel.send("{0.mention} (closed DM) isch cho".format(member))
        else:
            await logChannel.send("{0.mention} isch cho".format(member))


    def add_message(self, message):
        if message.author in self.entrance_track_buffer.keys():
            self.entrance_track_buffer[message.author].append(message)


    async def delete_member_history(self, member):
        # delete messages in entrance_track_buffer
        if member in self.entrance_track_buffer.keys():
            for msg in self.entrance_track_buffer[member]:
                try:
                    await msg.delete()
                except discord.errors.NotFound:
                    pass

            del self.entrance_track_buffer[member]


    async def delete_all_history(self, message, entranceChannel):
        if message.author.guild_permissions.manage_messages:
            # delete all messages in entrance channel
            async for msg in entranceChannel.history(limit=None):
                await msg.delete()
            # clear out entrance message buffer
            self.entrance_track_buffer = {}
        else:
            await message.reply("{0.mention} du häsch ke Berechtigung für de Command".format(message.author))