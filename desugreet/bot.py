import discord
import datetime
from dateutil.relativedelta import relativedelta

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
token = None
member_role_str = None
welcome_msg = None
log_channel_id = None
entrance_role_str = None
entrance_channel_id = None
entrance_msg = None
start_time = datetime.datetime.now()

entrance_track_buffer = {}

@client.event
async def on_member_join(member):
    server = member.guild
    entrance_role = discord.utils.get(server.roles, name=entrance_role_str)
    if entrance_role is not None:
        await member.add_roles(entrance_role)
    else:
        print("check your config file, the role does not exist!")

    entrance_track_buffer[member] = []  # create list buffer with a member obj key
    entrance_track_buffer[member].append(await client.get_channel(entrance_channel_id).send(entrance_msg.format(member)))

@client.event
async def on_member_update(member_before, member_after):
    server = member_after.guild

    ## check for entrance-role transition
    entrance_role = discord.utils.get(server.roles, name=entrance_role_str)
    member_before_entrance = entrance_role in member_before.roles
    member_after_entrance = entrance_role in member_after.roles
    # add user to member when the entrance-role is removed
    if member_before_entrance and not member_after_entrance:
        # entrance role was removed
        member_role = discord.utils.get(server.roles, name=member_role_str)
        if member_role is not None:
            await member_after.add_roles(member_role)
        else:
            print("check your config file, the role does not exist!")
        # detect when member does not accept DM
        try:
            await member_after.send(welcome_msg.format(member_after, server))
        except discord.errors.Forbidden:
            await client.get_channel(log_channel_id).send("{0.mention} (closed DM) isch cho".format(member_after))
        else:
            await client.get_channel(log_channel_id).send("{0.mention} isch cho".format(member_after))
        # delete messages in entrance_track_buffer
        if member_after in entrance_track_buffer.keys():
            for msg in entrance_track_buffer[member_after]:
                try:
                    await msg.delete()
                except discord.errors.NotFound:
                    pass

            del entrance_track_buffer[member_after]

    ## check for boost/de-boosting transition
    boost_role = discord.utils.get(server.roles, name='Nitro Booster')
    member_before_boost = boost_role in member_before.roles
    member_after_boost = boost_role in member_after.roles

    if member_after_boost and not member_before_boost:
        # booster role was added
        reaction_emoji = discord.utils.get(server.emojis, name='cirnoSmile')
        await client.get_channel(log_channel_id).send("{0.mention} het de Server boosted. Danke! {1}".format(member_after, reaction_emoji))
    if member_before_boost and not member_after_boost:
        # booster role was removed
        reaction_emoji = discord.utils.get(server.emojis, name='saddest')
        await client.get_channel(log_channel_id).send("{0.mention} het ufghört de Server zbooste. {1}".format(member_after, reaction_emoji))

@client.event
async def on_member_remove(member):
    # suppress the log when the member is of entrance-role
    server = member.guild
    entrance_role = entrance_role = discord.utils.get(server.roles, name=entrance_role_str)
    if entrance_role in member.roles:
        await client.get_channel(entrance_channel_id).send("{0.name}#{0.discriminator} isch wieder gange".format(member))
    else:
        await client.get_channel(log_channel_id).send("{0.name}#{0.discriminator} isch gange".format(member))


@client.event
async def on_message(message):
    global entrance_track_buffer

    if message.author == client.user:
        return

    entrance_channel = client.get_channel(entrance_channel_id)
    if message.channel is entrance_channel:
        if message.author in entrance_track_buffer.keys():
            entrance_track_buffer[message.author].append(message)

    if message.content.startswith('!dginfo'):
        now = datetime.datetime.now()
        diff = relativedelta(now, start_time)
        text = 'Running DesuGreet V1.2 since {0.days} days {0.hours} hours {0.minutes} minutes!'
        text += '\nsource: https://github.com/swissdesu/DesuGreet'
        text = text.format(diff)
        await message.channel.send(text)
    elif message.content.startswith('!clear-entrance'):
        if message.author.guild_permissions.manage_messages:
            # delete all messages in entrance channel
            async for message in entrance_channel.history(limit=None):
                await message.delete()
            # clear out entrance message buffer
            entrance_track_buffer = {}
        else:
            await message.reply("{0.mention} du häsch ke Berechtigung für de Command".format(message.author))


@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

def run():
    if (token is not None 
    and member_role_str is not None 
    and welcome_msg is not None
    and entrance_role_str is not None
    and entrance_channel_id is not None
    and entrance_msg is not None):
        client.run(token)
    else:
        print("Error: Some configuration are missing in the json config file")
