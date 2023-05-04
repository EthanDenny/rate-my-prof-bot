from parse_query import parse_query

import discord
import os


client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ratemyprof '):
        query = message.content[12:].replace(' ', '+')

        firstName, lastName, avgRating, wouldTakeAgainPercent, avgDifficulty = parse_query(query)

        if len(firstName) == 0:
            await message.channel.send('Sorry, I couldn\'t find that prof!')
        else:
            embed = discord.Embed(title='Professor Ratings')

            if len(firstName) > 1:
                embed.title = 'Professor Ratings'
                embed.description = 'Found multiple professors, here are the top results:'
            else:
                embed.title = 'Professor Rating'
            
            for i in range(len(firstName)):
                percent = max(wouldTakeAgainPercent[i], 0)
                value = f'Average rating is {avgRating[i]} and {percent:.0f}% would take again, with an average difficulty of {avgDifficulty[i]}'
                embed.add_field(name=f'{firstName[i]} {lastName[i]}', value=value, inline=False)

            await message.channel.send(embed=embed)


def main():
    client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
