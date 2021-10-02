import discord
from player_info.get_skin import get_avatar

# Returns a embed withh all the dungeon stats.
def dungeons_embed(dungeons, secrets, arg):

    # Creates an embed and adds a bunch of fields.
    embed = discord.Embed(titel=f"**{arg}'s Dungeon Catacombs**", description=f"{arg} is catacomb level {dungeons['catacombs']['level']}")
    embed.add_field(name="Healer", value=f"Level: {dungeons['healer']['level']}")
    embed.add_field(name="Mage", value=f"Level: {dungeons['mage']['level']}")
    embed.add_field(name="Berserk", value=f"Level: {dungeons['berserk']['level']}")
    embed.add_field(name="Archer", value=f"Level: {dungeons['archer']['level']}")
    embed.add_field(name="Tank", value=f"Level: {dungeons['tank']['level']}")
    embed.add_field(name="Secrets", value=secrets)

    clears_str = ""

    try:   # Creates a big string with all the clears.
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

    try:   # Same but with fastest times.
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

    avatar_url = get_avatar(arg)
    embed.set_thumbnail(url=avatar_url)

    return embed