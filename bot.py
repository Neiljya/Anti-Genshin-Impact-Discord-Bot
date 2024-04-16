# WARNING: EXTREMELY OLD AND POORLY WRITTEN

#################################################
#### INSTRUCTIONS ###############################
#################################################

## SET UP THE SERVER ##
# 1. Change the role name to whatever your 'mute' role is in your server:
role_name = 'Genshin players'

## SET UP THE SCRIPT ##
# 1. Insert your bot token below:
TOKEN = ''
# 2. If you want to REMOVE words from the filter, go into filter.txt under the config folder and remove a word.
# 3. If you want to ADD words from the filter, go into filter.txt under the config folder and add a word seperated by a NEW LINE
# 4. If you want to ADD to the nicknames, go into nicknames under config and seperate each nickname by a colon (':')
# 5. Adding responses is the same thing as adding nicknames

#################################################
#################################################
#################################################

import discord, random, time
from discord.ext import commands



with open('config/nicknames','r') as f:
    global nickname
    words = f.read()
    nicknames = words.split(':')

with open('config/filter.txt','r') as f:
    global filter
    words = f.read()
    triggerwords = words.split()

with open('config/responses.txt','r') as f:
    global response
    resp = f.read()
    response_list = resp.split(':')

intents = discord.Intents().all()
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)
bot = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as: {0.user}'.format(client))

@client.event
async def on_message(message):
    recipient = message.author
    if message.author == client.user:
        return
    msg = message.content
    if any(word in msg.lower() for word in triggerwords):
        role = discord.utils.get(message.author.guild.roles, name=role_name)
        # member = discord.utils.get(message.author.guild.roles,name=member_role)
        if not recipient.guild_permissions.kick_members:
            await recipient.edit(roles=[role])
            await recipient.edit(nick=random.choice(nicknames))
        else:
            await recipient.add_roles(role)
        await message.channel.send(random.choice(response_list) + message.author.mention)
        while recipient is not None and role in recipient.roles:
            time.sleep(.25)
            await recipient.send(random.choice(response_list) + message.author.mention)
        else:
            await recipient.send(recipient + ' left')
    if message.content.startswith('$addresponse'):
        phrase = message.content.split('$addresponse', 1)[1]
        with open('config/responses.txt', 'r') as f:
            global filter
            phrases = f.read()
            if phrase not in phrases:
                with open('config/responses.txt', "a") as f:
                    f.write(phrase + ":")
                    await message.channel.send(f'{phrase} has been successfully added!')
            else:
                await message.channel.send(f'{phrase} is already added!')

    await client.process_commands(message)


@client.event
async def on_presence_update(prev,cur):
    role = discord.utils.get(cur.guild.roles, name=role_name)
    game = "genshin impact"

    if cur.activity and cur.activity.name.lower() == game:
            await cur.edit(roles=[role]) #removes all roles except for mute role
    elif prev.activity and prev.activity.name.lower() == game and not cur.activity:
            return


@client.command(aliases=['filter','f'])
@commands.has_permissions(kick_members=True)
async def add_filter(ctx,arg):
    word = arg
    with open('config/filter.txt', 'r') as f:
        global filter
        words = f.read()
        if word.lower() not in words:
            with open('config/filter.txt', "a") as f:
                f.write(word + "\n")
                await ctx.send(word + ' successfully filtered')
        else:
            await ctx.send('That word is already filtered!')



@client.command(aliases=['rfilter'])
async def remove_filter(ctx,arg):
    word = arg
    with open('config/filter.txt', 'r') as f:
        global filter
        words = f.read()
        if word.lower() not in words:
            await ctx.send(f'{word} is not found in the list')
        else:
            with open('config/filter.txt', 'w') as f:
                delete = words.replace(word, '')
                f.write(delete)
                await ctx.send(f'{word} successfully removed!')






client.run(TOKEN)
