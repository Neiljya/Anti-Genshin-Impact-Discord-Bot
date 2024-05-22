import discord
import json
import random
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='$', intents=intents)
config_directory = 'config/config.json'
TOKEN = ''

# Load configurations from JSON file
def load_config():
    with open(config_directory, 'r') as f:
        return json.load(f)


config = load_config()


@client.event
async def on_ready():
    print(f'Logged in as: {client.user}')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    config = load_config()  # Reload configuration on every message
    msg = message.content.lower()

    if any(word in msg for word in config['filter_words']):
        role = discord.utils.get(message.guild.roles, name=config['role_name'])
        if role: and not message.author.guild_permissions.kick_members:
            await message.author.edit(roles=[role])  # Set roles to only the mute role
            await message.author.edit(nick=random.choice(config['nicknames']))
            await message.channel.send(random.choice(config['responses']) + message.author.mention)

    await client.process_commands(message)


@client.command()
@commands.has_permissions(manage_roles=True)
async def updaterole(ctx, *, new_role_name):
    config = load_config()
    config['role_name'] = new_role_name
    with open(config_directory, 'w') as f:
        json.dump(config, f)
    await ctx.send(f"Mute role updated to: {new_role_name}")


@client.command()
@commands.has_permissions(manage_messages=True)
async def addfilter(ctx, *, word):
    config = load_config()
    if word.lower() not in config['filter_words']:
        config['filter_words'].append(word.lower())
        with open(config_directory, 'w') as f:
            json.dump(config, f)
        await ctx.send(f'Word "{word}" added to filter.')
    else:
        await ctx.send('That word is already in the filter.')


@client.command()
@commands.has_permissions(manage_messages=True)
async def removefilter(ctx, *, word):
    config = load_config()
    if word.lower() in config['filter_words']:
        config['filter_words'].remove(word.lower())
        with open(config_directory, 'w') as f:
            json.dump(config, f)
        await ctx.send(f'Word "{word}" removed from filter.')
    else:
        await ctx.send('Word not found in the filter.')


@client.command()
@commands.has_permissions(manage_messages=True)
async def addresponse(ctx, *, response):
    config = load_config()
    if response not in config['responses']:
        config['responses'].append(response)
        with open(config_directory, 'w') as f:
            json.dump(config, f)
        await ctx.send(f'Response "{response}" added.')
    else:
        await ctx.send('That response is already added.')

@client.event
async def on_presence_update(prev,cur):
    role = discord.utils.get(cur.guild.roles, name=config['role_name'])
    game = "genshin impact"

    if cur.activity and cur.activity.name.lower() == game:
            await cur.edit(roles=[role]) #removes all roles except for mute role
    elif prev.activity and prev.activity.name.lower() == game and not cur.activity:
            return


client.run(TOKEN)
