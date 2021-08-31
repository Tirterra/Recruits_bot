from math import floor, ceil
from os import stat
from discord import embeds
from get_weight import get_dungeons_weight, get_skills_weight, get_slayers_weight
from get_lvl import get_secrets, get_slayer_lvl, get_dungeon_lvl, get_skill_lvl, get_dungeons, get_skills, get_slayers
import discord
from get_skin import get_avatar

def weight_embed(arg, weight, skills, dungeons, slayers, cute_name):

    embed = discord.Embed(
        title=f"**{arg}'s weight on {cute_name}**",
        description=f"**{weight['total']['normal']}** normal \
+ **{weight['total']['overflow']}** overflow\n\
(**{weight['total']['normal'] + weight['total']['overflow']}** total)",
        color=discord.Color.orange(),
        )

    avatar_url = get_avatar(arg)
    embed.set_thumbnail(url=avatar_url)

    skill_embed = str(f"```css\n\
Mining     > lvl: {floor(skills['mining']['level'])}    Weight: {weight['skills']['mining']['normal']} + {weight['skills']['mining']['overflow']}\n\
Foraging   > lvl: {floor(skills['foraging']['level'])}    Weight: {weight['skills']['foraging']['normal']} + {weight['skills']['foraging']['overflow']}\n\
Enchanting > lvl: {floor(skills['enchanting']['level'])}    Weight: {weight['skills']['enchanting']['normal']} + {weight['skills']['enchanting']['overflow']}\n\
Farming    > lvl: {floor(skills['farming']['level'])}    Weight: {weight['skills']['farming']['normal']} + {weight['skills']['farming']['overflow']}\n\
Combat     > lvl: {floor(skills['combat']['level'])}    Weight: {weight['skills']['combat']['normal']} + {weight['skills']['combat']['overflow']}\n\
Fishing    > lvl: {floor(skills['fishing']['level'])}    Weight: {weight['skills']['fishing']['normal']} + {weight['skills']['fishing']['overflow']}\n\
Alchemy    > lvl: {floor(skills['alchemy']['level'])}    Weight: {weight['skills']['alchemy']['normal']} + {weight['skills']['alchemy']['overflow']}\n\
Taming     > lvl: {floor(skills['taming']['level'])}    Weight: {weight['skills']['taming']['normal']} + {weight['skills']['taming']['overflow']}```"
    )

    slayers_embed = str(f"```css\n\
Revenant  > EXP: {slayers['zombie']['exp']}    Weight: {weight['slayers']['zombie']['normal']} + {weight['slayers']['zombie']['overflow']}\n\
Tarantula > EXP: {slayers['spider']['exp']}    Weight: {weight['slayers']['spider']['normal']} + {weight['slayers']['spider']['overflow']}\n\
Sven      > EXP: {slayers['wolf']['exp']}    Weight: {weight['slayers']['wolf']['normal']} + {weight['slayers']['wolf']['overflow']}\n\
Enderman  > EXP: {slayers['enderman']['exp']}    Weight: {weight['slayers']['enderman']['normal']} + {weight['slayers']['enderman']['overflow']}```"
    )

    dungeon_embed = str(f"```css\n\
Catacombs > lvl: {floor(dungeons['catacombs']['level'])}    Weight: {floor(weight['catacombs']['catacombs']['normal'])} + {floor(weight['catacombs']['catacombs']['overflow'])}\n\
Healer    > lvl: {floor(dungeons['healer']['level'])}    Weight: {floor(weight['catacombs']['healer']['normal'])} + {floor(weight['catacombs']['healer']['overflow'])}\n\
Mage      > lvl: {floor(dungeons['mage']['level'])}    Weight: {floor(weight['catacombs']['mage']['normal'])} + {floor(weight['catacombs']['mage']['overflow'])}\n\
Berserk   > lvl: {floor(dungeons['berserk']['level'])}    Weight: {floor(weight['catacombs']['berserk']['normal'])} + {floor(weight['catacombs']['berserk']['overflow'])}\n\
Archer    > lvl: {floor(dungeons['archer']['level'])}    Weight: {floor(weight['catacombs']['archer']['normal'])} + {floor(weight['catacombs']['archer']['overflow'])}\n\
Tank      > lvl: {floor(dungeons['tank']['level'])}    Weight: {floor(weight['catacombs']['tank']['normal'])} + {floor(weight['catacombs']['tank']['overflow'])}```"
    )

    embed.add_field(
        name=f"Skills Weight: **{weight['skills']['total']['normal']}** + \
**{weight['skills']['total']['overflow']}** (**{weight['skills']['total']['normal'] + weight['skills']['total']['overflow']}** total)",
        value=skill_embed,
        inline=False
        )

    embed.add_field(
        name=f"Slayers Weight: **{weight['slayers']['total']['normal']}** + \
**{weight['slayers']['total']['overflow']}** (**{weight['slayers']['total']['normal'] + weight['slayers']['total']['overflow']}** total)",
        value=slayers_embed,
        inline=False
        )

    embed.add_field(
        name=f"Dungeons Weight: **{weight['catacombs']['total']['normal']}** + \
**{weight['catacombs']['total']['overflow']}** (**{weight['catacombs']['total']['normal'] + weight['catacombs']['total']['overflow']}** total)",
        value=dungeon_embed,
        inline=False
        )

    return embed

def get_guild_average(leaderboard):

    total = 0

    for player in leaderboard:
        total += leaderboard[player]

    average = total / (len(leaderboard) + 1)
    return average

def get_rank(leaderboard, target):

    for rank, player in enumerate(leaderboard):
        if player.lower() == target.lower():
            return rank

def link_embed(discord_name, minecraft_name):

    embed = discord.Embed(title="Linked:", description=f"Sucessfully linked {minecraft_name} with {discord_name} !")
    return embed

def leaderboard_embed(book, page, leaderbord, average, pos):
    
    leaderboard_embed = ""

    try:

        for index, value in enumerate(book[page - 1]):

            player = list(value.keys())[0]
            rank = (page - 1) * 10 + index
            leaderboard_embed += str(f"#{rank+1}" + (4-len(str(rank)))*" " + f": {player}\n     > {'{:,}'.format(value[player])}\n") 

        field = str(f"```{leaderboard_embed}```")
        embed = discord.Embed(
            title=f"Recruits's {leaderbord} Leaderboard",
            description=f"The guild {leaderbord} average is **{'{:,}'.format(round(average, 2))}** !"
            )
        embed.add_field(name="\u200b", value=field)
        embed.set_footer(text=f"You are ranked #{pos+1} in guild")

        return embed

    except IndexError:

        embed = discord.Embed(title="IndexError", description=f"The list isn't that big: the last page is {len(book)}")
        return embed


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

    return embed


def dungeons_embed(dungeons, secrets, arg):

    embed = discord.Embed(title=f"**{arg}'s Dungeon Catacombs**", description=f"{arg} is catacomb level {dungeons['catacombs']['level']}")
    embed.add_field(name="Healer", value=f"Level: {dungeons['healer']['level']}")
    embed.add_field(name="Mage", value=f"Level: {dungeons['mage']['level']}")
    embed.add_field(name="Berserk", value=f"Level: {dungeons['berserk']['level']}")
    embed.add_field(name="Archer", value=f"Level: {dungeons['archer']['level']}")
    embed.add_field(name="Tank", value=f"Level: {dungeons['tank']['level']}")
    embed.add_field(name="Secrets", value=secrets)

    clears_str = ""

    try:
        clears_str += f"Entrance: {dungeons['clears']['entrance']}\n"
        clears_str += f"f1: {dungeons['clears']['f1']}\n"
        clears_str += f"f2: {dungeons['clears']['f2']}\n"
        clears_str += f"f3: {dungeons['clears']['f3']}\n"
        clears_str += f"f4: {dungeons['clears']['f4']}\n"
        clears_str += f"f5: {dungeons['clears']['f5']}\n"
        clears_str += f"f6: {dungeons['clears']['f6']}\n"
        clears_str += f"f7: {dungeons['clears']['f7']}\n"
    except:
        pass

    clears_embed = str(f"""```{clears_str}```""")
    embed.add_field(name="Floor clears", value=clears_embed)

    fastest_times_str = ""
    try:
        fastest_times_str += f"Entrance: {dungeons['fastest_times']['entrance']['minutes']}:{dungeons['fastest_times']['entrance']['seconds']}\n"
        fastest_times_str += f"floor 1:  {dungeons['fastest_times']['f1']['minutes']}:{dungeons['fastest_times']['f1']['seconds']}\n"
        fastest_times_str += f"floor 2:  {dungeons['fastest_times']['f2']['minutes']}:{dungeons['fastest_times']['f2']['seconds']}\n"
        fastest_times_str += f"floor 3:  {dungeons['fastest_times']['f3']['minutes']}:{dungeons['fastest_times']['f3']['seconds']}\n"
        fastest_times_str += f"floor 4:  {dungeons['fastest_times']['f4']['minutes']}:{dungeons['fastest_times']['f4']['seconds']}\n"
        fastest_times_str += f"floor 5:  {dungeons['fastest_times']['f5']['minutes']}:{dungeons['fastest_times']['f5']['seconds']}\n"
        fastest_times_str += f"floor 6:  {dungeons['fastest_times']['f6']['minutes']}:{dungeons['fastest_times']['f6']['seconds']}\n"
        fastest_times_str += f"floor 7:  {dungeons['fastest_times']['f7']['minutes']}:{dungeons['fastest_times']['f7']['seconds']}\n"
    except :
        pass

    fastest_times_embed = str(f"""```{fastest_times_str}```""")

    embed.add_field(name="Fastest Floor clears", value=fastest_times_embed)

    return embed