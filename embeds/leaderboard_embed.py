import discord

# Returns an embed with the leaderboard of a given type of leaderboard.
def leaderboard_embed(book, page, leaderbord, average, pos):
    
    leaderboard_embed = ""

    try:   # Creates the embed.

        for index, value in enumerate(book[page - 1]):   # Creates the page made of 10 lines.

            player = list(value.keys())[0]
            rank = (page - 1) * 10 + index
            leaderboard_embed += str(f"#{rank+1}" + (4-len(str(rank)))*" " + f": {player}\n     > {'{:,}'.format(value[player])}\n") 

        field = str(f"```{leaderboard_embed}```")   # Adds the page as a field to the embed.
        embed = discord.Embed(
            title=f"Recruits's {leaderbord} Leaderboard",
            description=f"The guild {leaderbord} average is **{'{:,}'.format(round(average, 2))}** !"
            )
        embed.add_field(name="\u200b", value=field)
        embed.set_footer(text=f"You are ranked #{pos+1} in guild")

        return embed

    except IndexError:   # If the user tries to access a page that doesn't exist.

        embed = discord.Embed(title="IndexError", description=f"The list isn't that big: the last page is {len(book)}")
        return embed