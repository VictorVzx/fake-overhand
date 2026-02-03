import discord
from discord.ext import commands
from discord import app_commands # Importação correta para Slash Commands

# 1. Sua classe DEVE herdar de commands.Cog
class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 2. O decorador de Slash Command dentro de Cog
    @app_commands.command(name='teste', description='Um comando de teste simples')
    async def teste(self, interaction: discord.Interaction):
        # Note o 'self' acima. Em Cogs, o primeiro parâmetro é sempre self.
        await interaction.response.send_message('Comando de teste executado com sucesso!')
    
async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))