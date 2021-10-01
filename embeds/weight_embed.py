import discord
from math import floor

from player_info.get_skin import get_avatar

# Returns an embed with all the weight info you can ever dream of.
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

    # This is the skill embed.
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

    # The slayer one.
    slayers_embed = str(f"```css\n\
Revenant  > EXP: {slayers['zombie']['exp']}    Weight: {weight['slayers']['zombie']['normal']} + {weight['slayers']['zombie']['overflow']}\n\
Tarantula > EXP: {slayers['spider']['exp']}    Weight: {weight['slayers']['spider']['normal']} + {weight['slayers']['spider']['overflow']}\n\
Sven      > EXP: {slayers['wolf']['exp']}    Weight: {weight['slayers']['wolf']['normal']} + {weight['slayers']['wolf']['overflow']}\n\
Enderman  > EXP: {slayers['enderman']['exp']}    Weight: {weight['slayers']['enderman']['normal']} + {weight['slayers']['enderman']['overflow']}```"
    )

    # And the dungeons one.
    dungeon_embed = str(f"```css\n\
Catacombs > lvl: {floor(dungeons['catacombs']['level'])}    Weight: {floor(weight['catacombs']['catacombs']['normal'])} + {floor(weight['catacombs']['catacombs']['overflow'])}\n\
Healer    > lvl: {floor(dungeons['healer']['level'])}    Weight: {floor(weight['catacombs']['healer']['normal'])} + {floor(weight['catacombs']['healer']['overflow'])}\n\
Mage      > lvl: {floor(dungeons['mage']['level'])}    Weight: {floor(weight['catacombs']['mage']['normal'])} + {floor(weight['catacombs']['mage']['overflow'])}\n\
Berserk   > lvl: {floor(dungeons['berserk']['level'])}    Weight: {floor(weight['catacombs']['berserk']['normal'])} + {floor(weight['catacombs']['berserk']['overflow'])}\n\
Archer    > lvl: {floor(dungeons['archer']['level'])}    Weight: {floor(weight['catacombs']['archer']['normal'])} + {floor(weight['catacombs']['archer']['overflow'])}\n\
Tank      > lvl: {floor(dungeons['tank']['level'])}    Weight: {floor(weight['catacombs']['tank']['normal'])} + {floor(weight['catacombs']['tank']['overflow'])}```"
    )

    # I just add all the field values in the corresponding field.
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