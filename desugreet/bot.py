import discord
import datetime
from dateutil.relativedelta import relativedelta

client = discord.Client()
token = None
role = None
welcome_msg = None
log_channel_id = None
start_time = datetime.datetime.now()


@client.event
async def on_member_join(member):
    server = member.server
    member_role = __getRole(server.roles, role)
    if member_role is not None:
        await client.add_roles(member, member_role)
    else:
        print("check your config file, the role does not exist!")
    await client.send_message(member, welcome_msg.format(member, server))
    await client.send_message(client.get_channel(log_channel_id), "{0.name} has joined".format(member))

@client.event
async def on_member_remove(member):
    await client.send_message(client.get_channel(log_channel_id), "{0.name} has left".format(member))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!dginfo'):
        now = datetime.datetime.now()
        diff = relativedelta(now, start_time)
        msg = 'Running DesuGreet V1.1 since {0.days} days {0.hours} hours {0.minutes} minutes! \nsource: https://github.com/AlexFence/DesuGreet'.format(diff)
        await client.send_message(message.channel, msg)

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
