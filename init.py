from discord import app_commands
from parse_query import parse_query

import discord
import os


client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await tree.sync(guild=discord.Object(id=497544520695808000))


@tree.command(name='ratemyprof', description='Rate profs!', guild=discord.Object(id=497544520695808000))
async def ratemyprof(interaction, message: str):
    query = message.replace(' ', '+')

    firstName, lastName, avgRating, wouldTakeAgainPercent, avgDifficulty = parse_query(query)

    if len(firstName) == 0:
        await interaction.response.send_message('Sorry, I couldn\'t find that prof!')
    else:
        embed = discord.Embed(title=f'Professor Ratings For "{message}"')

        if len(firstName) > 1:
            embed.description = 'Found multiple professors, here are the top results:'
        
        for i in range(len(firstName)):
            percent = max(wouldTakeAgainPercent[i], 0)
            value = f'Average rating is {avgRating[i]} and {percent:.0f}% would take again, with an average difficulty of {avgDifficulty[i]}'
            embed.add_field(name=f'{firstName[i]} {lastName[i]}', value=value, inline=False)

        await interaction.response.send_message(embed=embed)


def main():
    client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
