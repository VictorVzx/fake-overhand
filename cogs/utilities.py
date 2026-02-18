import asyncio
import discord
from discord.ext import commands
from discord import app_commands

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ban', description='Bane um usuário do servidor.')
    @app_commands.describe(user='O usuário a ser banido', reason='Motivo do banimento')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Sem motivo fornecido"):
        if interaction.guild.me.top_role <= user.top_role:
            return await interaction.response.send_message("Eu não tenho permissão hierárquica para banir este membro.", ephemeral=True)

        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(f'Usuário {user.mention} banido por: {reason}')

    @app_commands.command(name='unban', description='Desbane um usuário do servidor.')
    @app_commands.describe(user_id='ID do usuário a ser desbanido')
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            await interaction.response.send_message(f'Usuário {user.name} desbanido com sucesso.')
        except discord.NotFound:
            await interaction.response.send_message("Usuário não encontrado ou não está banido.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Por favor, forneça um ID numérico válido.", ephemeral=True)

    @app_commands.command(name='criar_cargo', description='Cria um cargo com uma cor específica')
    @app_commands.describe(nome='Nome do cargo', cor_hex='Cor em hexadecimal (ex: FF0000)')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def criar_cargo(self, interaction: discord.Interaction, nome: str, cor_hex: str):
        try:
            cor_limpa = cor_hex.lstrip('#')
            cor = discord.Color(int(cor_limpa, 16))
            await interaction.guild.create_role(name=nome, color=cor)
            await interaction.response.send_message(f'Cargo **{nome}** criado com sucesso!', ephemeral=True)
        except ValueError:
            await interaction.response.send_message('Formato de cor inválido! Use apenas letras e números (ex: 00FF00).', ephemeral=True)

    @app_commands.command(name='remover_cargo', description='Remove um cargo pelo nome')
    @app_commands.describe(cargo='Selecione o cargo para remover')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remover_cargo(self, interaction: discord.Interaction, cargo: discord.Role):
        try:
            await cargo.delete()
            await interaction.response.send_message(f'Cargo "{cargo.name}" removido com sucesso!', ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Eu não tenho permissão para excluir este cargo (ele pode ser superior ao meu).", ephemeral=True)

    @app_commands.command(name='limpar', description='Limpa uma quantidade específica de mensagens do canal.')
    @app_commands.describe(quantidade='Número de mensagens a serem deletadas')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def limpar(self, interaction: discord.Interaction, quantidade: int):
        if quantidade < 1:
            return await interaction.response.send_message("A quantidade deve ser pelo menos 1.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=quantidade)
        await interaction.followup.send(f'✅ Foram removidas {len(deleted)} mensagens.')

    @app_commands.command(name='give_role', description='Dá um cargo para um membro.')
    @app_commands.describe(cargo='Nome do cargo', membro='Membro que receberá o cargo')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def give_role(self, interaction: discord.Interaction, cargo: str, membro: discord.Member):
        # FIX: removido time.sleep() bloqueante; usando defer + followup corretamente
        try:
            role = discord.utils.get(interaction.guild.roles, name=cargo)
            if not role:
                return await interaction.response.send_message("Cargo não encontrado.", ephemeral=True)

            await interaction.response.defer(ephemeral=True)
            await membro.add_roles(role)
            await interaction.followup.send(f'Cargo **{role.name}** dado para {membro.mention} com sucesso!', ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("Eu não tenho permissão para dar este cargo.", ephemeral=True)

    @app_commands.command(name='unrole', description='Remove o cargo de um membro')
    @app_commands.describe(cargo='Nome do cargo', membro='Membro que irá ter o cargo removido')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unrole(self, interaction: discord.Interaction, cargo: str, membro: discord.Member):
        # FIX: removido time.sleep() bloqueante; usando defer + followup corretamente
        try:
            role = discord.utils.get(interaction.guild.roles, name=cargo)
            if not role:
                return await interaction.response.send_message("Cargo não encontrado.", ephemeral=True)

            await interaction.response.defer(ephemeral=True)
            await membro.remove_roles(role)
            await interaction.followup.send(f'Cargo **{role.name}** removido de {membro.mention} com sucesso!', ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("Eu não tenho permissão para tirar este cargo.", ephemeral=True)

    @app_commands.command(name='kickcargo', description='Remove (kick) todos os membros com um cargo específico')
    @app_commands.describe(cargo='Cargo cujos membros serão removidos do servidor')
    @app_commands.checks.has_permissions(administrator=True)
    async def kickcargo(self, interaction: discord.Interaction, cargo: discord.Role):
        await interaction.response.defer()

        try:
            await asyncio.wait_for(interaction.guild.chunk(), timeout=10)
        except asyncio.TimeoutError:
            pass

        membros = [m for m in interaction.guild.members if cargo in m.roles and not m.bot]

        if not membros:
            await interaction.followup.send(f"Nenhum membro encontrado com o cargo **{cargo.name}**.")
            return

        await interaction.followup.send(f"⏳ Removendo **{len(membros)}** membros com o cargo **{cargo.name}**...")

        removidos, erros = 0, 0
        for membro in membros:
            try:
                await membro.kick(reason=f"Remoção em massa pelo comando kickcargo — por {interaction.user}")
                removidos += 1
            except (discord.Forbidden, discord.HTTPException):
                erros += 1

        await interaction.channel.send(f"✅ **{removidos}** removidos | ❌ Erros: **{erros}**")

    @app_commands.command(name='remover_cargo_em_massa', description='Remove um cargo dos primeiros 50 membros que o possuem')
    @app_commands.describe(cargo='Cargo a ser removido dos membros')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remover_cargo_em_massa(self, interaction: discord.Interaction, cargo: discord.Role):
        await interaction.response.defer()

        try:
            await asyncio.wait_for(interaction.guild.chunk(), timeout=10)
        except asyncio.TimeoutError:
            pass

        membros = [m for m in interaction.guild.members if cargo in m.roles and not m.bot][:20]

        if not membros:
            await interaction.followup.send(f"Nenhum membro encontrado com o cargo **{cargo.name}**.")
            return

        await interaction.followup.send(f"⏳ Removendo o cargo **{cargo.name}** de **{len(membros)}** membros...")

        removidos, erros = 0, 0
        for membro in membros:
            try:
                await membro.remove_roles(cargo, reason=f"Remoção em massa — por {interaction.user}")
                removidos += 1
            except (discord.Forbidden, discord.HTTPException):
                erros += 1

        await interaction.channel.send(f"✅ Cargo removido de **{removidos}** membros | ❌ Erros: **{erros}**")


async def setup(bot):
    await bot.add_cog(UtilityCommands(bot))