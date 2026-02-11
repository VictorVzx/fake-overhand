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

    @app_commands.command(name='criar_cargo', description='Cria um cargo com uma especifica')
    @app_commands.describe(
        nome='Nome do cargo a ser criado',
        cor_hex='Cor em hexadecimal (ex: FF0000 para vermelho)'
    )
    async def criar_cargo(self, interaction: discord.Interaction, nome: str, cor_hex: str):
        try:
            cor = discord.Color(int(cor_hex, 16))
            cargo = await interaction.guild.create_role(name=nome, color=cor)
            await interaction.response.send_message(f'Cargo "{nome}" criado com sucesso!', ephemeral=True)
        except ValueError:
            await interaction.response.send_message('Cor inválida. Certifique-se de fornecer uma cor válida em hexadecimal.', ephemeral=True)
    
    @app_commands.command(name='remover_cargo', description='Remove um cargo')
    @app_commands.describe(
        nome='Nome do cargo a ser removido'
    )
    async def remover_cargo(self, interaction: discord.Interaction, nome: str):
        cargo = discord.utils.get(interaction.guild.roles, name=nome)
        if cargo:
            await interaction.guild.delete_role(cargo)
            await interaction.response.send_message(f'Cargo "{nome}" removido com sucesso!', ephemeral=True)
        else:
            await interaction.response.send_message(f'Cargo "{nome}" não encontrado.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))