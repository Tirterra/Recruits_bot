import discord
from player_info.get_skin import get_avatar

# You can figure it out...
def link_embed(discord_name, minecraft_name):

    embed = discord.Embed(title="Linked:", description=f"Sucessfully linked {minecraft_name} with {discord_name} !")
    avatar_url = get_avatar(minecraft_name)
    embed.set_thumbnail(url=avatar_url)

    return embed