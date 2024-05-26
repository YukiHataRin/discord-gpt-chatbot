import discord
from discord.ext import commands
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True,
    intents=intents
)

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f'Logged in as {bot.user}')
    print(f"載入 {len(slash)} 個斜線指令")

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load_cogs()
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))

asyncio.run(main())
