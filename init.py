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

        msg = ''

        if len(firstName) == 0:
            msg = 'Sorry, I couldn\'t find that prof!'
        else:
            if len(firstName) > 1:
                msg += 'Found several professors, here are the top results:\n\n'
            
            for i in range(len(firstName)):
                percent = max(wouldTakeAgainPercent[i], 0)
                msg += f'{firstName[i]} {lastName[i]}: Average rating is {avgRating[i]} and {percent:.0f}% would take again, with an average difficulty of {avgDifficulty[i]}\n'

        await message.channel.send(msg)


def main():
    client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
