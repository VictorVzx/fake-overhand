import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')
    try:
        # Isso envia seus comandos de barra para o Discord
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos de barra!")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

async def load_cogs():
    extensions = ['cogs.commands', 'cogs.utilities']
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f'Extensão {extension} carregada com sucesso!')
        except Exception as e: 
            print(f'Falha ao carregar a extensão {extension}: {e}.')
            
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
