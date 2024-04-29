import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


# Variável global para armazenar o tempo de início da chamada
call_start_times = {}

# Carregar variáveis de ambiente
load_dotenv()

# Acessar variáveis de ambiente
discord_key = os.getenv("DISCORD_KEY")

# Definir intents
intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True
intents.reactions = True

# Prefixo dos comandos do bot
prefix = "!"

# Inicializar bot
bot = commands.Bot(command_prefix=prefix, intents=intents)

