import discord
from discord.ext import commands
from discord import app_commands # Importação correta para Slash Commands

# 1. Sua classe DEVE herdar de commands.Cog
class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 2. O decorador de Slash Command dentro de Cog
    @app_commands.command(name='ping', description='Responde com pong!')
    async def ping(self, interaction: discord.Interaction):
        # Note o 'self' acima. Em Cogs, o primeiro parâmetro é sempre self.
        await interaction.response.send_message('Pong!')
        
    @app_commands.command(name='menu', description="Mostra um menu com todos os comandos do bot")
    async def menu(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 Menu de Comandos",
            description="Aqui estão os comandos disponíveis no bot:",
            color=discord.Color.blue()
        )

        # Comandos Gerais (desta Cog)
        embed.add_field(
            name="🏠 Geral",
            value="`/ping` - Responde com Pong!\n`/menu` - Mostra esta lista",
            inline=False
        )

        # Comandos de Utilidade (da Cog UtilityCommands)
        embed.add_field(
            name="🛠️ Utilidades & Moderação",
            value=(
                "`/ban` - Bane um usuário\n"
                "`/unban` - Desbane um usuário via ID\n"
                "`/criar_cargo` - Cria um cargo personalizado\n"
                "`/remover_cargo` - Exclui um cargo existente\n"
                "`/limpar` - Limpa uma quantidade específica de mensagens"
            ),
            inline=False
        )

        embed.set_footer(text=f"Solicitado por {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))