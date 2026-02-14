import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

# 1. Configurações Iniciais
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 

# 2. Criamos uma classe para o Bot para gerenciar o setup adequadamente
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None # Opcional: remove o comando help padrão
        )

    # O setup_hook é o melhor lugar para carregar Cogs e sincronizar comandos
    async def setup_hook(self):
        extensions = ['cogs.commands', 'cogs.utilities']
        
        meu_servidor = discord.Object(id=1467963749498355876) 
    
    # Copia os comandos globais para este servidor específico
        self.tree.copy_global_to(guild=meu_servidor)
        await self.tree.sync(guild=meu_servidor)

        for extension in extensions:
            try:
                await self.load_extension(extension)
                print(f'✅ Extensão {extension} carregada.')
            except Exception as e:
                print(f'❌ Falha ao carregar {extension}: {e}')

        # Sincronização dos Slash Commands
        print("Sincronizando comandos com o Discord...")
        try:
            # Sincronização Global (pode levar alguns minutos para aparecer)
            synced = await self.tree.sync()
            print(f"🚀 Sincronizados {len(synced)} comandos de barra globalmente!")
        except Exception as e:
            print(f"❌ Erro ao sincronizar: {e}")

# 3. Instanciamos o Bot
bot = MyBot()

@bot.event
async def on_ready():
    print(f'---')
    print(f'Logado como: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(f'---')
    
@bot.event
async def on_member_join(member):
    role_name="Membro"
    
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        try:
            await member.add_roles(role)
            print(f"Cargo {role_name} aplicado a {member.name}")
        except discord.Forbidden:
            print("Erro: O bot não tem permissão para dar esse cargo (verifique a hierarquia).")
    else:
        print(f"Cargo {role_name} não encontrado no servidor.")

@bot.event
async def on_member_join(member, ctx):
    await ctx.send(f"Bem-vindo, {member.mention}!")

# 4. Execução principal
async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot desligado.")