import sqlite3
import discord
from discord.ext import commands
from utils import format_duration
from database import c, conn
from config import bot, prefix


# Remove o comando de ajuda padrão
bot.remove_command('help')

# Função para enviar uma mensagem embed
async def send_embed(ctx, title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)

# Comando para exibir a lista de comandos disponíveis
@bot.command(brief="Exibe lista de comandos")
async def listcommands(ctx):
    await send_embed(ctx, "Comandos disponíveis", f"Aqui está a lista de comandos disponíveis: `{get_command_list(ctx)}`", discord.Color.blue())

# Função para obter a lista de comandos disponíveis
def get_command_list(ctx):
    return ', '.join([f'{prefix}{cmd.name}' for cmd in bot.commands])

# Comando para exibir os cargos salvos no banco de dados
@bot.command(brief="Mostra os cargos salvos no banco de dados")
async def listrolesdb(ctx):
    try:
        roles_data = get_roles_data()
        if roles_data:
            roles_info = "\n".join([f"ID: {role[0]}, Nome: {role[1]}" for role in roles_data])
            await send_embed(ctx, "Registros da tabela 'roles'", roles_info, discord.Color.blue())
        else:
            await send_embed(ctx, "Nenhum registro encontrado na tabela 'roles'", "", discord.Color.yellow())
    except sqlite3.Error as e:
        await send_embed(ctx, "Erro ao acessar o banco de dados", str(e), discord.Color.red())

# Função para obter os dados dos cargos salvos no banco de dados
def get_roles_data():
    c.execute("SELECT * FROM roles")
    return c.fetchall()

# Comando para exibir os cargos no servidor
@bot.command(brief="Mostra os cargos no servidor")
async def listroles(ctx):
    try:
        roles_list = get_roles_list(ctx)
        await send_embed(ctx, "Lista de cargos", roles_list, discord.Color.blue())
    except commands.CommandError as e:
        await send_embed(ctx, "Erro ao executar o comando", str(e), discord.Color.red())

# Função para obter a lista de cargos no servidor
def get_roles_list(ctx):
    if not ctx.guild.me.guild_permissions.manage_roles:
        raise commands.CommandError("O bot não tem permissão para listar os cargos.")
    if ctx.guild is None:
        raise commands.CommandError("O bot não está conectado ao servidor do Discord.")
    return "\n".join([role.name for role in ctx.guild.roles])

# Comando para salvar um cargo no banco de dados
@bot.command(brief="Salva o cargo no banco de dados")
async def saverole(ctx, role_name: str):
    try:
        if not role_name:
            await send_embed(ctx, "Nome do cargo não fornecido", "Por favor, forneça o nome do cargo.", discord.Color.red())
            return
        save_role_to_db(ctx, role_name)
        await send_embed(ctx, "Cargo salvo", f"O cargo '{role_name}' foi salvo no banco de dados.", discord.Color.blue())
    except commands.CommandError as e:
        await send_embed(ctx, "Erro ao executar o comando", str(e), discord.Color.red())

# Função para salvar um cargo no banco de dados
def save_role_to_db(ctx, role_name):
    if not ctx.guild.me.guild_permissions.manage_roles:
        raise commands.CommandError("O bot não tem permissão para gerenciar cargos.")
    if ctx.guild is None:
        raise commands.CommandError("O bot não está conectado ao servidor do Discord.")
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        c.execute("INSERT INTO roles (role_id, role_name) VALUES (?, ?)", (role.id, role.name))
        conn.commit()
    else:
        raise commands.CommandError("O cargo especificado não foi encontrado.")

# Comando para listar os registros da tabela calls
@bot.command(brief="Exibe as chamadas salvas")
async def listcallsdb(ctx):
    try:
        calls_data = get_calls_data()
        if calls_data:
            calls_info = "\n".join([f"ID do membro: {call[0]}, ID do cargo: {call[1]}, Data de início: {call[2]}, Duração: {format_duration(call[3])}" for call in calls_data])
            await send_embed(ctx, "Registros das chamadas'", calls_info, discord.Color.blue())
        else:
            await send_embed(ctx, "Nenhum registro encontrado na tabela 'calls'", "", discord.Color.yellow())
    except sqlite3.Error as e:
        await send_embed(ctx, "Erro ao acessar o banco de dados", str(e), discord.Color.red())

# Função para obter os dados das chamadas salvas no banco de dados
def get_calls_data():
    c.execute("SELECT * FROM calls")
    return c.fetchall()

# Comando para resetar o banco de dados
@bot.command(brief="Apaga os registros no banco de dados")
@commands.has_permissions(administrator=True)
async def resetdb(ctx):
    try:
        reset_database()
        await send_embed(ctx, "Registros do banco de dados resetados com sucesso", "", discord.Color.blue())
    except sqlite3.Error as e:
        await send_embed(ctx, "Erro ao acessar o banco de dados", str(e), discord.Color.red())

# Função para resetar o banco de dados
def reset_database():
    c.execute("DELETE FROM roles")
    c.execute("DELETE FROM calls")
    conn.commit()
