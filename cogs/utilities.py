import discord
from discord.ext import commands
from discord import app_commands

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Responde com Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')


    @app_commands.command(name='ban', description='Bane um usuário do servidor.')
    @app_commands.describe(user='O usuário a ser banido', reason='Motivo do banimento')
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Sem motivo fornecido"):
        if interaction.user.guild_permissions.ban_members:
            await interaction.guild.ban(user, reason=reason)
            await interaction.response.send_message(f'Usuário {user.mention} banido por: {reason}')
        else:
            await interaction.response.send_message('Você não tem permissão para banir membros.', ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))