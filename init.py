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

        success, firstName, lastName, avgRating, wouldTakeAgainPercent, avgDifficulty = parse_query(query)

        if success:
            msg = f'{firstName} {lastName}: Average rating is {avgRating} and {wouldTakeAgainPercent}% would take again, with an average difficulty of {avgDifficulty}'
            await message.channel.send(msg)
        else:
            await message.channel.send('Sorry, I couldn\'t find that prof!')


def main():
    client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
