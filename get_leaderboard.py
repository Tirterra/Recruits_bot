import os
import discord
import json

def get_booked_leaderboard(leaderboard):

    book = []

    for count, player in enumerate(leaderboard):

        modulo = int(count) % 10

        if modulo == 0 and count > 3:
            book.append(current_page)
            current_page = []
        elif count == 0:
            current_page = []

        current_page.append({player : leaderboard[player]})

    return book

def get_leaderboard(arg):

    def get_main_name(arg):
        
        if arg.lower() == "dg" or arg.lower() == "dungeons" or arg.lower() == "cata":
            return "catacombs"
        elif arg.lower() == "sa" or arg.lower() == "skill average":
            return "skill_average"
        elif arg.lower() == "eman":
            return "enderman"
        elif arg.lower() == "revs":
            return "revenants"
        elif arg.lower() == "tara" or arg.lower() == "taras":
            return "tarantula"
        elif arg.lower == "we":
            return "weight"
        else:
            return arg

    DIR_PATH = os.path.dirname(__file__)

    availables = [
        "catacombs",
        "skill_average",
        "slayers",
        "revenants",
        "tarantula",
        "svens",
        "enderman",
        "secrets",
        "weight",
        ]

    arg = get_main_name(arg)

    if arg not in availables:
        arg = "help"
    
    if arg == "help":

        embed = discord.Embed(title="Leaderboard help")
        embed.add_field(name="available leaderboards:", value="""```-dungeons(dg)     -skill average(sa)\n-slayers  \
        -revenants(revs)\n-tarantula(tara)  -svens\n-enderman(eman)   -secrets\n-weight```""")

        return embed, arg

    with open(DIR_PATH+r"\guild_data.json", "r") as file:
        guild_data = json.load(file)
    
    leaderboard = {}

    for player in guild_data:
        leaderboard.update({player : guild_data[player][arg]})

    leaderboard = {player : cata for player, cata in sorted(leaderboard.items(), key=lambda item : item[1], reverse=True)}
    return leaderboard, arg