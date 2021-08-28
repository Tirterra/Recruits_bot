from math import floor, ceil

from discord import embeds
from get_weight import get_dungeon_weight, get_skills_weight, get_slayers_weight
from get_lvl import get_slayer_lvl, get_dungeon_lvl, get_skill_lvl, get_dungeons, get_skills, get_slayers
import discord
from get_skin import get_avatar

def create_weight_embed(arg, res, current):

    skills_weight = get_skills_weight(res, current)
    dungeon_weight = get_dungeon_weight(res, current)
    slayers_weight = get_slayers_weight(res, current)

    skills = get_skills(res, current)
    slayers = get_slayers(res, current)
    dungeons = get_dungeons(res, current)

    weight = {
        "total" : {
            "normal" : skills_weight["total"]["normal"] + dungeon_weight["total"]["normal"] + slayers_weight["total"]["normal"],
            "overflow" : skills_weight["total"]["overflow"] + dungeon_weight["total"]["overflow"] + slayers_weight["total"]["overflow"]
        },
        "skills" : skills_weight,
        "dungeon" : dungeon_weight,
        "slayers" : slayers_weight,
    }

    embed = discord.Embed(
        title=f"**{arg}'s weight on {res['profiles'][current]['cute_name']}**",
        description=f"**{weight['total']['normal']}** normal \
+ **{weight['total']['overflow']}** overflow\n\
(**{weight['total']['normal'] + weight['total']['overflow']}** total)",
        color=discord.Color.orange(),
        )

    avatar_url = get_avatar(arg)
    embed.set_thumbnail(url=avatar_url)

    skill_embed = str(f"""```css\n\
Mining     > lvl: {floor(skills['mining']['level'])}    Weight: {skills_weight['mining']['normal']} + {skills_weight['mining']['overflow']}\n\
Foraging   > lvl: {floor(skills['foraging']['level'])}    Weight: {skills_weight['foraging']['normal']} + {skills_weight['foraging']['overflow']}\n\
Enchanting > lvl: {floor(skills['enchanting']['level'])}    Weight: {skills_weight['enchanting']['normal']} + {skills_weight['enchanting']['overflow']}\n\
Farming    > lvl: {floor(skills['farming']['level'])}    Weight: {skills_weight['farming']['normal']} + {skills_weight['farming']['overflow']}\n\
Combat     > lvl: {floor(skills['combat']['level'])}    Weight: {skills_weight['combat']['normal']} + {skills_weight['combat']['overflow']}\n\
Fishing    > lvl: {floor(skills['fishing']['level'])}    Weight: {skills_weight['fishing']['normal']} + {skills_weight['fishing']['overflow']}\n\
Alchemy    > lvl: {floor(skills['alchemy']['level'])}    Weight: {skills_weight['alchemy']['normal']} + {skills_weight['alchemy']['overflow']}\n\
Taming     > lvl: {floor(skills['taming']['level'])}    Weight: {skills_weight['taming']['normal']} + {skills_weight['taming']['overflow']}```"""
    )

    slayers_embed = str(f"""```css\n\
Revenant  > EXP: {slayers['zombie']}    Weight: {slayers_weight['zombie']['normal']} + {slayers_weight['zombie']['overflow']}\n\
Tarantula > EXP: {slayers['spider']}    Weight: {slayers_weight['spider']['normal']} + {slayers_weight['spider']['overflow']}\n\
Sven      > EXP: {slayers['wolf']}    Weight: {slayers_weight['wolf']['normal']} + {slayers_weight['wolf']['overflow']}\n\
Enderman  > EXP: {slayers['enderman']}    Weight: {slayers_weight['enderman']['normal']} + {slayers_weight['enderman']['overflow']}```"""
    )

    dungeon_embed = str(f"""```css\n\
Catacomb  > lvl: {floor(dungeons['catacomb']['level'])}    Weight: {floor(dungeon_weight['catacomb']["normal"])} + {floor(dungeon_weight['catacomb']['overflow'])}\n\
Healer    > lvl: {floor(dungeons['healer']['level'])}    Weight: {floor(dungeon_weight['healer']["normal"])} + {floor(dungeon_weight['healer']['overflow'])}\n\
Mage      > lvl: {floor(dungeons['mage']['level'])}    Weight: {floor(dungeon_weight['mage']["normal"])} + {floor(dungeon_weight['mage']['overflow'])}\n\
Berserk   > lvl: {floor(dungeons['berserk']['level'])}    Weight: {floor(dungeon_weight['berserk']["normal"])} + {floor(dungeon_weight['berserk']['overflow'])}\n\
Archer    > lvl: {floor(dungeons['archer']['level'])}    Weight: {floor(dungeon_weight['archer']["normal"])} + {floor(dungeon_weight['archer']['overflow'])}\n\
Tank      > lvl: {floor(dungeons['tank']['level'])}    Weight: {floor(dungeon_weight['tank']["normal"])} + {floor(dungeon_weight['tank']['overflow'])}```"""
    )

    embed.add_field(
        name=f"Skills Weight: **{skills_weight['total']['normal']}** + \
**{skills_weight['total']['overflow']}** (**{skills_weight['total']['normal'] + skills_weight['total']['overflow']}** total)",
        value=skill_embed,
        inline=False
        )

    embed.add_field(
        name=f"Slayers Weight: **{slayers_weight['total']['normal']}** + \
**{slayers_weight['total']['overflow']}** (**{slayers_weight['total']['normal'] + slayers_weight['total']['overflow']}** total)",
        value=slayers_embed,
        inline=False
        )

    embed.add_field(
        name=f"Dungeons Weight: **{dungeon_weight['total']['normal']}** + \
**{dungeon_weight['total']['overflow']}** (**{dungeon_weight['total']['normal'] + dungeon_weight['total']['overflow']}** total)",
        value=dungeon_embed,
        inline=False
        )

    return embed