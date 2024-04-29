from datetime import timezone, datetime
from config import bot

# Função para formatar a duração da chamada
def format_duration(duration):
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    formatted_time = ""
    if hours > 0:
        formatted_time += f"{hours} hora(s), "
    if minutes > 0:
        formatted_time += f"{minutes} minuto(s) e "
    formatted_time += f"{seconds} segundo(s)"
    return formatted_time

# Função para obter a duração da chamada de voz ou vídeo
async def get_call_duration(member_id):
    voice_state = bot.get_guild(GUILD_ID).get_member(member_id).voice
    if voice_state and voice_state.channel:
        start_time = voice_state.self_mute_time or voice_state.self_deaf_time
        if start_time:
            return datetime.now(timezone.utc) - start_time
    return None
