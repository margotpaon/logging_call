import sqlite3
import discord
from discord.ext import commands
from database import c, conn
from config import bot, call_start_times
from datetime import timezone, datetime
from utils import format_duration


# Evento para imprimir uma mensagem quando o bot estiver online
@bot.event
async def on_ready():
    print(f'{bot.user} está online!')


# Função para salvar a entrada do membro em um canal de voz
async def save_voice_channel_join(member):
    try:
        role_data = c.execute("SELECT * FROM roles WHERE role_id=?", (member.top_role.id,)).fetchone()
        if role_data:
            start_time = datetime.now(timezone.utc)
            call_start_times[member.id] = start_time
            c.execute("INSERT INTO calls (member_id, role_id, start_time) VALUES (?, ?, ?)",
                      (member.id, role_data[0], start_time))
            conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao executar a operação SQL: {e}")


# Função para salvar a saída do membro de um canal de voz
async def save_voice_channel_leave(member):
    try:
        if member.id in call_start_times:
            start_time = call_start_times.pop(member.id)
            duration = datetime.now(timezone.utc) - start_time
            duration_str = format_duration(duration)
            role_data = c.execute("SELECT role_id FROM calls WHERE member_id=? AND start_time=?", (member.id, start_time)).fetchone()
            role_name = role_data[0] if role_data else "Desconhecido"
            c.execute("UPDATE calls SET duration=? WHERE member_id=? AND start_time=?",
                       (duration_str, member.id, start_time))
            conn.commit()
            await member.guild.text_channels[0].send(f"O membro {member.mention} passou {duration_str} no canal de voz {role_name}.")

    except sqlite3.Error as e:
        print(f"Erro ao executar a operação SQL: {e}")


# Evento para detectar a entrada em um canal de voz
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        await save_voice_channel_join(member)
    elif before.channel is not None and after.channel is None:
        await save_voice_channel_leave(member)


# Evento para detectar a saída de um canal de voz
@bot.event
async def on_voice_channel_leave(member, channel):
    await save_voice_channel_leave(member)


# Evento para lidar com erros de comando
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Comando não encontrado. Use !listcommands para ver a lista de comandos disponíveis.", color=discord.Color.red())
        await ctx.send(embed=embed)

