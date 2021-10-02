import discord
from math import ceil
from player_info.get_skin import get_avatar

#Returns an embed with a bunch of stats.
def stats_embed(stats, arg):

    embed = discord.Embed(titel=f"Stats", description=f"**{arg}'s Profile Overview !**")
    embed.add_field(name="**Average Skill Level**", value=f"{stats['average_skill']}, \
    true sa: {stats['true_average_skill']}")
    embed.add_field(name="**Catacombs level**", value=stats["catacombs_level"])
    embed.add_field(name="Slayers", value=f"{stats['slayers_xp']} Total XP !")
    embed.add_field(name="Weight", value=f"{stats['normal_weight']} + {stats['overflow_weight']}\n\
({stats['normal_weight']+stats['overflow_weight']} Total)")
    embed.add_field(name="Coins", value='{:,}'.format(ceil(stats["coins"])))
    embed.add_field(name="Minion Slots", value=stats["minions"])
    embed.add_field(name="Pets", value=stats["pets"])
    embed.add_field(name="Collection tiers unlocked", value=stats["collections"])

    avatar_url = get_avatar(arg)
    embed.set_thumbnail(url=avatar_url)

    return embed