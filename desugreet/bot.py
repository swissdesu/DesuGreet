import discord
import datetime
from dateutil.relativedelta import relativedelta

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
token = None
role = None
welcome_msg = None
log_channel_id = None
start_time = datetime.datetime.now()


@client.event
async def on_member_join(member):
    server = member.guild
    member_role = __getRole(server.roles, role)
    if member_role is not None:
        await member.add_roles(member_role)
    else:
        print("check your config file, the role does not exist!")
    
    # detect when member does not accept DM
    try:
        await member.send(welcome_msg.format(member, server))
    except discord.errors.Forbidden:
        await client.get_channel(log_channel_id).send("{0.mention} (closed DM) has joined".format(member))
    else:
        await client.get_channel(log_channel_id).send("{0.mention} has joined".format(member))

@client.event
async def on_member_update(member_before, member_after):
    server = member_after.guild

    # check for boost/de-boosting
    boost_role = discord.utils.get(server.roles, name='Nitro Booster Test')
    member_before_boost = boost_role in member_before.roles
    member_after_boost = boost_role in member_after.roles

    if member_after_boost and not member_before_boost:
        reaction_emoji = discord.utils.get(server.emojis, name='cirnoSmile')
        await client.get_channel(log_channel_id).send("{0.mention} het de Server boosted. Danke! {1}".format(member_after, reaction_emoji))
    if member_before_boost and not member_after_boost:
        reaction_emoji = discord.utils.get(server.emojis, name='saddest')
        await client.get_channel(log_channel_id).send("{0.mention} het ufghört de Server zbooste. {1}".format(member_after, reaction_emoji))

@client.event
async def on_member_remove(member):
    await client.get_channel(log_channel_id).send("{0.name}#{0.discriminator} has left".format(member))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!dginfo'):
        now = datetime.datetime.now()
        diff = relativedelta(now, start_time)
        text = 'Running DesuGreet V1.2 since {0.days} days {0.hours} hours {0.minutes} minutes!'
        text += '\nsource: https://github.com/swissdesu/DesuGreet'
        text = text.format(diff)
        await message.channel.send(text)


@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')


def __getRole(roles, role_name):
    for r in roles:
        if r.name == role_name:
            return r

    return None


def run():
    if token is not None and role is not None and welcome_msg is not None:
        client.run(token)
