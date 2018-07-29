import discord
import asyncio
from discord.ext import commands

TOKEN = 'NDM4MDY3OTQ1MTI2NDk0MjI5.Dj6yCQ.9IsfraSFu_hmpWtUuFeJJ4JA0gU'

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Test'))

client.run(TOKEN)