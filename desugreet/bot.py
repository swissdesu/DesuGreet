from desugreet.entrance_handler import EntranceHandler
from desugreet.member_comparator import SameMemberComparator
from desugreet.config import ObjConfig
import discord
import datetime
from dateutil.relativedelta import relativedelta


class DesuGreetBot(discord.Client):
    def __init__(self, 
                 jsonConfig,
                 intents) -> None:
        self.jsonConfig = jsonConfig
        self.startTime = datetime.datetime.now()
        self.entranceHandler = EntranceHandler()
        # run __setup method to initialize config with objects
        self.objConfig = None
        super().__init__(intents=intents)
        

    def __setup(self):
        guild = self.guilds[0]
        self.objConfig = ObjConfig(self, guild, self.jsonConfig)


    async def on_member_join(self, member):
        entranceMsg = self.jsonConfig.entrance_msg.format(member)
        await self.entranceHandler.create_new_entrance_person(member, 
                                                        self.objConfig.entranceRole, 
                                                        self.objConfig.entranceChannel, 
                                                        entranceMsg)


    async def on_member_update(self, member_before, member_after):
        guild = member_after.guild
        memberComparator = SameMemberComparator(member_before, member_after)

        ## check for entrance-role transition
        if memberComparator.roleWasRemoved(self.objConfig.entranceRole):
            # entrance role was removed
            welcomeMsg = self.jsonConfig.welcome_msg.format(member_after, member_after.guild)
            await self.entranceHandler.add_member(member_after, self.objConfig.memberRole, welcomeMsg, self.objConfig.logChannel)
            await self.entranceHandler.delete_member_history(member_after)

        ## check for boost/de-boosting transition
        if memberComparator.roleWasAdded(self.objConfig.boostRole):
            reaction_emoji = discord.utils.get(guild.emojis, name='cirnoSmile')
            await self.objConfig.logChannel.send("{0.mention} het de guild boosted. Danke! {1}".format(member_after, reaction_emoji))
        if memberComparator.roleWasRemoved(self.objConfig.boostRole):
            reaction_emoji = discord.utils.get(guild.emojis, name='saddest')
            await self.objConfig.logChannel.send("{0.mention} het ufghört de guild zbooste. {1}".format(member_after, reaction_emoji))


    async def on_member_remove(self, member):
        # suppress the log when the member is of entrance-role
        if self.objConfig.entranceRole in member.roles:
            await self.objConfig.entranceChannel.send("{0.name}#{0.discriminator} isch wieder gange".format(member))
        else:
            await self.objConfig.logChannel.send("{0.name}#{0.discriminator} isch gange".format(member))


    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel is self.objConfig.entranceChannel:
            self.entranceHandler.add_message(message)

        if message.content.startswith('!dginfo'):
            now = datetime.datetime.now()
            diff = relativedelta(now, self.startTime)
            text = 'Running DesuGreet V1.2 since {0.days} days {0.hours} hours {0.minutes} minutes!'
            text += '\nsource: https://github.com/swissdesu/DesuGreet'
            text = text.format(diff)
            await message.channel.send(text)
        elif message.content.startswith('!clear-entrance'):
            await self.entranceHandler.delete_all_history(message, self.objConfig.entranceChannel)


    async def on_ready(self):
        print('Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.__setup()

    def run(self):
        if (self.jsonConfig.token is not None 
        and self.jsonConfig.member_role_str is not None 
        and self.jsonConfig.welcome_msg is not None
        and self.jsonConfig.entrance_role_str is not None
        and self.jsonConfig.entrance_channel_id is not None
        and self.jsonConfig.entrance_msg is not None):
            super().run(self.jsonConfig.token)
        else:
            print("Error: Some configuration are missing in the json config file")