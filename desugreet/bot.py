import discord
import datetime
from dateutil.relativedelta import relativedelta

client = discord.Client()
token = None
role = None
start_time = datetime.datetime.now()


@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    member_role = __getRole(server.roles, role)
    if member_role is not None:
        await client.add_roles(member, member_role)
    else:
        print("check your config file, the role does not exist!")
    await client.send_message(member, fmt.format(member, server))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('dg!info'):
        now = datetime.datetime.now()
        diff = relativedelta(start_time, now)
        msg = 'Running DesuGreet V0.1 since {0.days} days {0.hours} hours {0.minutes} minutes!'.format(diff)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

def __getRole(roles, role_name):
    for role in roles:
        if role.name == role_name:
            return role

    return None

def run():
    if token is not None and role is not None:
        client.run(token)
