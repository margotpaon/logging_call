
The bot doesn't work with commands.

Hello! I'm trying to learn about discord.py and create bots on Discord, but I'm having a curious problem because my bot responds to commands in DMs, but it doesn't respond in the server channel even though I've given it permissions.

My code
``` 
# Importe a biblioteca dotenv
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse as variáveis de ambiente
discord_key = os.getenv("DISCORD_KEY")

# Prefixo dos comandos do bot
prefix = "!"

# Definição dos intents
intents = discord.Intents.default()
intents.messages = True  # Habilita o intent para mensagens
intents.guilds = True    # Habilita o intent para servidores
intents.members = True   # Habilita o intent para membros
intents.reactions = True # Habilita o intent para reações

# Inicialização do bot
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

# Evento para imprimir uma mensagem quando o bot estiver online
@bot.event
async def on_ready():
    print(f'{bot.user} está online!')

# Comando simples para dizer olá
@bot.command()
async def ola(ctx):
    await ctx.send(f'Olá, {ctx.author.mention}!')

# Comando para somar dois números
@bot.command()
async def soma(ctx, num1: int, num2: int):
    resultado = num1 + num2
    await ctx.send(f'A soma de {num1} e {num2} é {resultado}.')

# Roda o bot
bot.run(discord_key)

```
My log on docker 

```
 docker-compose up
[+] Running 1/0
 ✔ Container bot-python_app-1  Created                                                                 0.0s
Attaching to python_app-1
python_app-1  | 2024-04-10 10:39:08 WARNING  discord.ext.commands.bot Privileged message content intent is missing, commands may not work as expected.
python_app-1  | 2024-04-10 10:39:08 INFO     discord.client logging in using static token
python_app-1  | 2024-04-10 10:39:11 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: f12d4510255ae67e973c93462642f397).

```

My url to invite bot to server
> https://discord.com/oauth2/authorize?client_id=1226960931527987281&permissions=8&scope=applications.commands+bot+messages.read+guilds+applications.commands.permissions.update

[Privileged Intents](https://i.stack.imgur.com/vBQp8.png)